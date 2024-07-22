#!/usr/bin/env python3

# ====================================|
# Imports
# ====================================|
import csv
import json
import os
import sys

from typing import Dict, List, Union, Tuple
from clams_utils.aapb import guidhandler

# ====================================|

def build_csv_string(annos: Dict) -> Tuple[bool, str]:
    """Convert a dictionary to a csv string.
    this is done mainly for portability
    ### params
    + annos := dictionary of Role/Filler pairs
    ### returns
    + indicates if the annotation was skipped
    + raw CSV string
    """
    pruned_annos = {k: v for k, v in annos.items() if k and k[0] != "_" and v}
    is_skipped = False

    out = "\n".join(
        [
            f",{role},{filler}"
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

def process_golds(fname: Union[str, os.PathLike]) -> List[Tuple[str, str, bool, str]]:
    """Process a directory of gold files
    ### params
    + fname := input raw annotation file name
    ### returns
    a list of tuples, each representing a line of the csv
    """
    out = []
    with open(fname, "r", encoding='utf-8') as f:
        fp_golds = json.load(f)
        for frame, annotations in fp_golds.items():
            guid = guidhandler.get_aapb_guid_from(annotations['_image_id'])
            csv_line = (
                guid,
                frame,
                build_csv_string(annotations)[0],
                build_csv_string(annotations)[1],
            )
            out.append(csv_line)
    return out


def write_csv(csvs: List[Tuple[str, str, str]], outfname: Union[str, os.PathLike]):
    """Write csv lines to file

    ### params
    + csvs := list of tuples that represent csv lines
    + outfname := name of output .csv file
    ### returns
    void
    """
    with open(outfname, "w", encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(["GUID", "FRAME", "SKIPPED", "ANNOTATIONS"])
        writer.writerows(csvs)


def main():
    """Main function for processing gold annotations
    """
    source_gold_anns_dir = sys.argv[1]
    out_dir = 'golds'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for root, _, anns in os.walk(source_gold_anns_dir):
        for ann in anns:
            write_csv(process_golds(os.path.join(root, ann)),
                        os.path.join(out_dir, guidhandler.get_aapb_guid_from(ann) + "-gold.csv")
                        )

if __name__ == "__main__":
    main()
