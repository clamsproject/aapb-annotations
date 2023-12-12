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


def srt_to_tsv(srt_filename, tsv_filename):
    subs = pysrt.open(srt_filename, encoding='utf-8')
    with open(tsv_filename, 'w', encoding='utf-8') as out:
        out.write("index\tstart\tend\tcontent\n")
        # sub means subtitles
        for sub in subs:
            index = sub.index
            start = str(sub.start).replace(',', '.')
            end = str(sub.end).replace(',', '.')
            text_content = sub.text.replace('\n', ' ')
            out.write(f"{index}\t{start}\t{end}\t{text_content}\n")


def convert_directory(source_directory, destination_directory):
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    for filename in os.listdir(source_directory):
        if filename.endswith('.srt'):
            source_path = os.path.join(source_directory, filename)
            dest_path = os.path.join(destination_directory, filename.replace('.srt', '.tsv'))
            srt_to_tsv(source_path, dest_path)


if __name__ == '__main__':
    root_dir = pathlib.Path(__file__).parent
    for batch_dir in root_dir.glob('*'):
        if batch_dir.is_dir() and len(batch_dir.name) > 7 and batch_dir.name[6] == '-' and all([c.isdigit() for c in batch_dir.name[:6]]):
            print(f'Processing {batch_dir.name}...')
            convert_directory(batch_dir.name, root_dir / 'golds')
    print("Processing complete.")
