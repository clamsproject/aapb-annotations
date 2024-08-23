import os
import difflib
import argparse
import pandas as pd
from speaker_identificaiton import identify_speakers, dict_generator


def speaker_words_dicts_generator(file_name):
    with open(file_name) as f:
        transcript_text = f.read()
    speakers = identify_speakers(transcript_text)
    speaker_words_dicts = dict_generator(transcript_text, speakers)
    return speaker_words_dicts


def gold_generator(gold_tsv_dir, gold_transcript_dir):
    speaker_start_end_dicts = {}

    for file in os.listdir(gold_tsv_dir):
        if file.endswith(".tsv"):
            speaker_start_end_dicts.update({file: []})
            gold_tsv_path = os.path.join(gold_tsv_dir, file)
            gold_transcript_path = os.path.join(gold_transcript_dir, file).replace(".tsv", "-transcript.txt")
            if os.path.exists(gold_transcript_path):
                df = pd.read_csv(gold_tsv_path, sep='\t')
                speaker_words_dicts = speaker_words_dicts_generator(gold_transcript_path)
                start_line = 0
                for speaker_words_dict in speaker_words_dicts:
                    speaker = list(speaker_words_dict.keys())[0]
                    words = " ".join(speaker_words_dict[speaker].lower().strip().replace("'", "`").split())
                    current_line = ""
                    for i in range(start_line, len(df['content'])):
                        current_line += " " + " ".join(df['content'][i].lower().replace("'", "`").strip().split())
                        current_line = current_line.strip()
                        if len(words.split())/len(current_line.split()) < 0.5:
                            break
                        if i != 0 and i == start_line:
                            matcher = (difflib.SequenceMatcher(None, words, current_line)
                                       .find_longest_match(0, len(words), 0, len(current_line)))
                            if matcher.a == 0 and matcher.b != 0:
                                current_line = current_line[matcher.b:]
                            elif matcher.a != 0 and matcher.b == 0:
                                possible_leftover_words = current_line[matcher.b:(matcher.b+matcher.size)]
                                if len(possible_leftover_words.split())/len(current_line.split()) > 0.5:
                                    words = words[matcher.a:]
                                else:
                                    break
                            elif matcher.a == 0 and matcher.b == 0:
                                current_line = current_line
                                words = words
                            else:
                                if matcher.size < len(current_line)/2:
                                    break
                                else:
                                    current_line = current_line[matcher.b:]
                                    words = words[matcher.a:]
                        current_ratio = difflib.SequenceMatcher(None, words, current_line, autojunk=False).quick_ratio()
                        next_line = "".join(df['content'][start_line:i+2])
                        next_line = " ".join(next_line.lower().replace("'", "`").strip().split())
                        next_ratio = difflib.SequenceMatcher(None, words, next_line, autojunk=False).quick_ratio()

                        if next_ratio >= current_ratio and i == len(df['content'])-2:
                            start_time = list(df["start"])[start_line]
                            end_time = list(df["end"])[i+1]
                            speaker_start_end_dicts[file].append({"speaker": speaker, "start_time": start_time,
                                                                  "end_time": end_time})

                        if next_ratio < current_ratio:
                            start_time = list(df["start"])[start_line]
                            end_time = list(df["end"])[i]
                            speaker_start_end_dicts[file].append({"speaker": speaker, "start_time": start_time,
                                                                  "end_time": end_time})
                            start_line = i+1
                            break

    return speaker_start_end_dicts


def time_to_ms(time:str):
    other, millisecond = time.split(".")
    hour, minute, second = other.split(":")
    result = int(millisecond) + int(second)*1000 + int(minute)*1000*60 + int(hour)*1000*60*60
    return result


def ms_to_second(ms:int):
    return ms/1000


def rttm_generator(speaker_start_end_dicts:dict):
    for i, item in enumerate(speaker_start_end_dicts):
        gold_list = speaker_start_end_dicts[item]
        rttm_entries = []
        rttm_filename = item.replace(".tsv", ".rttm")
        for slice in gold_list:
            speaker = "_".join(slice['speaker'].split())
            start_time = ms_to_second(time_to_ms(slice['start_time']))
            end_time = ms_to_second(time_to_ms(slice['end_time']))
            length = round((end_time - start_time), 3)
            rttm_entries.append({"TYPE": "SPEAKER", "FILE_ID": item.replace(".tsv", ""), "CHANNEL_ID": 1, "START_TIME":start_time, "DURATION": length, "SPKR_ID":speaker})

        with open(rttm_filename, 'w') as file:
            for entry in rttm_entries:
                line = f"{entry['TYPE']} {entry['FILE_ID']} {entry['CHANNEL_ID']} {entry['START_TIME']} {entry['DURATION']} <NA> <NA> {entry['SPKR_ID']} <NA> <NA>\n"
                file.write(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--gold_tsv_dir", action='store',
                        help='path to the directory of all tsv files that contains a list of start times, end times, and slices of transcripts')
    parser.add_argument("--gold_transcript_dir", action='store',
                        help='path to the directory of all NewsHour transcript files')
    parsed_args = parser.parse_args()
    speaker_start_end_dicts = gold_generator(parsed_args.gold_tsv_dir, parsed_args.gold_transcript_dir)
    rttm_generator(speaker_start_end_dicts)
