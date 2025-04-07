"""
Script to convert CADET-based subtitle/caption timing sync annotation (in srt format)
into a more machine-friendly tsv files.

the input looks like this:
'''
1
00:02:05,570 --> 00:02:08,570
Good evening. I'm Jim Lehrer. On the NewsHour tonight coverage
'''

the output looks like this:
'''
index	start	end	content
1	00:02:05.570	00:02:08.570	Good evening. I'm Jim Lehrer. On the NewsHour tonight coverage

In doing so, the script also replaces the underlying text in the CADET srt files with the gold transcript text.
'''


"""
import pathlib
import shutil

import pysrt
import difflib
import argparse
from clams_utils.aapb.newshour_transcript_cleanup import clean


def get_tokens_aligned(non_gold:str, gold:str):
    """
    Given the non-gold transcript text and the gold transcript text,
    return their token-to-token mappings.
    """
    tokens1 = non_gold.strip().split()
    tokens2 = clean("\n"+gold.strip()).strip().split()
    sequence_matcher = difflib.SequenceMatcher(None, tokens1, tokens2)
    mappings = {}

    for tag, i1, i2, j1, j2 in sequence_matcher.get_opcodes():
        if tag == "equal":
            for i in range(0, i2-i1):
                mappings.update({int(i1+i): {'srt': tokens1[i1+i:i1+i+1][0], 'txt': tokens2[j1+i:j1+i+1][0]}})
        elif tag == "delete" and i2-i1 > 10:
            # the current version of clams_utils.aapb.newshour_transcript_cleanup.py uses regex to remove keywords
            # Regex can make mistakes, so sometimes the cleaner can remove a whole sentence/paragraph
            # this step saves the text in non_gold with more than 10 tokens whose corresponding text in gold is
            # mistakenly deleted by regex (this does not 100% save the mistake but at least helps)
            for i in range(0, i2-i1):
                mappings.update({int(i1+i): {'srt': tokens1[i1+i:i1+i+1][0], 'txt': tokens1[i1+i:i1+i+1][0]}})
        else:
            mappings.update({int(i1): {'srt': " ".join(tokens1[i1:i2]), 'txt': " ".join(tokens2[j1:j2])}})

    return mappings


def srt_to_tsv(srt_filename, gold_transcript_filename, tsv_filename):
    """
    Given a srt file and its corresponding gold transcript file,
    replace the srt text with the gold transcript corresponding texts
    and output it to the given tsv file.
    """
    subs = pysrt.open(srt_filename, encoding='utf-8')
    non_gold = ""
    for sub in subs:
        non_gold += sub.text.replace('\n', ' ') + " "
    with open(gold_transcript_filename, 'r') as f:
        gold = f.read()

    mappings = get_tokens_aligned(non_gold, gold)
    prev_length = 0
    current_length = 0

    with open(tsv_filename, 'w', encoding='utf-8') as out:
        out.write("index\tstart\tend\tspeech-transcript\n")
        # sub means subtitles
        for sub in subs:
            index = sub.index
            start = str(sub.start).replace(',', '.')
            end = str(sub.end).replace(',', '.')
            replaced_line = ""
            current_length += len(sub.text.replace('\n', ' ').split())
            for i in range(prev_length, current_length):
                try:
                    replaced_line += mappings[i]['txt'] + " "
                except KeyError:
                    replaced_line += " "
            text_content = replaced_line
            prev_length = current_length

            out.write(f"{index}\t{start}\t{end}\t{text_content}\n")


def process(source_directory, destination_directory, gold_transcript_directory):
    for source_path in source_directory.glob('*.srt'):
        gold_transcript_path = source_path.name.split(".")[0]+"-transcript.txt"
        gold_txt_path = gold_transcript_directory / gold_transcript_path
        if gold_txt_path.exists():
            dest_path = destination_directory / source_path.with_suffix('.tsv').name
            srt_to_tsv(source_path, gold_txt_path, dest_path)
        else:
            print(source_path, "has no corresponding gold transcript in", gold_transcript_directory)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--gold-txt-dir', required=True,
                            help='the directory to the gold transcripts which should be txt files.')
    parsed_args = arg_parser.parse_args()
    
    task_dir = pathlib.Path(__file__).parent
    golds_dir = task_dir / 'golds'

    # delete golds directory if it exists
    shutil.rmtree(golds_dir, ignore_errors=True)
    # then start from clean slate
    golds_dir.mkdir(exist_ok=True)

    # find all directories starts with six digits and a dash
    for batch_dir in task_dir.glob('[0-9][0-9][0-9][0-9][0-9][0-9]-*'):
        process(batch_dir, golds_dir, pathlib.Path(parsed_args.gold_txt_dir))

