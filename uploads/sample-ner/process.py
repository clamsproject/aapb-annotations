"""process.py for the sample NE annotation work

Run this script with a directory name where raw txt files are placed, passed as an argument. 
The script will copy ann files to the txt directory and generate conll.tsv files there. 
After tsv files are generated, they are copied back to `golds` directory to be ready 
for being pushed back to annotation collection repository. 
Note that the script does not automatically do the "git push". That has to be manually done.

Other python scripts in this directory are copied from brat repository. 
https://github.com/nlplab/brat/tree/44ecd825810167eed2a5d8ad875d832218e734e8
"""
import anntoconll
import sys
import pathlib
import shutil
import argparse


if len(sys.argv) < 2:
    sys.stderr.write(__doc__)
    sys.exit(1)
out_dir = pathlib.Path(sys.argv[1]).expanduser()

for ann in pathlib.Path('./annotations').glob('*.ann'):
    shutil.copy(ann, out_dir)

options = argparse.Namespace(**{
    'singleclass': False,
    'nosplit': False,
    'annsuffix': '.ann',
    'outsuffix': '.conll.tsv',
    'text': out_dir.glob('*.txt'),
    })
anntoconll.options = options

anntoconll.process_files(options.text)

proj_name = (pathlib.Path(__file__) / '..').resolve().name
gold_dir = (pathlib.Path(__file__).parent / '..' / '..' / 'golds' / proj_name).resolve()
gold_dir.mkdir(parents=True, exist_ok=True)
for tsv in out_dir.glob('*.conll.tsv'):
    shutil.move(tsv, gold_dir)

