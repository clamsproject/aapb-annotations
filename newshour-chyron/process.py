"""
This script takes as input a directory containing VIA version 3 project files containing video annotations and
generates a CSV file with the following columns: video_filename, start_time, end_time, text
for each annotation in the project file.
"""
import csv
import json
import pathlib
import shutil
from collections import defaultdict as ddict
from pathlib import Path


def timeformat(sec_dot_ms):
    if isinstance(sec_dot_ms, str):
        s, ms = map(int, sec_dot_ms.split('.'))
    else:
        s, ms = divmod(sec_dot_ms, 1)
        s = int(s)
        ms = int(ms*1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f'{h:02d}:{m:02d}:{s:02d}.{ms:03d}'


def process(raw_dir, golds_dir):
    # Loop through each file in the input directory and process it
    csv_data = []
    for via_f in Path(raw_dir).glob('*'):
        if via_f.suffix == '.json':
            # Load the VIA project file
            data = json.load(open(via_f))

            # Loop through each annotation in the VIA project file, if it contains 2 z values, add it to a dictionary
            # with the key being the first z value and the value being the second z value
            z_dict = {}
            for annotation_id, annotation_data in data['metadata'].items():
                if 'z' in annotation_data and len(annotation_data['z']) == 2:
                    z_dict[annotation_data['z'][0]] = annotation_data['z'][1]

            # Loop through each annotation in the VIA project file, if it contains 1 z value, find the lowest key in the z_dict
            # that is less than the z value of the annotation if the value of that key is greater than the z value for the annotation
            # use the key as the start time and the value as the end time
            # add a row to the csv_data list with the video filename, start time, end time, and text
            for annotation_id, annotation_data in data['metadata'].items():
                # lookup video filename in data["file"] based on annotation_data[vid]
                video_filename = data["file"][annotation_data["vid"]]["fname"]
                if 'z' in annotation_data and len(annotation_data['z']) == 1:
                    z_value = annotation_data['z'][0]
                    start_time = max([key for key in z_dict.keys() if key < z_value])
                    end_time = z_dict[start_time]
                    if end_time > z_value:
                        try:
                            csv_data.append([video_filename, timeformat(start_time), timeformat(end_time), annotation_data['av']["text-boxes"]])
                        except KeyError as e:
                            print(e)
                            print(annotation_data)

    # Write the CSV file, text value may contain new lines
    guid_annotation_map = ddict(list)
    for row in csv_data:
        guid = row[0].replace('.mp4', '')
        guid_annotation_map[guid].append(row[1:])
    for guid, annotations in guid_annotation_map.items():
        annotations.sort()
        outf_path = (Path(golds_dir) / guid).with_suffix('.csv')
        with open(outf_path, 'a+', encoding='utf8') as f:
            writer = csv.writer(f)
            writer.writerow(['index', 'start', 'end', 'text-transcript'])
            for i, annotation in enumerate(annotations, 1):
                annotation[-1] = annotation[-1].replace('\n', '\\n')
                writer.writerow([i] + annotation)


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
