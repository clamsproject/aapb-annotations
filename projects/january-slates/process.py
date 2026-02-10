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
            pos, neg = 0, 0
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
                    # print(f"Start or end time not annotated for {row_df['GUID'].values[0]}")
                    continue
                else:
                    if has_slate:
                        pos += 1
                        # print(f"positive annotation: {pos}")
                    else:
                        neg += 1
                        # print(f"negative annotation: {neg}")
                # manual inspection of the raw annotation shows that 
                # "digital" always implied "typed", and "recorded" always implied "handwriting"
                # there's one instance of "fixed-recorded" combination, but we will treat it 
                # as "handwriting" for now
                if has_slate:
                    subtype = "digital" if row_df['digital'].values[0].startswith('digit') else "handwriting"
                else:
                    subtype = '-'
                # drop unnecessary columns
                row_df.drop(columns=['GUID', 'digital', 'type'], inplace=True)
                # then add columns for labels based on has_slate and subtype values
                row_df.insert(3, 'scene-label', 'slate' if has_slate else '-')
                row_df.insert(4, 'scene-subtype-label', subtype)
                # row_df['scene-subtype'] = subtype
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
