"""Processing NER uploads.

NER annotation for this project is done with Brat tool and the output format is 
Brat standalone `ann` format. We will use thr ann format as the gold format as
well. Thus processing these "raw" into golds files is simply just copying files.
"""
import pathlib
import shutil

if __name__ == '__main__':
    root_dir = pathlib.Path(__file__).parent
    golds_dir = root_dir / 'golds'
    golds_dir.mkdir(exist_ok=True)
    for batch_dir in root_dir.glob('*'):
        if batch_dir.is_dir() and len(batch_dir.name) > 7 and batch_dir.name[6] == '-' and all([c.isdigit() for c in batch_dir.name[:6]]):
            for ann in batch_dir.glob('*.ann'):
                shutil.copy(ann, golds_dir)
