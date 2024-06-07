# process script to copy raw csv into new golds directory
# iterate through each raw directory (use yy-mm-dd pattern to find directories)
# copy each csv file to golds directory


from pathlib import Path
import numpy as np
import re
import shutil
import pandas as pd

def truncate(value, is_total = False):
    """
    This method takes in strings of filenames from the original format (filename column)
    and truncates to either the total_ms value or the timestamp value based on boolean is_total
    """
    if is_total:
        truncated = value.split("_")[-2]
    else:
        # get last portion of value, delimited by underscores
        truncated = value.split("_")[-1]
        # remove file extension
        truncated = truncated[:-4]
    return truncated
def convert_ISO(value, is_total):
    """
    This method takes in a string of milliseconds and then converts the milliseconds to
    ISO standard timestamps.
    """
    truncated = truncate(value, is_total)
    ms = int(truncated)
    # 3600000 milliseconds per hour, 60000 milliseconds per minute, 1000 miliseconds per second
    hours = ms // 3600000
    ms %= 3600000
    minutes = ms // 60000
    ms %= 60000
    seconds = ms // 1000
    ms %= 1000
    timestamp = str(hours).zfill(2) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2) + "." + str(ms).zfill(3)
    return timestamp


folder = Path.cwd()
goldpath = folder / 'golds'
# iterate through files in scene-recognition
# if a directory starts w/ yy-mm-dd pattern, copy contents to the golds directory
for directory in folder.glob('*'):
    if directory.is_dir() and re.match("[0-9]{2}[0-1][0-9][0-3][0-9]", directory.name):
        # copy contents by iterating
        for file in directory.glob('*'):
            source = file
            destination = goldpath / file.name
            shutil.copy2(source, destination)
            # read in as dataframe to more easily manipulate columns
            df = pd.read_csv(destination)
            # create new timestamp column and fill with values
            df.insert(1, 'timestamp', "")
            df['timestamp'] = df['filename'].apply(convert_ISO, is_total=False)
            # add total column (total_ms, second to last set of numbers in filename)
            df.insert(2, 'total', df['filename'].apply(convert_ISO, is_total=True))
            # remove unseen
            df = df[(df.seen != "false") & (df.seen != "False")]
            # remove seen column
            df = df.drop('seen', axis=1)
            # any that are left have been seen. therefore, any rows with label = "" are negative
            # so their labels should be changed to "-"
            df['type label'] = np.where(df['type label'] == "", "-", df['type label'])
            # remove first column (filename)
            df = df.drop('filename', axis=1)
            # remove transcript and note columns
            df = df.drop('transcript', axis=1)
            df = df.drop('note', axis=1)
            # output to csv with same filename
            df.to_csv(destination, index=False)
