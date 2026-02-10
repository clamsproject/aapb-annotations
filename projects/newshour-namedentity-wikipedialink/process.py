"""Processes Named Entity Linking annotation files.

Reads in the NEL `.tab` annotations file containing grounding/linking information in the `BATCH` directory,
then reads in each brat .ann file (from previous `newshour-namedentity`/NER annotation project)
downloaded from URL specified in `base-ner.url` file in the same BATCH directory, 
then outputs a tsv file for each unique GUID. During the conversion, it also fetches wikidata 
QIDs using the wikipedia URLs in the data. Converted tsv files are exported to a `golds` directory
at the top level of this repository, where they are ready to be committed back
into the annotation collection repository and pushed up. The script does not do
the automatic commit and push in order to avoid hasty commits.

"""

import pathlib
from pathlib import Path
from typing import List, Union
from urllib.parse import unquote_plus

import pandas as pd
import requests
from brat_parser import get_entities_relations_attributes_groups
from clams_utils.aapb import goldretriever

qid_map = {}


def fetch_wikidata_qids(urls: Union[str, List[str]]) -> Union[str, List[str]]:
    """
    Fetch wikidata QIDs from English Wikipedia URLs.
    """
    qids = []
    api = "https://en.wikipedia.org/w/api.php?"
    # headers
    reqheaders = {'Accept': 'application/json'}
    if isinstance(urls, str):
        urls = [urls]
    for title in urls:
        title = unquote_plus(title.split("/")[-1])
        # parameters to use
        if title in qid_map:
            qids.append(qid_map[title])
        else:
            params = {
                'action': 'query',
                'prop': 'pageprops',
                'ppprop': 'wikibase_item',
                'titles': title,
                'redirects': 1,
                'format': 'json'
            }
            json_data = requests.post(api, data=params, headers=reqheaders).json()
            # parse resulting json for QIDs
            for page in json_data['query']['pages'].values():
                qid = page['pageprops']['wikibase_item']
                qid_url = "https://www.wikidata.org/wiki/" + qid
                qid_map[title] = qid_url
                qids.append(qid_url)
    if len(qids) > 1:
        print('TWO OR MORE QIDS')
        return list(reversed(qids))
    else:
        return qids[0]


def process(ner_ann_dir, nel_tab_dir, golds_dir):

    if isinstance(ner_ann_dir, str):
        ner_ann_dir = pathlib.Path(ner_ann_dir)
    if isinstance(nel_tab_dir, str):
        nel_tab_dir = pathlib.Path(nel_tab_dir)
    if isinstance(golds_dir, str):
        golds_dir = pathlib.Path(golds_dir)

    golds_dir.mkdir(parents=True, exist_ok=True)
    print(f'>>> Exporting {nel_tab_dir.name[7:]} annotations to the gold directory')
    print(f'>>> --> {golds_dir}')

    brat_anns = ner_ann_dir.glob('*.ann')
    tab_file = next(nel_tab_dir.glob('*.tab'))

    # read in the relevant information from the annotations.tab
    with open(tab_file) as fh_in:
        nel_df = pd.read_table(fh_in, sep='\t', encoding='utf-16', header=None)
    nel_df.dropna(axis=1, how='all', inplace=True)
    nel_df.drop(nel_df.columns[[0, 1, 4, 5]], axis=1, inplace=True)
    nel_df.columns = ['src_ann', 'text', 'wiki_url']

    # read in the entities for each .ann file
    for brat_ann in brat_anns:
        entities, relations, attributes, groups = get_entities_relations_attributes_groups(brat_ann)
        data = {'src_ann': brat_ann.name,
                'src_ann_id': [entities[e].id for e in entities],
                'type': [entities[e].type for e in entities],
                'start': [entities[e].span[0][0] for e in entities],
                'end': [entities[e].span[0][1] for e in entities],
                'text': [entities[e].text for e in entities]}
        ner_df = pd.DataFrame(data=data, columns=['src_ann', 'src_ann_id', 'type', 'start', 'end', 'text'])
        # collapse all 'title' subtypes into one category
        ner_df['type'].mask(ner_df['type'].str.endswith("title"), "title", inplace=True)

        # merge wiki_url column from nel dataframe, fetch qids
        ner_df = ner_df.merge(nel_df, how='left', on=['src_ann', 'text'])
        ner_df['qid'] = ner_df['wiki_url'].map(fetch_wikidata_qids, na_action='ignore')
        print(f'\tQid: {ner_df["qid"]}')
        ner_df.to_csv(Path(golds_dir, data['src_ann'].rstrip('-transcript.ann')).with_suffix('.tsv'), sep='\t', index=False)

if __name__ == '__main__':

    root_dir = pathlib.Path(__file__).parent
    for nel_tab_dir in root_dir.glob('*'):
        if nel_tab_dir.is_dir() and len(nel_tab_dir.name) > 7 and nel_tab_dir.name[6] == '-' and all([c.isdigit() for c in nel_tab_dir.name[:6]]):
            base_ner_url = open(nel_tab_dir / 'base-ner.url').read().strip()
            print(f'Downloading the base NER annotations from {base_ner_url} ...')
            ner_ann_dir = Path(goldretriever.download_golds(base_ner_url))
            gold_dir = nel_tab_dir.parent / 'golds'
            print(f'Processing {nel_tab_dir.name}...')
            process(ner_ann_dir, nel_tab_dir, root_dir / 'golds')
