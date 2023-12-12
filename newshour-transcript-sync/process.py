"""Processes Slate annotation files

$ process.py --input_path /your/input/path --output_path /your/output/path

the input looks like this:
'''
1
00:02:05,570 --> 00:02:08,570
Good evening. I'm Jim Lehrer. On the NewsHour tonight coverage
'''

the output looks like this:
'''
index	starts	ends	content
1	00:02:05.570	00:02:08.570	Good evening. I'm Jim Lehrer. On the NewsHour tonight coverage
'''

"""
import argparse
import os
import pysrt


def srt_to_tsv(srt_filename, tsv_filename):
    subs = pysrt.open(srt_filename, encoding='utf-8')
    with open(tsv_filename, 'w', encoding='utf-8') as out:
        out.write("index\tstarts\tends\tcontent\n")
        # sub means subtitles
        for sub in subs:
            index = sub.index
            starts = str(sub.start).replace(',', '.')
            ends = str(sub.end).replace(',', '.')
            text_content = sub.text.replace('\n', ' ')
            out.write(f"{index}\t{starts}\t{ends}\t{text_content}\n")


def convert_directory(source_directory, destination_directory):
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    for filename in os.listdir(source_directory):
        if filename.endswith('.srt'):
            source_path = os.path.join(source_directory, filename)
            batchname = source_path.split(os.sep)[-2][7:]
            if not os.path.exists(os.path.join(destination_directory, batchname)):
                os.makedirs(os.path.join(destination_directory, batchname))
            dest_path = os.path.join(destination_directory, batchname, filename.replace('.srt', '.tsv'))
            srt_to_tsv(source_path, dest_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input_path', type=str, required=True,
                        help='Path to the directory containing the CLAMS newshour transcript sync annotated files')
    parser.add_argument('--output_path', type=str, required=True,
                        help='Path to the output .tsv file')
    args = parser.parse_args()
    convert_directory(args.input_path, args.output_path)
    print("Processing complete.")
