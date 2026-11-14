"""
Creates the gold files of the spoken-lid project from a data drop.

    python3 process.py

Reads every data drop (`YYMMDD-batchName` directory) next to this script and
writes one file per GUID to a fresh `golds/` directory. Clips that need a
manual check are reported on stderr. See README.md for the formats and the
label rules.
"""
import csv
import re
import shutil
import sys
from pathlib import Path

TASK_DIR = Path(__file__).parent
GOLDS_DIR = TASK_DIR / 'golds'
LABEL_FIELD = 'scene-label'
ORDER_FIELD = 'language-order'

# raw labels (lowercased) to gold language labels
LANGUAGES = {
    'central alaskan yupik': 'Central Alaskan Yupik',
    'central yupik': 'Central Alaskan Yupik',
    'esu': 'Central Alaskan Yupik',
    'non-central alaskan yupik': 'Non-Central Alaskan Yupik',
    'samoan': 'Samoan',
    'smo': 'Samoan',
    'spanish': 'Spanish',
    'english': 'English',
    'eng': 'English',
}
OTHER = {'other': 'Other'}
MIXED = 'Mixed'
NO_LABEL = 'No Label'
# the target language of each annotator, which a language order must include
TARGETS = {
    'a1': {'Central Alaskan Yupik', 'Non-Central Alaskan Yupik'},
    'a3': {'Spanish'},
    'a5': {'Samoan'},
}

# order texts: "A to B" or "A -> B", "A and B" or "A & B", and "A and B back
# and forth"
ORDER = re.compile(r'^(?P<a>[\w -]+?) (?:to|->|and|&) (?P<b>[\w -]+?)'
                   r'(?P<both> back and forth)?$')


def language_order(text):
    """
    :returns: `A>B` for a switch from A to B, `A<>B` for back and forth, or
        `None` when the whole text is not an order of two known languages
    """
    m = ORDER.match(text.strip().rstrip('.').strip().lower())
    if not m:
        return None
    a, b = LANGUAGES.get(m['a']), LANGUAGES.get(m['b'])
    if not (a and b):
        return None
    return f'{a}<>{b}' if m['both'] else f'{a}>{b}'


def gold_label(row):
    raw = row['label'].strip().lower()
    if raw in LANGUAGES:
        return LANGUAGES[raw]
    if raw in OTHER:
        return OTHER[raw]
    if raw == '':
        return NO_LABEL
    if raw == 'mixed':
        return MIXED
    raise ValueError(f'unknown label "{row["label"]}"')


def gold_order(row, label, problems):
    """
    :returns: the language order of a mixed clip, from `mixed-order`, or from
        `notes` when `mixed-order` is empty; empty when there is none
    """
    clip = f'clip {row["clip-set"]}/{row["clip"]}'
    field = row['mixed-order'].strip()
    from_field = language_order(field) if field else None
    from_notes = language_order(row['notes'])
    if field and from_field is None:
        problems.append(f'{clip}: unreadable mixed-order "{field}"')
    if from_field and from_notes and from_field != from_notes:
        problems.append(f'{clip}: mixed-order {from_field} and notes '
                        f'{from_notes} differ; mixed-order is used')
    order = from_field or from_notes
    if not order:
        return ''
    if label != MIXED:
        problems.append(f'{clip}: label {label} with order {order}; '
                        f'the order is left out')
        return ''
    target = TARGETS.get(row['annotator'], set())
    if target and not target & set(re.split('<>|>', order)):
        problems.append(f'{clip}: order {order} without the target language '
                        f'of {row["annotator"]}')
    return order


def timestamp(ms):
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f'{h:02d}:{m:02d}:{s:02d}.{ms:03d}'


def gold_frames(rows, problems):
    """
    :returns: `[start, end, label, order]` per clip in time order, in
        integer milliseconds, with each overlap between consecutive clips cut
        at its midpoint
    """
    frames = []
    for row in rows:
        label = gold_label(row)
        frames.append([int(row['start_ms']), int(row['end_ms']), label,
                       gold_order(row, label, problems)])
    frames.sort()
    for prev, cur in zip(frames, frames[1:]):
        if prev[1] > cur[0]:
            middle = round((prev[1] + cur[0]) / 2)
            prev[1] = cur[0] = middle
    return frames


def drop_files():
    """
    :returns: the CSV files of all data drops (`YYMMDD-batchName`
        directories next to this script)
    :raises SystemExit: if there are none, or a GUID is in two drops
    """
    files = {}
    for drop_dir in sorted(TASK_DIR.glob('[0-9]' * 6 + '-*')):
        for drop_file in sorted(drop_dir.glob('*.csv')):
            if drop_file.name in files:
                sys.exit(f'{drop_file.stem} is in two data drops: '
                         f'{files[drop_file.name].parent.name} and '
                         f'{drop_dir.name}')
            files[drop_file.name] = drop_file
    if not files:
        sys.exit(f'no data drop in {TASK_DIR}')
    return list(files.values())


def process():
    shutil.rmtree(GOLDS_DIR, ignore_errors=True)
    GOLDS_DIR.mkdir()
    files = drop_files()
    for drop_file in files:
        with open(drop_file, newline='') as f:
            rows = list(csv.DictReader(f))
        problems = []
        frames = gold_frames(rows, problems)
        with open(GOLDS_DIR / drop_file.name, 'w', newline='') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(['start', 'end', LABEL_FIELD, ORDER_FIELD])
            for start, end, label, order in frames:
                writer.writerow([timestamp(start), timestamp(end), label,
                                 order])
        for problem in problems:
            print(f'{drop_file.stem}: {problem}', file=sys.stderr)
    print(f'wrote {len(files)} gold files to {GOLDS_DIR}')


if __name__ == '__main__':
    process()
