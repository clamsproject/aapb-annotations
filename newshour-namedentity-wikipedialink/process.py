"""Processes Named Entity Linking annotation files

$ process.py [-h] PROJECT_DIR

Reads in each '.tab' annotation file in the 'PROJECT_DIR' directory.
Fetches wikidata QIDs using the wikipedia URLs in the data.
Generates a tsv file for each unique GUID. Exports the results to a "gold" directory
at the top level of this repository, where they are ready to be committed back
into the annotation collection repository and pushed up. The script does not do
the automatic commit and push in order to avoid hasty commits.

"""

import argparse
import pandas as pd
from pathlib import Path
import requests
from typing import List, Union
from urllib.parse import unquote_plus


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
        description='Process uploaded NER annotation files with named entity links')
    ap.add_argument('batch', help='Directory containing the batch the process')
    return ap.parse_args()


if __name__ == '__main__':

    options = parse_arguments()

    batch_dir = Path(options.batch).resolve()

    batch = Path(options.batch).resolve().name
    repo_dir = (Path(__file__).parent / '..' / '..').resolve()
    gold_dir = repo_dir / 'golds' / 'nel' / batch
    gold_dir.mkdir(parents=True, exist_ok=True)
    print(f'>>> Exporting {batch} annotations to the gold directory')
    print(f'>>> --> {gold_dir}')
    for tab_file in batch_dir.glob('*.tab'):
        with open(tab_file) as fh:
            df = pd.read_table(fh, sep='\t', encoding='utf-16', header=None)
        df.dropna(axis=1, how='all', inplace=True)
        df.columns = ['index', 'timestamp', 'GUID', 'entity', 'type', 'instances', 'wiki_url']
        df['QID'] = df['wiki_url'].map(fetch_wikidata_qids, na_action='ignore')
        grouped = df.groupby(['GUID'])
        unique_guids = list(df["GUID"].unique())
        for guid in unique_guids:
            output_df = grouped.get_group(guid)
            output_df.to_csv(Path(gold_dir, guid.rstrip('-transcript.ann')).with_suffix('.tsv'), sep='\t', index=False)
