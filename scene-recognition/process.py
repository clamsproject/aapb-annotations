import pathlib
import shutil
import collections

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
    label_freq = collections.Counter()
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
        df.loc[df['scene-subtype'].isna(), 'scene-subtype'] = ''
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
        # concat scene-type and scene-subtype into a single 'full' label and count them
        full_labels = df['scene-type'].astype(str) + df['scene-subtype'].astype(str)
        label_freq.update(full_labels.tolist())
    return label_freq


if __name__ == '__main__':
    task_dir = pathlib.Path(__file__).parent
    golds_dir = task_dir / 'golds'

    # delete golds directory if it exists
    shutil.rmtree(golds_dir, ignore_errors=True)
    # then start from clean slate
    golds_dir.mkdir(exist_ok=True)

    # find all directories starts with six digits and a dash
    label_dist = {}
    for batch_dir in task_dir.glob('[0-9][0-9][0-9][0-9][0-9][0-9]-*'):
        if batch_dir.is_dir():
            label_dist[batch_dir.name] = process(batch_dir, golds_dir)
    # plot label distribution to png, must do two plots, one for "full" labels 
    # and one for "short" labels (first letter of each label)
    # also include negative labels (`"-"`)
    import matplotlib.pyplot as plt
    import seaborn as sns
    for batch, freq in label_dist.items():
        # create a figure with two subplots side by side
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        # sort the frequency dictionary by keys
        freq = dict(sorted(freq.items()))
        # plot full labels
        sns.barplot(x=list(freq.keys()), y=list(freq.values()), ax=axes[0])
        axes[0].set_title(f'Full Label Distribution for {batch}')
        axes[0].set_xlabel('Labels')
        axes[0].set_ylabel('Frequency')
        axes[0].tick_params(axis='x', rotation=45)

        # plot short labels (first letter of each label)
        # merge all labels into their first letter
        short_freq = collections.Counter()
        for label, count in freq.items():
            short_label = label[0] 
            short_freq[short_label] += count
        sns.barplot(x=list(short_freq.keys()), y=list(short_freq.values()), ax=axes[1])
        axes[1].set_title(f'Short Label Distribution for {batch}')
        axes[1].set_xlabel('Short Labels')
        axes[1].set_ylabel('Frequency')
        axes[1].tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.savefig(task_dir / f'{batch}-labels.png')
        plt.close()
    # Combine all label frequencies across batches
    total_freq = collections.Counter()
    for freq in label_dist.values():
        total_freq.update(freq)

    # Create a figure with two subplots side by side for all batches combined
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # Plot full labels
    total_freq = dict(sorted(total_freq.items()))
    sns.barplot(x=list(total_freq.keys()), y=list(total_freq.values()), ax=axes[0])
    axes[0].set_title('Full Label Distribution for All Batches')
    axes[0].set_xlabel('Labels')
    axes[0].set_ylabel('Frequency')
    axes[0].tick_params(axis='x', rotation=45)  
    # Plot short labels (first letter of each label)
    short_total_freq = collections.Counter()
    for label, count in total_freq.items():
        short_label = label[0] 
        short_total_freq[short_label] += count
    sns.barplot(x=list(short_total_freq.keys()), y=list(short_total_freq.values()), ax=axes[1])
    axes[1].set_title('Short Label Distribution for All Batches')
    axes[1].set_xlabel('Short Labels')
    axes[1].set_ylabel('Frequency')
    axes[1].tick_params(axis='x', rotation=45) 
    plt.tight_layout()
    plt.savefig(task_dir / 'all-batches-labels.png')
    plt.close()
