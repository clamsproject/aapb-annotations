"""

Create gold files from a selected data drop.

TODO:
- allow a set of data drops, without it there could be a problem when two data
  drops both have annotations for the same file
- there are 92 rows with an empty label, these should be skipped
- review the normalized language labels
- review whether all annotators need to be included
- determine whether it is a problem that some timeframes overlap

"""


import csv
import argparse
from pathlib import Path

from mappings import languages


def create_golds(datadrop: str):
    datadrop_path = Path(datadrop)
    golds_created = 0
    for csvfile in datadrop_path.iterdir():
        content = load_csv_file(csvfile)
        selected_content= select_content(content)
        write_content_to_gold_file(csvfile.name, selected_content)
        golds_created += 1
    print(f'Created {golds_created} gold files from {datadrop}')


def load_csv_file(filename: str, verbose=False) -> list:
    """Return a list of rows from a csv file."""
    with open(filename) as csvfile:
        content = []
        reader = csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            content.append(row)
        if verbose:
            print(f'Loaded {len(content)} rows from {filename}')
        return content


def select_content(content: list) -> dict:
    selected_content = {}
    for row in content:
        start = row['start_sec']
        end = row['end_sec']
        label = row['label']
        # For now we assume that the last annotation is the one we want. If we
        # want to change that we should collect all annotations and then select
        # one:
        #    selected_content.setdefault((start,end), []).append(label)
        #    select_annotations(annotations)
        selected_content[(start,end)] = label
    return selected_content


def write_content_to_gold_file(fname: str, content: dict):
    #print(f'{len(content):4d}  {csvfile}')
    gold_file = Path('golds') / fname
    with open(gold_file, 'w') as fh:
        fh.write('start,end,scene-label\n')
        for start, end in sorted(content):
            label = content[(start, end)]
            label = languages.get(label, label)
            start = convert_seconds(start)
            end = convert_seconds(end)
            fh.write(f'{start},{end},{label}\n')


def convert_seconds(seconds: float):
    (hours, seconds) = divmod(seconds, 3600)
    (minutes, seconds) = divmod(seconds, 60)
    formatted = f"{hours:02.0f}:{minutes:02.0f}:{seconds:06.3f}"
    return formatted


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Create gold files from data drop files.')
    parser.add_argument('directory', help='input directory with data drop files')
    return parser.parse_args()



if __name__ == '__main__':

    args = parse_arguments()
    create_golds(args.directory)
