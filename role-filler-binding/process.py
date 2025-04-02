import csv
import json
import pathlib
import shutil
from mmif.utils import timeunit_helper as tuh

from typing import Dict, Tuple

FPS = 29.97  # we know all videos in aapb-ann-44 batch are encoded with 29.97 fps. For a future (very unlikley) event of adding more batches to this RFB work, this might need to be double-checked


def build_csv_string(annos: Dict) -> Tuple[bool, str]:
    pruned_annos = {k: v for k, v in annos.items() if k and k[0] != "_" and v}
    is_skipped = False

    out = "|".join(
        [
            f"{role}={filler}"
            for role, fillers in pruned_annos.items()
            for filler in fillers
        ]
    )
    if out == "":
        for role, fillers in annos.items():
            if role == "_skip_reason":
                out += fillers
                is_skipped = True

    return is_skipped, out


def process(raw_dir, golds_dir):
    swt_type_dict = {
        '231117': 'credits'
    }
    swt_type = swt_type_dict[raw_dir.name.split('-')[0]]
    for fname in raw_dir.glob('*.json'):
        annotations = json.load(open(fname, "r", encoding='utf-8'))
        out = []
        for frame, annotation in annotations.items():
            timecode = tuh._second_to_isoformat(int(frame) / FPS)
            csv_line = (
                timecode,
                swt_type,
                *build_csv_string(annotation)
            )
            out.append(csv_line)
        outfname = golds_dir / fname.with_suffix('.csv').name
        with open(outfname, "w", encoding='utf-8') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(["at", "scene-type", "skipped", "role-fillers"])
            writer.writerows(out)


if __name__ == '__main__':
    task_dir = pathlib.Path(__file__).parent
    golds_dir = task_dir / 'golds'

    # delete golds directory if it exists
    shutil.rmtree(golds_dir, ignore_errors=True)
    # then start from clean slate
    golds_dir.mkdir(exist_ok=True)

    # find all directories starts with six digits and a dash
    for batch_dir in task_dir.glob('[0-9][0-9][0-9][0-9][0-9][0-9]-*'):
        process(batch_dir, golds_dir)
