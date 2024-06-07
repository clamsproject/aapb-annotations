# process script to copy raw csv into new golds directory
# iterate through each raw directory (use yy-mm-dd pattern to find directories)
# copy each csv file to golds directory


from pathlib import Path
import os
import re
import shutil
import pandas as pd

def truncate_total(value):
    """
    This method takes in strings of filenames from the original format (filename column)
    and truncates to just the total_ms value.
    """
    truncated = value.split("_")[-2]
    return truncated
def truncate_convert_ISO(value):
    """
    This method takes in strings of filenames from the original format (filename column)
    and truncates it to just the millisecond value, and then converts the milliseconds to
    ISO standard timestamps.
    """
    # get last portion of value, delimited by underscores
    truncated = value.split("_")[-1]
    # remove file extension
    truncated = truncated[:-4]
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
            df['timestamp'] = df['filename'].apply(truncate_convert_ISO)
            # add total column (total_ms, second to last set of numbers in filename)
            df.insert(2, 'total', df['filename'].apply(truncate_total))
            # remove unseen
            df = df[(df.seen != "false") & (df.seen != "False")]
            # remove first column (filename)
            df = df.drop('filename', axis=1)
            # output to csv with same filename
            df.to_csv(destination, index=False)
