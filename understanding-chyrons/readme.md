# Understanding Chyrons

## Project Overview

This annotation project is a follow-up effort to [`scene-recognition`](../scene-recognition). In the previous project, the primary goal was to label still images (video frames) based on the distinctive visual elements. In this follow-up project, the focus shifts to annotating transcription and understanding of the textual content found in "chyron" (also kwown as [lower third](https://en.wikipedia.org/wiki/Lower_third)) images. 

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
    * Used batches
        * [`hi-chy-practice`](../batches/hi-chy-practice.txt): 23 GUIDs, 507 annotation records
        * [`hi-chy-hi-pre-2000`](../batches/hi-chy-hi-pre-2000.txt): 72 GUIDs, 1430 annotation records
        * [`hi-chy-hi-post-2000`](../batches/hi-chy-hi-post-2000.txt): 86 GUIDs, 395 annotation records
    * Planned batches
        * hi-chy-comps-pre-2000
        * hi-chy-comps-post-2000
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
Tool usage hasn't changed from the previous project. However since this annotation started from pre-compiled confirmed images of slates, the `type` was pre-filled as either "I", "Y", or "N".  The annotator was asked to correct the scene type label when pre-filled value is wrong. The annotator's primary job was to fill in the `note-3` and `note-4` fields, following the guidelines below.

### Decisions, Differentiation, and Precision Level during Annotation

The guidelines in this section are copied from the `conf.js` file used in the KSL for the annotation. The original guidelines were written in HTML syntax and have been adapted here for markdown syntax.

#### Verbatim transcription
(in `note-3` field)

To annotate, enter text in the box. Leave this area blank unless the frame type is "I", "N", or "Y".

If the frame category is "I", "N", or "Y", then transcribe verbatim the text in the "lower third" or "chryon" area of the screen, including every character. Preserve spacing and line breaks where feasible. Do not, under any circumstances, include text that is in the top half of the frame. Even for text in the bottom half of frame, do not include the text unless it is part of the chyron graphical element. Easily legible text in a logo that is part of the chyron should be included, but watermarks, background text, and filmed text should be omitted.

To transcribe an okina character, use the backtick: ` (ASCII code 39).

#### Text understanding
(in `note-4` field)

To annotate, enter text in the box. Leave this area blank unless the frame type is "I". If the frame type is "I", then identify important parts of the person's name and characteristics as follows:
In general: Add one datum per line, skipping lines between items.

First datum: Copy exactly the person's name as written, including titles (such as "Miss", "Dr.", "Senator", "Rev.", etc.) and designations (such as "M.D." or "Ph.D."). Preserve capitalization presented on screen.

Second datum: Write the normalized form of the person's name. Normalize capitalization, and change the order to "Lastname, Firstname" or "Lastname, Firstname Middlename, Suffix". For example: "Murray, Patty" or "King, Martin Luther, Jr." Do not add names, initials, characters (such as an okina), or forms of the name not used in the verbatim transcription.

Additional data: Copy verbatim any role, location, context, or other characteristics associated with the person, with one attribute per line. Do not separate attributes into multiple lines unless they could be considered separate attributes of the person and are deliberately separated spatially on the screen (as with a hard line break, but not just with wrapping long lines). In cases of multiple attributes, skip one line between them.

#### Data Quality Efforts (or other subheaders, optional)

No separate post-annotation QC effort were reported, but the annotation process was conducted with careful attention to data quality. Guidelines were established through a rigorous setup phase including a practice round, followed by discussions to address edge cases, ambiguities, and consistency in transcription and data formatting. 

## Data Format and `process.py`

### `raw` data
Annotations for each batch are stored in a `.js` file. This JavaScript file defines a single variable that holds a list of manual annotations and associated metadata. Within this list, each "record" corresponds to the annotations for one chyron instance. A record itself is a list comprising the following elements, in the specified order:

* `filename` (string) - the filename of the image to be labeled. Included within the filename of the image is also its time information in ISO format.
* `seen` (bool) - indicates whether the item has been seen
* `type-label` (char) - indicates the type label, if any, of seen items
* `subtype-label` (char) - indicates the subtype label, if any, of items with type labels
* `modifier` (bool) - indicates whether the label has the "modifier" status, indicating the frame was "transitional" in the sense that the still image was captured as the text was fading in or out of view
* `note-3` (string) - a _verbatim_ transcription of the text in the source image, where a best attempt is made to keep the original reading order intact using spaces and newlines.
* `note-4` (string) - a _re-formatted_ structured understanding based on the verbatim text from the previous column. The method for re-formatting by structuring the text to key-value pairs is written with more details in the annotation guidelines above.

### [`process.py`](process.py)
Again, the processing script does the same clean-up and re-organization ([relevant section in the previous project](https://github.com/clamsproject/aapb-annotations/tree/main/scene-recognition#processpy])), then add `note-3` and `note-4` values to new columns, while also performing the following additional tasks to handle issues in the raw data:

1. Skip any rows that are maked as `DUPE`. 
2. Ignore `note-4` values that do not conform to the specified annotation guidelines (i.e., are malformed syntax-wise). Only `note-3` values are kept in such cases.

> [!NOTE]
> In the previous scene type labeling project, both the raw and gold data are serialized in CSV format, while the current project uses JSON for both. The decision was to avoid the complexity of encoding structured text in a plain text format, and to leverage the inherent structural syntax of the JSON format.

### `golds` data
A set of `.json` files in which each row is a frame timestamped and with relevant labels and transcripts. Rows are sorted by the timestamp.

* Fields:
    * `at` - string representing the ISO timestamp of the frame
    * `scene-type` - string representing the type label (from `type label` in raw data)
    * `scene-subtype` - string representing the subtype label, if applicable (from `subtype label` in raw data)
    * `transitional` - boolean representing if the image is _transitional_ between two scene types (from `modifier` in raw data)
    * `text-transcript` - string transferred from `note-3` (verbatim) column in the raw data. Line break markers are replaced with actual line breaks (U+000A). 
    * `keyed-information` — an object (string-string) transferred from the `note-4` (key-value) column in the raw data: the first line (datum) is keyed as `name-as-written`, the second as `name-normalized`, and all other lines are included under `attributes` as a list of strings. Or `null` if the `note-4` data is not automatically parse-able due to format issues. 
    * All other columns from the raw data are removed.
* Example:
```
$ cat golds/cpb-aacip-225-99n2zd03.json
[
  {
    "at": "00:03:19.265",
    "scene-type": "I",
    "scene-subtype": "",
    "transitional": false,
    "text-transcript": "TOM OKAMURA (D)\n\nHouse Majority Leader",
    "keyed-information": {
      "name-as-written": "TOM OKAMURA (D)",
      "name-normalized": "Okamura, Tom",
      "attributes": [
        "House Majority Leader"
      ]
    }
  }
]

$ cat golds/cpb-aacip-225-22h70v35.json
[ 
  ...
  {
    "at": "00:22:04.022",
    "scene-type": "I",
    "scene-subtype": "",
    "transitional": false,
    "text-transcript": "George Mavrothalassitis",
    "keyed-information": null
  }
]
```
