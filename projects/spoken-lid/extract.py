"""

Open an SQLite database with LID annotations and write the results to a CSV file.

Note that the resulting CSV file may have more rows than the table because quotes
are enabled and therefore text fields with newlines will cause the row to be written
to multiple lines.

To make the annotators anonymous we use a file named mappings.py which is not in
the repository but stored elsewhere. Its contents look like the sample file named
sample_mappings.py, but with usernameN replaced with the username in the database.

TODO:
- This does not yet deal with subsequent data drops where new rows in the data base
are added to another data drop file

"""

import csv
import sqlite3
import argparse
from pathlib import Path

from mappings import annotators


def extract(dbfile: str, datadrop: str):

    data = load_db(dbfile)
    write_files(datadrop, data)


def load_db(dbfile: str) -> dict:
    """Load all data from the database, with rows grouped by guid."""
    with sqlite3.connect(dbfile) as connection:
        data = {'column-names': None, "guids": {}}
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM annotation_events")
        data['column-names'] = [description[0] for description in cursor.description]
        row_count = 0
        for row in cursor:
            row_count += 1
            copied_row = list(row)
            # anonymize the annotator name
            copied_row[1] = annotators[row[1]]
            guid = row[3]
            data['guids'].setdefault(guid, []).append(copied_row)
        print(f'Extracted {row_count} rows from "{dbfile}"')
        return data


def write_files(datadrop: str, data: dict):
    drop_path = Path(datadrop)
    drop_path.mkdir(exist_ok=True)
    columns = data['column-names']
    row_count = 0
    for guid in data['guids']:
        csvfile = Path(drop_path) / f'{guid}.csv'
        with open(csvfile, 'w') as fh:
            writer = csv.writer(fh, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(columns)
            for row in data['guids'][guid]:
                row_count += 1
                writer.writerow(row)
    print(f'Wrote {row_count} rows to {len(data["guids"])} files in "{datadrop}"')


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            'Extract rows from an SQLite database and save them as data drop files.'))
    parser.add_argument('dbfile', help='the SQLite database')
    parser.add_argument('directory', help='the output directory for the data drop')
    return parser.parse_args()


if __name__ == '__main__':

    args = parse_arguments()
    extract(args.dbfile, args.directory)
