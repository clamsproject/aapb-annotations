"""
Processes Slate annotation files. 
To read all the tabular files from in the YYMMDD-batchname directories and generate one file per GUID in golds
"""

import os
import pathlib
import shutil

import pandas as pd


def process(input_directory, output_directory):
    desired_columns = ["GUID", "collection", "start", "end", "type", "digital", "format-summary", "moving-elements"]
    for filename in os.listdir(input_directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(input_directory, filename)
            df = pd.read_csv(filepath,encoding='utf-8')
            df.replace(',', '', regex=True, inplace=True)
            df.columns = [col.replace(',', '') for col in df.columns]
            df.columns = [col.replace('"', '') for col in df.columns]
            df.columns = [col.replace(' ', '') for col in df.columns]
            df.rename(columns={
                'Series/Group': 'collection',
                'SlateStart': 'start',
                'SlateEnd': 'end',
                'WritingTypes': 'type',
                'Recorded/Digital': 'digital',
                'formatofmostoftheinformation': 'format-summary',
                'Anythingmovingonscreenduringslate?': 'moving-elements'
            }, inplace=True)
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].str.strip().str.replace(r'\s+', ' ')
            for _, row in df.iterrows():
                guid = row['GUID']
                csv_filename = f"{guid}.csv"
                csv_filepath = os.path.join(output_directory, csv_filename)
                os.makedirs(os.path.dirname(csv_filepath), exist_ok=True)
                row_df = pd.DataFrame([row[desired_columns]])
                is_annotated = False
                has_slate = False
                for time_col in ['start', 'end']:
                    v = row_df[time_col].values[0]
                    if v.startswith('no'):
                        row_df[time_col] = 'NO'
                        is_annotated = True
                    elif ';' in v:
                        # standard format is 00:00:00.000, which is 12 characters
                        time, frnum = v.split(';')
                        millisecs = int(frnum[:2]) / 30 * 1000
                        row_df[time_col] = f'{time}.{millisecs:03.0f}'
                        is_annotated = True
                        has_slate = True
                    elif ':' in v:
                        row_df[time_col] = f'{v}.000'
                        is_annotated = True
                        has_slate = True
                if not is_annotated:
                    print(f"Start or end time not annotated for {row_df['GUID'].values[0]}")
                    continue
                v = row_df['type'].values[0]
                if not has_slate:
                    row_df['type'] = '-'
                elif v.lower().startswith('hand') or v.lower().startswith('fixed'):
                    row_df['type'] = 'h'
                elif v.lower().startswith('type'):
                    row_df['type'] = 't'
                else:
                    raise ValueError(f"Unknown type: {v}")
                v = row_df['digital'].values[0]
                if not has_slate:
                    row_df['digital'] = False
                elif v.lower().startswith('digit'):
                    row_df['digital'] = True
                elif v.lower().startswith('record'):
                    row_df['digital'] = False
                else:
                    raise ValueError(f"Unknown type: {v}")
                row_df.to_csv(csv_filepath, index=False, sep=',')


if __name__ == '__main__':
    task_dir = pathlib.Path(__file__).parent
    golds_dir = task_dir / 'golds'

    # delete golds directory if it exists
    shutil.rmtree(golds_dir, ignore_errors=True)
    # then start from clean slate
    golds_dir.mkdir(exist_ok=True)

    # find all directories starts with six digits and a dash
    for batch_dir in task_dir.glob('[0-9][0-9][0-9][0-9][0-9][0-9]-*'):
        process(batch_dir, golds_dir)
