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
'''

"""
import os
import pathlib
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
        out.write("index\tstart\tend\tcontent\n")
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


def convert_directory(source_directory, destination_directory, gold_transcript_directory):
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    for filename in os.listdir(source_directory):
        if filename.endswith('.srt'):
            gold_transcript_path = filename.split(".")[0]+"-transcript.txt"
            if gold_transcript_path in os.listdir(gold_transcript_directory):
                source_path = os.path.join(source_directory, filename)
                gold_transcript_path = os.path.join(gold_transcript_directory, gold_transcript_path)
                dest_path = os.path.join(destination_directory, filename.replace('.srt', '.tsv'))
                srt_to_tsv(source_path, gold_transcript_path, dest_path)
            else:
                print(filename, "has no corresponding gold transcript in", gold_transcript_directory)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--gold_txt_dir', required=True,
                            help='the directory to the gold transcripts which should be txt files.')
    parsed_args = arg_parser.parse_args()
    root_dir = pathlib.Path(__file__).parent
    for batch_dir in root_dir.glob('*'):
        if batch_dir.is_dir() and len(batch_dir.name) > 7 and batch_dir.name[6] == '-' and all([c.isdigit() for c in batch_dir.name[:6]]):
            print(f'Processing {batch_dir.name}...')
            convert_directory(batch_dir.name, root_dir / 'golds', parsed_args.gold_txt_dir)
    print("Processing complete.")
