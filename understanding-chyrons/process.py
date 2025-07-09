import json
import pathlib
import shutil
from collections import defaultdict


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
    js_files = list(raw_dir.glob('*.json'))
    # check if there are more js files, which indicates a trouble 
    if len(js_files) > 1:
        raise ValueError(f"More than one json file found in {raw_dir}")
    js_file = js_files[0]
    with open(js_file, 'r') as f:
        annotations = json.loads("".join(f.read()))
        reformatted = defaultdict(list)  # GUID to list of annotations dict
        skip = 0
        dupe = 0
        unseen = 0
        irrel = 0
        for annotation in annotations:
            ann = {}
            filename, seen, type_label, subtype_label, modifier, note_3, note_4 = annotation
            if seen in ('false', 'False'):
                unseen += 1
                continue
            if type_label not in 'INY':
                irrel += 1
                continue
            if note_4.startswith('DUPE'):
                if not str(raw_dir).endswith('practice'):
                    print(annotation)
                dupe += 1
                continue
            note_4_data = note_4.split('\n\n')
            if len(note_4_data) < 2:
                # in the minimum case, note4 should be written-name and normal-name (without any attribute lines)
                if type_label == 'I':
                    print(annotation)
                    skip += 1
                # still keep the record since note3 annotation is still valid and usable
                note_4_structured = None
            else:
                note_4_structured = {
                    'name-as-written': note_4_data[0],
                    'name-normalized': note_4_data[1],
                    'attributes': note_4_data[2:]
                }
            guid = filename.split('_')[0]
            ann['at'] = format_timecode(filename)
            ann['scene-type'] = '-' if not type_label else type_label
            ann['scene-subtype'] = subtype_label
            ann['transitional'] = bool(modifier)
            ann['text-transcript'] = note_3.replace(r'\n', '\n')
            ann['text-transcript'] = ann['text-transcript'].replace(r'\"', '"')
            ann['keyed-information'] = note_4_structured
            reformatted[guid].append(ann)
        print(f'from {raw_dir.name}, skipped {skip} records due to malformed note-4 data')
        print(f'from {raw_dir.name}, skipped {dupe} records due to DUPE mark')
        print(f'from {raw_dir.name}, skipped {unseen} records due to unseen mark')
        print(f'from {raw_dir.name}, skipped {irrel} records with irrelevant type label (not I, N, Y)')
        for guid, anns in reformatted.items():
            with open(golds_dir / f'{guid}.json', 'w') as f:
                json.dump(anns, f, indent=2)


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
