#!/usr/bin/env python3

# ====================================|
# Imports
# ====================================|
import csv
import json
import os
import sys


from typing import Dict, List, Union, Tuple

# ====================================|


def process_golds(fname: Union[str, os.PathLike]) -> List[Tuple[str, str, str]]:
    """Process a directory of gold files
    ### params
    + fname := input directory name
    ### returns
    a list of tuples, each representing a line of the csv
    """
    out = []
    for root, direcs, files in os.walk(fname):
        for fp in files:
            with open(os.path.join(root, fp), "r") as f:
                fp_golds = json.load(f)
                for frame, annotations in fp_golds.items():
                    guid = annotations["_image_id"].split(".")[0]
                    csv_line = (
                        guid,
                        frame,
                        build_csv_string(annotations),
                    )
                    out.append(csv_line)
    return out


def build_csv_string(annos: Dict) -> str:
    """Convert a dictionary to a csv string.
    this is done mainly for portability
    ### params
    + annos := dictionary of Role/Filler pairs
    ### returns
    raw CSV string
    """
    pruned_annos = {k: v for k, v in annos.items() if k and k[0] != "_" and v}

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

    return out


def write_csv(csvs: List[Tuple[str, str, str]], outfname: Union[str, os.PathLike]):
    """Write csv lines to file

    ### params
    + csvs := list of tuples that represent csv lines
    + outfname := name of output .csv file
    ### returns
    void
    """
    with open(outfname, "w", encoding="utf8") as f:
        writer = csv.writer(f)
        writer.writerow(["GUID", "FRAME", "ANNOTATIONS"])
        writer.writerows(csvs)


if __name__ == "__main__":
    write_csv(process_golds(sys.argv[1]), outfname=sys.argv[2])
