"""Processing NER uploads.

Creates MMIF or CoNNL files from the Brat annotation files.

$ process.py [-h] [--export] PROJECT_DIR

Takes all  annotations file in the 'PROJECT_DIR/annotations' directory and
copy them to the working directory.

With the --export option the results are then copied to the "gold" directory at
the toplevel of this repository, where they are ready to be committed back into
the annotation collection repository and pushed up. The script does not do the
automatic commit and push in order to avoid hasty commits.

"""

from pathlib import Path
import shutil
import argparse


ANNOTATIONS_DIR = Path('./annotations')
WORKING_DIR = Path('./working')


def parse_arguments():
    ap = argparse.ArgumentParser(
        description='Process uploaded NEL annotation files with named entitie links')
    ap.add_argument('batch', help='Batch to process files for')
    ap.add_argument('--export', default=False, action='store_true',
                    help='Export results to the gold directory')
    return ap.parse_args()


if __name__ == '__main__':

    options = parse_arguments()

    batch_dir = Path(options.batch).resolve()
    annotations_dir = batch_dir / 'annotations'
    working_dir = batch_dir / 'working'
    working_dir.mkdir(exist_ok=True)

    # this is overkill because we do not even change the file, but we may do
    # that in the future
    print(f'>>> Copying files...')
    print(f'>>> {annotations_dir}')
    print(f'>>> --> {working_dir}')
    for tab_file in annotations_dir.glob('*.tab'):
        shutil.copy(str(tab_file), working_dir)

    if options.export:
        batch = Path(options.batch).resolve().name
        repo_dir = (Path(__file__).parent / '..' / '..').resolve()
        gold_dir = repo_dir / 'golds' / 'nel' / batch
        gold_dir.mkdir(parents=True, exist_ok=True)
        print(f'>>> Exporting {batch} annotations to the gold directory')
        print(f'>>> --> {gold_dir}')
        for tab_file in working_dir.glob('*.tab'):
            shutil.copy(str(tab_file), gold_dir)
