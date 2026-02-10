# Understanding Slates

## Project Overview

This annotation project is a follow-up effort to [`scene-recognition`](../scene-recognition). In the previous project, the primary goal was to label still images (video frames) based on the distinctive visual elements. In this follow-up project, the focus shifts to annotating transcription and understanding of the textual content found in "slates" images. 

### Specs
* Annotation Project Name - `swt-transcription`
* Annotator Demographics
    * Number of annotators - 2
    * Occupational description - college student (primary), GBH Metadata Operations Specialist (secondary/reviewer)
* Annotation Environment Information
    * Name - Keystroke Labeler
    * Version - unknown
    * Tool documentation - (see below tool installation)
* Project Changes
    * Used batch: [`aapb-collaboration-27-f`](../batches/aapb-collaboration-27-f.txt), a part of this batch (503 out of 1118 video assets) was annotated for transcribing their "slates". 
        * This dataset is also available on [Kaggle](https://www.kaggle.com/datasets/madisoncourtney/transcribed-slates)
        * This dataset is based on the *version 7* of the Kaggle distribution.
    * Other version control information - N/A

## Tooling 

Consistent with the previous project, the Keystroke Labeler tool was utilized. Detailed information, including installation instructions, can be found in the [documentation for the previous project](https://github.com/clamsproject/aapb-annotations/tree/main/scene-recognition#tool-installation-keystroke-labeler).

For transcript annotation, several additional "note" fields were introduced to capture text input.

## Annotation Guidelines

### Preparation
Source images are prepared in the identical way as the previous project. See the [relevant section in the previous project](https://github.com/clamsproject/aapb-annotations/tree/main/scene-recognition#preparation)]

### What to Annotate
The previous project was mostly focused on categorizing extracted still images, while this project aims at 
1. literally transcribing the text found in those images
1. re-format the text into structured data based on human understanding of the text

### How to Annotate It
Tool usage hasn't changed from the previous project. However since this annotation started from pre-compiled confirmed images of slates, the `type` was pre-filled as "S" (slate).  The annotator was asked to choose the correct sub-type for the Slate, and also set the modifier flag if the slate frame should be considered "transitional".  The annotator's primary job was to fill in the `note-3` and `note-4` fields, following the guidelines below.

### Decisions, Differentiation, and Precision Level during Annotation
The guidelines in this section are copied from the `conf.js` file used in the KSL for the annotation. The original guidelines were written in HTML syntax and have been adapted here for markdown syntax.

#### Verbatim transcription
(in `note-3` field)

Transcribe verbatim the text on the screen, including every character.
Preserve capitalization, meaningful spacing, and line breaks.

#### Text understanding
(in `note-4` field)

Record values for any of the following elements:

- program-title
- episode-title
- series-title
- title
- episode-no
- create-date
- air-date
- date
- director
- producer
- camera

Normalize dates as `YYYY-MM-DD`.
Normalize names as `Last, First Middle`.

#### Data Quality Efforts (or other subheaders, optional)

All data reviewed and corrected by a secondary annotator as of Feb 2025. 

## Data Format and `process.py`

### `raw` data
Annotations for each batch are stored in a `.js` file. This JavaScript file defines a single variable that holds a list of manual annotations and associated metadata. Within this list, each "record" corresponds to the annotations for one slate instance. A record itself is a list comprising the following elements, in the specified order:

* `filename` (string) - the filename of the image to be labeled. Included within the filename of the image is also its time information in ISO format.
* `seen` (bool) - indicates whether the item has been seen
* `type-label` (char) - indicates the type label, if any, of seen items
* `subtype-label` (char) - indicates the subtype label, if any, of items with type labels
* `modifier` (bool) - indicates whether the label has the "modifier" status, indicating the frame was "transitional" in the sense that the still image was captured as the text was fading in or out of view
* `note-3` (string) - a _verbatim_ transcription of the text in the source image, where a best attempt is made to keep the original reading order intact using spaces and newlines.
* `note-4` (string) - a _re-formatted_ structured understanding based on the verbatim text from the previous column. The method for re-formatting by structuring the text to key-value pairs is written with more details in the annotation guidelines above.

### [`process.py`](process.py)
Again, the processing script does the same clean-up and re-organization ([relevant section in the previous project](https://github.com/clamsproject/aapb-annotations/tree/main/scene-recognition#processpy])), then add `note-3` and `note-4` values to new columns. 

> [!NOTE]
> In the previous project, both the raw and gold data are serialized in CSV format, while the current project uses JSON for both. The decision was to avoid the complexity of encoding structured text in a plain text format, and to leverage the inherent structural syntax of the JSON format.

### `golds` data
A set of `.json` files in which each row is a frame timestamped and with relevant labels and transcripts. Rows are sorted by the timestamp.

* Fields:
    * `at` - string representing the ISO timestamp of the frame
    * `scene-label` - string representing the type label (from `type label` in raw data)
    * `scene-subtype-label` - string representing the subtype label, if applicable (from `subtype label` in raw data)
    * `transitional` - boolean representing if the image is _transitional_ between two scene types (from `modifier` in raw data)
    * `text-transcript` - string transferred from `note-3` (verbatim) column in the raw data. Line break markers are replaced with actual line breaks (U+000A). 
    * `keyed-information` - object (string-string) transferred from `note-4` (key-value) column in the raw data, parsed based on these delimiters; `\\n` between pairs, `:` between keys and values
    * all other columns from the raw data are removed
* Example:
```
$ cat golds/cpb-aacip-27def972f9c.json 
[
  {
    "at": "00:01:07.000",
    "scene-label": "S",
    "scene-subtype-label": "D",
    "transitional": false,
    "text-transcript": "Wild Florida\nShow # 209\n\"DRY TORTUGAS\"\nTRT: 26:42\nSTEREO",
    "keyed-information": {
      "episode-title": "Dry Tortugas",
      "series-title": "Wild Florida",
      "episode-no": "209"
    }
  }
]
```
