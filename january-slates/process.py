"""Processes Slate annotation files
To read all the tabular files from in the YYMMDD-batchname directories and generate one file per GUID in golds

$ process.py --input_path /your/input/path --output_path /your/output/path

"""

import argparse
import pandas as pd
import numpy as np
import os


def process_csv(input_directory, output_directory):
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
                tsv_filename = f"{guid}.tsv"
                tsv_filepath = os.path.join(output_directory, tsv_filename)
                os.makedirs(os.path.dirname(tsv_filepath), exist_ok=True)
                row_df = pd.DataFrame([row[desired_columns]])
                for time_col in ['start', 'end']:
                    v = row_df[time_col].values[0]
                    if v.startswith('no'):
                        row_df[time_col] = 'NO'
                    elif ';' in v:
                        # standard format is 00:00:00.000, which is 12 characters
                        row_df[time_col] = '.'.join(v.split(';')) + '0' * (12 - len(v))
                    elif ':' in v:
                        row_df[time_col] = f'{v}.000'
                v = row_df['type'].values[0]
                if pd.isnull(v):
                    continue
                elif v.lower().startswith('hand') or v.lower().startswith('fixed'):
                    row_df['type'] = 'h'
                elif v.lower().startswith('type'):
                    row_df['type'] = 't'
                elif len(v) == 0:
                    continue
                else:
                    raise ValueError(f"Unknown type: {v}")
                v = row_df['digital'].values[0]
                if pd.isnull(v):
                    continue
                elif v.lower().startswith('digit'):
                    row_df['digital'] = True
                elif v.lower().startswith('record'):
                    row_df['digital'] = False
                # elif len(v) == 0:
                #     continue
                else:
                    raise ValueError(f"Unknown type: {v}")
                if row_df['start'].values[0]:
                    row_df.to_csv(tsv_filepath, index=False, sep='\t')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', type=str,
                        help='Path to the directory containing the CLAMS slate annotation metadata files')
    parser.add_argument('--output_path', type=str, default='golds',
                        help='Path to the output .tsv file')
    args = parser.parse_args()
    process_csv(args.input_path, args.output_path)
    print("Processing complete.")


