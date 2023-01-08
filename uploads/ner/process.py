"""Processing NER uploads.

Creates MMIF or CoNNL files from the Brat annotation files.

$ process.py [-h] [--format (mmif|connl)] [--export] PROJECT_DIR

Takes all Brat annotations file in the 'PROJECT_DIR/annotations' directory and
write all results to the "PROJECT_DIR/working" directory. The script generates
.mmif files (the default) or .conll.tsv files. If the format is "connl" then the
working directory needs to include the text files, which for copyright reasons
cannot be included in this repository.

With the --export option the results are copied to the "gold" directory at the
toplevel of this repository, where they are ready to be commited back into the
annotation collection repository and pushedcup. The script does not do automatic
commits and pushes in order to avoid hasty commits.

Other python scripts in this directory were copied from the brat repository at
https://github.com/nlplab/brat/tree/44ecd825810167eed2a5d8ad875d832218e734e8.

Requirements:

$ pip install mmif-python
$ pip install jsonschema
$ pip install lapps

The latter two are because they are not defined as a dependency for the former.

"""

import sys
from pathlib import Path
import shutil
import argparse

from mmif import Mmif, DocumentTypes
from mmif import __specver__ as mmif_version
from lapps.discriminators import Uri

import anntoconll


ANNOTATIONS_DIR = Path('./annotations')
WORKING_DIR = Path('./working')


def parse_arguments():
    ap = argparse.ArgumentParser(
        description='Convert uploaded Brat annotation files with named entities')
    ap.add_argument('project', help='Project to convert files for')
    ap.add_argument('--format', default="mmif",
                    help='Desired output format: "mmif" (default) or "connl"')
    ap.add_argument('--export', default=False, action='store_true',
                    help='Export results to the gold directory')
    return ap.parse_args()


def convert_into_mmif(annotations_dir: Path, working_dir: Path):
    for ann in annotations_dir.glob('*.ann'):
        create_mmif(ann, working_dir)


def convert_into_connl(annotations_dir: Path, working_dir: Path):
    for ann in annotations_dir.glob('*.ann'):
        shutil.copy(ann, working_dir)
    anntoconll.options = argparse.Namespace(**{
        'singleclass': False,
        'nosplit': False,
        'annsuffix': '.ann',
        'outsuffix': '.conll.tsv',
        'text': working_dir.glob('*.txt'),
        })
    anntoconll.process_files(anntoconll.options.text)


def mmif_template(document_id: str, transcript: str) -> Mmif:
    """Create an empty MMIF object with just the document."""
    return Mmif(
        { "documents": [
            { "@type": str(DocumentTypes.TextDocument),
              "properties": {
                  "id": document_id,
                  "mime": "text/plain",
                  "location": transcript }} ],
          "views": [],
          "metadata": {
              "mmif": f"http://mmif.clams.ai/{mmif_version}" }})


def create_mmif(annotation_file: Path, output_dir: Path):
    """Create a MMIF file from the Brat annotation file."""
    document_id = 'd1'
    # TODO: figure out what the exact location is
    file_location = f'file:///var/archive/{annotation_file}'
    mmif = mmif_template(document_id, file_location)
    view = mmif.new_view()
    view.new_contain(Uri.NE)
    with annotation_file.open() as fh:
        for line in fh:
            (identifier, annotation, text) = line.strip().split('\t')
            category, start, end = annotation.split()
            a = view.new_annotation(Uri.NE, identifier, document=document_id,
                                    start=int(start), end=int(end), text=text)
    # extract the file name but change the extension
    file_name = annotation_file.parts[-1][:-3] + 'mmif'
    with open(output_dir / file_name, 'w') as fh_out:
        fh_out.write(mmif.serialize(pretty=True))


if __name__ == '__main__':

    options = parse_arguments()

    project_dir = Path(options.project).resolve()
    annotations_dir = project_dir / 'annotations'
    working_dir = project_dir / 'working'
    working_dir.mkdir(exist_ok=True)

    print(f'>>> Converting files into the {options.format.upper()} format')
    print(f'>>> {annotations_dir}')
    print(f'>>> --> {working_dir}')
    if options.format == 'mmif':
        convert_into_mmif(annotations_dir, working_dir)
    elif options.format == 'connl':
        convert_into_connl(annotations_dir, working_dir)

    if options.export:
        proj_name = Path(options.project).resolve().name
        repo_dir = (Path(__file__).parent / '..' / '..').resolve()
        gold_dir = repo_dir / 'golds' / 'ner' / proj_name
        gold_dir.mkdir(parents=True, exist_ok=True)
        print(f'>>> Exporting {proj_name} annotations to the gold directory')
        print(f'>>> --> {gold_dir}')
        if options.format == 'connl':
            for tsv_file in working_dir.glob('*.conll.tsv'):
                shutil.copy(str(tsv_file), gold_dir)
        if options.format == 'mmif':
            for mmif_file in working_dir.glob('*.mmif'):
                shutil.copy(str(mmif_file), gold_dir)
