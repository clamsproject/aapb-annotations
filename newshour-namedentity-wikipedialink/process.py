"""Processes Named Entity Linking annotation files:

Reads in the `.tab` annotations file containing grounding information in the `BATCH` directory,
then reads in each brat .ann file (from previous `newshour-namedentity` annotation project) 
downloaded from URL specified in `base-ner.url` file in the same BATCH directory, 
then outputs a tsv file for each unique GUID. During the conversion, it also fetches wikidata 
QIDs using the wikipedia URLs in the data. Converted tsv files are exported to a `golds` directory
at the top level of this repository, where they are ready to be committed back
into the annotation collection repository and pushed up. The script does not do
the automatic commit and push in order to avoid hasty commits.

"""

import argparse
from pathlib import Path
from typing import List, Union
from urllib.parse import unquote_plus

import pandas as pd
import requests
from brat_parser import get_entities_relations_attributes_groups

from clams_utils.aapb import goldretriever


def fetch_wikidata_qids(urls: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    Fetch wikidata QIDs from English Wikipedia URLs.
    """
    api = "https://en.wikipedia.org/w/api.php?"
    # headers
    reqheaders = {'Accept': 'application/json'}
    if isinstance(urls, list):
        titles = [unquote_plus(url.split("/")[-1]) for url in urls]
        titles = " | ".join(titles)
    else:
        titles = unquote_plus(urls.split("/")[-1])
    # parameters to use
    params = {
        'action': 'query',
        'prop': 'pageprops',
        'ppprop': 'wikibase_item',
        'titles': titles,
        'redirects': 1,
        'format': 'json'
    }
    json_data = requests.post(api, data=params, headers=reqheaders).json()
    # parse resulting json for QIDs
    qids = []
    for page in json_data['query']['pages'].values():
        qid = page['pageprops']['wikibase_item']
        qids.append("https://www.wikidata.org/wiki/" + qid)
    if len(qids) > 1:
        return list(reversed(qids))
    else:
        return qids[0]


def parse_arguments():
    ap = argparse.ArgumentParser(
        description=__doc__)
    ap.add_argument('BATCH', help='Directory containing the annotations file with grounding information (.tab format). Must start with YYMMDD- prefix to infer the batch name. Also must contain `base-ner.url` file with the URL to the NER annotations.')
    return ap.parse_args()


if __name__ == '__main__':

    options = parse_arguments()

    ann_batch_dir = Path(options.batch).resolve()
    ner_dir = Path(goldretriever.download_golds(open(Path(options.batch)/'base-ner.url').read().strip()))

    batch_name = ann_batch_dir.name[7:]
    gold_dir = ann_batch_dir.parent / 'golds' / batch_name
    gold_dir.mkdir(parents=True, exist_ok=True)
    print(f'>>> Exporting {batch_name} annotations to the gold directory')
    print(f'>>> --> {gold_dir}')

    brat_anns = ner_dir.glob('*.ann')
    tab_file = next(ann_batch_dir.glob('*.tab'))

    # read in the relevant information from the annotations.tab
    with open(tab_file) as fh_in:
        nel_df = pd.read_table(fh_in, sep='\t', encoding='utf-16', header=None)
    nel_df.dropna(axis=1, how='all', inplace=True)
    nel_df.drop(nel_df.columns[[0, 1, 4, 5]], axis=1, inplace=True)
    nel_df.columns = ['guid', 'text', 'wiki_url']

    # read in the entities for each .ann file
    for brat_ann in brat_anns:
        entities, relations, attributes, groups = get_entities_relations_attributes_groups(brat_ann)
        data = {'guid': brat_ann.name,
                'anno_id': [entities[e].id for e in entities],
                'type': [entities[e].type for e in entities],
                'begin_offset': [entities[e].span[0][0] for e in entities],
                'end_offset': [entities[e].span[0][1] for e in entities],
                'text': [entities[e].text for e in entities]}
        ner_df = pd.DataFrame(data=data, columns=['guid', 'anno_id', 'type', 'begin_offset', 'end_offset', 'text'])
        # collapse all 'title' subtypes into one category
        ner_df['type'].mask(ner_df['type'].str.endswith("title"), "title", inplace=True)

        # merge wiki_url column from nel dataframe, fetch qids
        ner_df = ner_df.merge(nel_df, how='left', on=['guid', 'text'])
        ner_df['qid'] = ner_df['wiki_url'].map(fetch_wikidata_qids, na_action='ignore')
        ner_df.to_csv(Path(gold_dir, data['guid'].rstrip('-transcript.ann')).with_suffix('.tsv'), sep='\t', index=False)
