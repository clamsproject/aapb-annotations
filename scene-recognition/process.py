import pathlib
import shutil

import pandas as pd


def truncate(value, is_total = False):
    """
    This method takes in strings of filenames from the original format (filename column)
    and truncates to either the total_ms value or the timestamp value based on boolean is_total
    """
    if is_total:
        truncated = value.split("_")[1]
    else:
        # get last portion of value, delimited by underscores
        truncated = value.split("_")[-1]
        # remove file extension
        truncated = truncated[:-4]
    return truncated


def format_timecode(value):
    """
    This method takes in a string of milliseconds and then converts the milliseconds to
    ISO standard timestamps.
    """
    _, cur = value.split('.')[0].rsplit("_", maxsplit=1)
    # remove extension and cast type 
    ms = int(cur.split(".")[0])
    # 3600000 milliseconds per hour, 60000 milliseconds per minute, 1000 miliseconds per second
    hours = ms // 3600000
    ms %= 3600000
    minutes = ms // 60000
    ms %= 60000
    seconds = ms // 1000
    ms %= 1000
    timestamp = str(hours).zfill(2) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2) + "." + str(ms).zfill(3)
    return timestamp


def process(raw_dir, golds_dir):
    for file in raw_dir.glob('*.csv'):
        source = file
        print(file)
        destination = golds_dir / file.with_suffix('.csv').name
        # read in as dataframe to more easily manipulate columns
        df = pd.read_csv(source)
        # create new timestamp column and fill with values
        df.insert(1, 'at', "")
        df['at'] = df['filename'].apply(format_timecode)
        # remove unseen
        df = df[(df.seen != "false") & (df.seen != "False")]
        # remove seen column
        df = df.drop('seen', axis=1)
        # then rename columns
        df = df.rename(columns={
            'type label': 'scene-type',
            'type-label': 'scene-type',
            'subtype label': 'scene-subtype',
            'subtype-label': 'scene-subtype',
            'modifier': 'transitional',
        })
        # any that are left have been seen. therefore, any rows with label = "" are negative
        # so their labels should be changed to "-"
        df.loc[df['scene-type'].isna(), 'scene-type'] = '-'
        # remove first column (filename)
        df = df.drop('filename', axis=1)
        # remove transcript and note columns, if they exist
        for col in ['transcript', 'note', 'note-3', 'note-4']:
            if col in df.columns:
                df = df.drop(col, axis=1)
        # sort by `at` col
        df = df.sort_values(by=['at'])
        # output to csv with same filename
        df.to_csv(destination, index=False)


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
