"""
Script to generate speaker diarization gold data by combining:
1. Time-sync annotations (TSV files with timestamps + character offsets)
2. Gold transcripts with speaker markers

Input: Time-sync gold TSV (from newshour-transcript-sync/golds/*.tsv)
    start           end             alignment-start alignment-end
    00:01:39.150    00:01:42.530    0               82
    00:01:42.540    00:01:46.780    83              152

Input: Gold transcript (from aapb-collaboration/21/*-transcript.txt)
    ROBERT MacNEIL: Good evening. Here are the top news headlines...
    JUDY WOODRUFF: We focus most of the NewsHour tonight...

Output: Speaker diarization TSV
    start           end             speaker-id
    00:01:39.150    00:01:42.530    ROBERT_MacNEIL
    00:01:42.540    00:01:46.780    JUDY_WOODRUFF

Requires: clams-utils package (pip install -e path/to/clams-utils)
"""
import argparse
import csv
import pathlib
import shutil
import sys
from typing import List, Tuple

# Add clams-utils to path if not installed as package
_CLAMS_UTILS_PATH = pathlib.Path(__file__).parent.parent.parent / 'clams-utils'
if _CLAMS_UTILS_PATH.exists():
    sys.path.insert(0, str(_CLAMS_UTILS_PATH))

from clams_utils.aapb.newshour_transcript_cleanup import (
    extract_speaker_spans,
    split_by_speakers,
)


def parse_time(time_str: str) -> float:
    """
    Parse ISO 8601 time string (hh:mm:ss.mmm) to seconds.

    :param time_str: Time string in format "hh:mm:ss.mmm"
    :returns: Time in seconds as float
    """
    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds


