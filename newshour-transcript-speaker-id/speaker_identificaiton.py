import os
import re
import spacy
from clams_utils.aapb.newshour_transcript_cleanup import clean_brackets
nlp = spacy.load("en_core_web_sm")


def clean_titles(transcript_text):
    """
    Given a plain text read from a txt file, clean the news section titles in the transcript,
    including "Focus", "Intro", and "News Summary"
    """
    focus = r'\nFOCUS\s?-.*\n'
    focus_removed = re.sub(focus, '\n', transcript_text)

    intro = r'\nI(?i:ntro)[\n\s]'
    intro_removed = re.sub(intro, '\n', focus_removed)

    newsmaker = r'\nN(?:ewsmaker)\n'
    newsmaker_removed = re.sub(newsmaker, '\n', intro_removed)

    recap = r'\nRECAP.*\n'
    recap_removed = re.sub(recap, '\n', newsmaker_removed)

    conversation = r'\nCONVERSATION.*?\n'
    conversation_removed = re.sub(conversation, '\n', recap_removed)

    update = r'\nUPDATE\s?-.*\n'
    update_removed = re.sub(update, '\n', conversation_removed)

    lookback = r'\nFINALLY\s?-.*\n'
    lookback_removed = re.sub(lookback, '\n', update_removed)

    secondlook = r'\nSECOND LOOK\s?-.*\n'
    secondlook_removed = re.sub(secondlook, '\n', lookback_removed)

    news_summary = r'(?<=\s|\n)N(?i:ews)\s(?i:summary)(?=\n)'
    all_titles_removed = re.sub(news_summary, '\n', secondlook_removed)

    return all_titles_removed


def identify_speakers(transcript_text):
    transcript_text = "\n"+clean_titles(clean_brackets("\n"+transcript_text))
    speakers = []
    for line in transcript_text.split("\n"):
        if line:
            split = line.split(":", 1)
            if len(split) > 1 and line.split(":", 1)[1] != "":
                speaker = line.split(":", 1)[0]
                speakers.append(speaker)

    speakers = set(speakers)
    cleaned_speakers = []
    for speaker in speakers:
        cleaned_speakers.append(speaker.strip())

    finalized_speakers = []
    for i, cleaned_speaker in enumerate(cleaned_speakers):
        if len(cleaned_speaker.split(".")) > 1:
            cleaned_speaker = cleaned_speaker.split(".")[-1].strip()
        if name_checker(cleaned_speaker,cleaned_speakers[:i])[0] == False and name_checker(cleaned_speaker,cleaned_speakers[i+1:])[0] == False:
            finalized_speakers.append(cleaned_speaker)

    return finalized_speakers


def unify_speakers(transcript_line, finalized_speakers):
    speaker_exist = True
    split = transcript_line.split(":", 1)
    doc = nlp(split[0])
    tag_list = [token.tag_ for token in doc]
    if "VBD" in tag_list:
        speaker_exist = False
        speaker = None
        words = transcript_line
    elif len(split) > 1 and transcript_line.split(":")[1] != "":
        speaker = transcript_line.split(":")[0]
        words = ":".join(transcript_line.split(":")[1:])
        if "." in speaker:
            speaker = speaker.split(".")[-1].strip()
        exist_bool, replace_name = name_checker(speaker, finalized_speakers)
        if exist_bool:
            speaker = replace_name
    else:
        speaker_exist = False
        speaker = None
        words = transcript_line
    return speaker_exist, {speaker: words}


def name_checker(target_name, name_list):
    exist = False
    replace_name = ""
    for name in name_list:
        if "".join(target_name.split()).lower() in "".join(name.split()).lower():
            exist = True
            replace_name = name
    return exist, replace_name


def transcript_dir_speakers(transcript_dir):
    each_file_speakers = []
    for file in os.listdir(transcript_dir):
        if file.endswith(".txt"):
            with open(os.path.join(transcript_dir, file), 'r') as f:
                transcript = f.read()
                each_file_speakers.append(identify_speakers(transcript))

    return each_file_speakers


def dict_generator(transcript_text, finalized_speakers):
    transcript_text = "\n" + clean_titles(clean_brackets("\n" + transcript_text))
    lines = transcript_text.split("\n")
    mappings = []
    for i, line in enumerate(lines):
        if line:
            speaker_exist, mapping = unify_speakers(line, finalized_speakers)
            if not speaker_exist:
                last_speaker = list(mappings[-1].keys())[-1]
                mappings[-1][last_speaker] = mappings[-1][last_speaker] + " " + mapping[None]
            else:
                mappings.append(mapping)
    return mappings

#
# if __name__ == '__main__':
#     gold_text_dir = "/Users/selenasong/Desktop/CLAMS/aapb-collaboration/21"
#     speakers_removed_gold = "/Users/selenasong/Desktop/CLAMS/21"
#     os.makedirs(speakers_removed_gold, exist_ok=True)
#     for docs in os.listdir(gold_text_dir):
#         print(docs)
#         if docs.endswith(".txt"):
#             transcript_path = os.path.join(gold_text_dir, docs)
#             speakers_removed_gold_path = os.path.join(speakers_removed_gold, docs)
#             pure_text = ""
#             with open(transcript_path, 'r') as f:
#                 transcript_text = f.read()
#             speakers = identify_speakers(transcript_text)
#             for line in dict_generator(transcript_text, speakers):
#                 pure_text += list(line.values())[-1]
#             with open(speakers_removed_gold_path, 'w') as f:
#                 f.write(pure_text)
