"""
This module evaluates the performance of the chyron detection and OCR apps on the chyron dataset.
The chyron dataset is loaded as a CSV containing the following columns:
- video_filename, the name of the video file
- start_time, the start time of the chyron in seconds
- end_time, the end time of the chyron in seconds
- chyron_text, the text of the chyron (could contain multiple lines)
The script takes a path to the CSV file and a path to a directory containing the MMIF files.
The script will iterate through the MMIF files and compare the chyron text and timeframe to the
gold standard. The script will output IOU scores for chyron detection and character error rate.
"""

import argparse
import csv
import os

from mmif import Mmif
from mmif.serialize import Mmif
from mmif.vocabulary import AnnotationTypes, DocumentTypes
from pyannote.core import Segment, Timeline, Annotation
from pyannote.metrics.detection import DetectionErrorRate
import jiwer


def load_gold_standard(chyron_csv):
    gold_text = {}
    gold_timeframes = {}
    with open(chyron_csv, 'r') as gold_csv:
        reader = csv.DictReader(gold_csv)
        for row in reader:
            video_filename = row["filename"]
            start_time = float(row["start"])
            end_time = float(row["end"])
            chyron_text = row["text"]
            if video_filename not in gold_text:
                gold_text[video_filename] = []
                gold_timeframes[video_filename] = Timeline()
            gold_text[video_filename].append(chyron_text)
            gold_timeframes[video_filename].add(Segment(start_time, end_time))
    return gold_text, gold_timeframes


def get_mmif_file_list(mmif_dir):
    mmif_files = os.listdir(mmif_dir)
    return [os.path.join(mmif_dir, file) for file in mmif_files if file.endswith(".mmif")]


def process_mmif_files(mmif_files):
    chyron_text = {}
    chyron_timeframes = {}
    for mmif_file in mmif_files:
        mmif = Mmif(open(mmif_file).read())
        video_filename = mmif.get_documents_by_type(DocumentTypes.VideoDocument)[0].location
        video_filename = os.path.basename(video_filename)
        if video_filename not in chyron_text:
            chyron_text[video_filename] = []
            chyron_timeframes[video_filename] = Timeline()
        chyron_view = mmif.get_view_contains(AnnotationTypes.Alignment)
        anno_id_to_annotation = {annotation.id: annotation for annotation in chyron_view.annotations}
        for annotation in chyron_view.annotations:
            if annotation.at_type == AnnotationTypes.Alignment:
                source_id = annotation.properties["source"]
                target_id = annotation.properties["target"]
                source_anno = anno_id_to_annotation[source_id]
                target_anno = anno_id_to_annotation[target_id]
                chyron_text[video_filename].append(target_anno.text_value)
                chyron_timeframes[video_filename].add(Segment(source_anno.properties["start"], source_anno.properties["end"]))
    return chyron_text, chyron_timeframes


def calculate_error_rates(gold_text, chyron_text):
    for video_filename in chyron_text:
        # print(" ".join(gold_text[video_filename]), " ".join(chyron_text[video_filename]))
        try:
            cer = jiwer.cer(" ".join(gold_text[video_filename])," ".join(" ".join(chyron_text[video_filename]).split()))
            print(f"Character Error Rate {video_filename}= ", cer)
            wer = jiwer.wer(" ".join(gold_text[video_filename]), " ".join(" ".join(chyron_text[video_filename]).split()))
            print(f"Word Error Rate {video_filename}= ", wer)
        except KeyError:
            print(f"Error: {video_filename} not in annotations")


def calculate_detection_metrics(gold_timeframes, chyron_timeframes):
    metric = DetectionErrorRate()

    for video_filename in chyron_timeframes:
        reference = Annotation()
        for segment in gold_timeframes[video_filename]:
            reference[segment] = "chyron"
        hypothesis = Annotation()
        for segment in chyron_timeframes[video_filename]:
            hypothesis[segment] = "chyron"
        try:
            results_dict = metric.compute_components(reference, hypothesis, collar=1.0)
            print (results_dict)
        except KeyError:
            print(f"Error: {video_filename} not in annotations")



if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--chyron_csv")
    ap.add_argument("--mmif_dir")
    args = ap.parse_args()
    chyron_csv = args.chyron_csv
    mmif_dir = args.mmif_dir

    gold_text, gold_timeframes = load_gold_standard(chyron_csv)
    mmif_files = get_mmif_file_list(mmif_dir)
    chyron_text, chyron_timeframes = process_mmif_files(mmif_files)

    calculate_error_rates(gold_text, chyron_text)
    calculate_detection_metrics(gold_timeframes, chyron_timeframes)