def format_time(seconds: float) -> str:
    """
    Format seconds to ISO 8601 time string (hh:mm:ss.mmm).

    :param seconds: Time in seconds
    :returns: Time string in format "hh:mm:ss.mmm"
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


def read_time_sync_tsv(tsv_path: pathlib.Path) -> List[Tuple[str, str, int, int]]:
    """
    Read time-sync TSV file.

    :param tsv_path: Path to TSV file
    :returns: List of (start_time, end_time, char_start, char_end) tuples
    """
    rows = []
    with open(tsv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            start = row['start']
            end = row['end']
            # Handle empty or missing alignment values
            char_start_str = row.get('alignment-start', '').strip()
            char_end_str = row.get('alignment-end', '').strip()
            if not char_start_str or not char_end_str:
                continue
            char_start = int(char_start_str)
            char_end = int(char_end_str)
            rows.append((start, end, char_start, char_end))
    return rows


def process_slice_majority(
    speaker_spans: List[Tuple[str, int, int]],
    char_start: int,
    char_end: int
) -> str:
    """
    Return speaker with most characters in the given range.

    :param speaker_spans: List of (speaker_id, span_start, span_end) from extract_speaker_spans
    :param char_start: Start character offset
    :param char_end: End character offset
    :returns: Speaker ID with majority of characters, or empty string if no overlap
    """
    splits = split_by_speakers(speaker_spans, char_start, char_end)

    if not splits:
        return ""

    # Count characters per speaker
    speaker_chars = {}
    for speaker_id, overlap_start, overlap_end in splits:
        char_count = overlap_end - overlap_start
        speaker_chars[speaker_id] = speaker_chars.get(speaker_id, 0) + char_count

    # Return speaker with most characters
    return max(speaker_chars, key=speaker_chars.get)


def process_slice_split(
    speaker_spans: List[Tuple[str, int, int]],
    char_start: int,
    char_end: int,
    time_start: str,
    time_end: str
) -> List[Tuple[str, str, str]]:
    """
    Split time slice proportionally by speaker character counts.

    Assumes uniform speaking rate within the time slice.

    :param speaker_spans: List of (speaker_id, span_start, span_end) from extract_speaker_spans
    :param char_start: Start character offset
    :param char_end: End character offset
    :param time_start: Start time string (hh:mm:ss.mmm)
    :param time_end: End time string (hh:mm:ss.mmm)
    :returns: List of (start_time, end_time, speaker_id) tuples
    """
    splits = split_by_speakers(speaker_spans, char_start, char_end)

    if not splits:
        return []

    if len(splits) == 1:
        # Only one speaker in this range
        return [(time_start, time_end, splits[0][0])]

    # Multiple speakers: split time proportionally
    total_chars = char_end - char_start
    if total_chars <= 0:
        return [(time_start, time_end, splits[0][0])]

    start_seconds = parse_time(time_start)
    end_seconds = parse_time(time_end)
    duration = end_seconds - start_seconds

    results = []
    current_time = start_seconds

    for i, (speaker_id, overlap_start, overlap_end) in enumerate(overlaps):
        speaker_chars = overlap_end - overlap_start
        speaker_duration = (speaker_chars / total_chars) * duration

        speaker_start_time = format_time(current_time)
        current_time += speaker_duration
        # For last speaker, use exact end time to avoid floating point issues
        if i == len(overlaps) - 1:
            speaker_end_time = time_end
        else:
            speaker_end_time = format_time(current_time)

        results.append((speaker_start_time, speaker_end_time, speaker_id))

    return results


def process_file(
    time_sync_tsv: pathlib.Path,
    transcript_path: pathlib.Path,
    output_path: pathlib.Path,
    strategy: str
) -> bool:
    """
    Process a single file pair to generate speaker diarization gold data.

    :param time_sync_tsv: Path to time-sync TSV file
    :param transcript_path: Path to gold transcript file
    :param output_path: Path to output TSV file
    :param strategy: Either "majority" or "split"
    :returns: True if processing succeeded, False otherwise
    """
    # Read transcript and extract speaker spans
    with open(transcript_path, 'r', encoding='utf-8') as f:
        transcript_text = f.read()

    speaker_spans = extract_speaker_spans(transcript_text)
    if not speaker_spans:
        print(f"Warning: No speaker spans found in {transcript_path}")
        return False

    # Read time-sync TSV
    time_sync_rows = read_time_sync_tsv(time_sync_tsv)
    if not time_sync_rows:
        print(f"Warning: No valid rows in {time_sync_tsv}")
        return False

    # Generate output rows
    output_rows = []

    for start_time, end_time, char_start, char_end in time_sync_rows:
        if strategy == "majority":
            speaker_id = process_slice_majority(speaker_spans, char_start, char_end)
            if speaker_id:
                output_rows.append((start_time, end_time, speaker_id))
        else:  # split
            split_rows = process_slice_split(
                speaker_spans, char_start, char_end, start_time, end_time
            )
            for row_start, row_end, speaker_id in split_rows:
                output_rows.append((row_start, row_end, speaker_id))

    # Write output TSV
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        f.write("start\tend\tlabel\n")
        for start, end, speaker_id in output_rows:
            f.write(f"{start}\t{end}\t{speaker_id}\n")

    return True


def process_all(
    gold_tsv_dir: pathlib.Path,
    gold_transcript_dir: pathlib.Path,
    output_dir: pathlib.Path,
    strategy: str
):
    """
    Process all matching file pairs.

    :param gold_tsv_dir: Directory containing time-sync TSV files
    :param gold_transcript_dir: Directory containing gold transcript files
    :param output_dir: Directory to write output TSV files
    :param strategy: Either "majority" or "split"
    """
    tsv_files = list(gold_tsv_dir.glob('*.tsv'))
    processed = 0
    skipped = 0

    for tsv_path in tsv_files:
        # Extract GUID from filename (e.g., cpb-aacip-507-154dn40c26.tsv)
        guid = tsv_path.stem

        # Find corresponding transcript
        transcript_path = gold_transcript_dir / f"{guid}-transcript.txt"

        if not transcript_path.exists():
            print(f"Skipping {guid}: no transcript at {transcript_path}")
            skipped += 1
            continue

        output_path = output_dir / f"{guid}.tsv"

        if process_file(tsv_path, transcript_path, output_path, strategy):
            processed += 1
        else:
            skipped += 1

    print(f"Processed {processed} files, skipped {skipped}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate speaker diarization gold data from time-sync annotations and gold transcripts.'
    )
    parser.add_argument(
        '--gold-tsv-dir',
        required=True,
        help='Directory containing time-sync TSV files (e.g., ../newshour-transcript-sync/golds)'
    )
    parser.add_argument(
        '--gold-transcript-dir',
        required=True,
        help='Directory containing gold transcript files (e.g., /path/to/aapb-collaboration/21)'
    )
    parser.add_argument(
        '--output-dir',
        default='./golds',
        help='Directory to write output TSV files (default: ./golds)'
    )
    parser.add_argument(
        '--strategy',
        choices=['majority', 'split'],
        default='majority',
        help='Strategy for handling time slices with multiple speakers: '
             '"majority" assigns entire slice to dominant speaker, '
             '"split" divides time proportionally (default: majority)'
    )

    args = parser.parse_args()

    gold_tsv_dir = pathlib.Path(args.gold_tsv_dir)
    gold_transcript_dir = pathlib.Path(args.gold_transcript_dir)
    output_dir = pathlib.Path(args.output_dir)

    if not gold_tsv_dir.is_dir():
        parser.error(f"Gold TSV directory does not exist: {gold_tsv_dir}")

    if not gold_transcript_dir.is_dir():
        parser.error(f"Gold transcript directory does not exist: {gold_transcript_dir}")

    # Clean and recreate output directory
    shutil.rmtree(output_dir, ignore_errors=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    process_all(gold_tsv_dir, gold_transcript_dir, output_dir, args.strategy)
