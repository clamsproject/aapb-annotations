# process script to copy raw csv into new golds directory
# iterate through each raw directory (use yy-mm-dd pattern to find directories)
# copy each csv file to golds/timepoints directory (with some changes)
# create csv files for TimeFrame annotations in golds/timeframes


import re
import shutil
import csv
from pathlib import Path
import pandas as pd


# Set this to True if you want the TimeFrames to be sensitive to sublabels, with a
# sequence [S:D, S:H] you would get a TimeFrame of type S with the current setting,
# but two TimeFrames with labels S:D and S:H if you include the sublabel. Given the 
# way the current classifier is trained the former makes much more sense.
USE_SUBLABEL = False


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


def copy_timepoints(source, destination):
    # read in as dataframe to more easily manipulate columns
    df = pd.read_csv(source)
    df = amend_dataframe(df)
    # output to csv
    df.to_csv(destination, index=False)


def copy_timeframes(source, destination):
    # read in as dataframe to more easily manipulate columns
    df = pd.read_csv(source)
    df = amend_dataframe(df)
    current_label = None
    current_sublabel = None
    current_frame = []
    with open(destination, "w") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(get_column_names())
        for index, row in df.iterrows():
            ts = row['timestamp']
            label = row['type label']
            sublabel = row['subtype label']
            sublabel = '-' if type(sublabel) is float else sublabel
            modifier = row['modifier']
            if labels_match(current_label, label, current_sublabel, sublabel):
                current_frame.append((ts, label, sublabel))
            else:
                if current_frame and current_frame[0][1] != '-':
                    # this takes the modifier of the last timepoint
                    timeframe = create_timeframe(
                        current_frame, current_label, current_sublabel, modifier)
                    csv_writer.writerow(timeframe)
                current_frame = [(ts, label, sublabel)]
                current_label = label
                current_sublabel = sublabel


def amend_dataframe(df):
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
    df.loc[df['type label'].isna(), 'type label'] = '-'
    # remove first column (filename)
    df = df.drop('filename', axis=1)
    # remove transcript and note columns
    df = df.drop('transcript', axis=1)
    df = df.drop('note', axis=1)
    return df


def get_column_names():
    if USE_SUBLABEL:
        return ['start', 'end', 'type label', 'subtype label', 'modifier']
    return ['start', 'end', 'type label', 'modifier']


def labels_match(current_label, label, current_sublabel, sublabel):
    if USE_SUBLABEL:
        return current_label == label and current_sublabel == sublabel
    else:
        return current_label == label


def create_timeframe(frame, label, sublabel, modifier):
    sub = [sublabel] if USE_SUBLABEL else []
    return [frame[0][0], frame[-1][0], label] + sub + [modifier]



if __name__ == '__main__':

    folder = Path.cwd()
    goldpath = folder / 'golds'
    # iterate through files in scene-recognition
    # if a directory starts w/ yy-mm-dd pattern, copy contents to the golds directory
    for directory in folder.glob('*'):
        if directory.is_dir() and re.match("[0-9]{2}[0-1][0-9][0-3][0-9]", directory.name):
            # copy contents by iterating
            print(directory.name)
            for file in directory.glob('*'):
                print('   ', file.name)
                source = file
                destination_points = goldpath / 'timepoints' / file.name
                destination_frames = goldpath / 'timeframes' / file.name
                #copy_timepoints(source, destination_points)
                copy_timeframes(source, destination_frames)
