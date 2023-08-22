"""Processes Slate annotation files
To read all the tabular files from in the YYMMDD-batchname directories and generate one file per GUID in golds

$ process.py --input_path /your/input/path --output_path /your/output/path

"""

import argparse
import pandas as pd
import os


def process_csv(input_directory, output_directory):
    desired_columns = [
        "GUID", "Series/Group", "Slate Start", "Slate End",
        "Writing Types", "Recorded/Digital", "format of most of the information",
        "Anything moving on screen during slate?"
    ]
    batchname = os.path.basename(input_directory)[7:]  # chopping date prefix
    for filename in os.listdir(input_directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(input_directory, filename)
            df = pd.read_csv(filepath,encoding='utf-8')
            df.replace(',', '', regex=True, inplace=True)
            df.columns = [col.replace(',', '') for col in df.columns]
            df.columns = [col.replace('"', '') for col in df.columns]
            df.columns = [col.replace(' ', '') for col in df.columns]
            df.rename(columns={
                'SlateStart': 'Slate Start',
                'SlateEnd': 'Slate End',
                'WritingTypes': 'Writing Types',
                'formatofmostoftheinformation': 'format of most of the information',
                'Anythingmovingonscreenduringslate?': 'Anything moving on screen during slate?'
            }, inplace=True)
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].str.strip().str.replace(r'\s+', ' ')
            for _, row in df.iterrows():
                guid = row['GUID']
                tsv_filename = f"{guid}.tsv"
                tsv_filepath = os.path.join(output_directory, batchname, tsv_filename)
                os.makedirs(os.path.dirname(tsv_filepath), exist_ok=True)
                row_df = pd.DataFrame([row[desired_columns]])
                if row_df['Slate Start'].values[0]:
                    row_df.to_csv(tsv_filepath, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', type=str,
                        help='Path to the directory containing the CLAMS slate annotation metadata files')
    parser.add_argument('--output_path', type=str, default='golds',
                        help='Path to the output .tsv file')
    args = parser.parse_args()
    process_csv(args.input_path, args.output_path)
    print("Processing complete.")


