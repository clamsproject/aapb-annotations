# Scene-with-text Transcription

## Project Overview

This annotation project is a follow-up effort to `scene-recognition`. In the previous project, the primary goal was to label still images (video frames) based on the distinctive visual elements. In this follow-up project, the focus shifts to transcribing the textual content found within the frames previously identified as "scenes with text." (e.g., slates, chyrons, credits)


> [!NOTE]
> At the moment, the focus is not on general ["scene text"](https://en.wikipedia.org/wiki/Scene_text) in the background captured in the footage, but mostly on injected or overlay text that include "names" that can be used directly as 

### Specs
* Annotation Project Name - `swt-transcription`
* Annotator Demographics
    * Number of annotators - 3
    * Occupational description - college student
    * Age range - 20s
* Annotation Environment Information
    * Name - Keystroke Labeler
    * Version - unknown
    * Tool documentation - (see below tool installation)
* Project Changes
    * Used batch - 3 batches
        * [`aapb-collaboration-27-e`](../batches/aapb-collaboration-27-e.txt): part of this batch (504 out of 1118 video assets) was annotated for transcribing their "slates". 
            * TODO: mention this portion of the data is also published on kaggle
        * [`new-chyron-batch`](../batches/new-chyron-batch.txt): newly compiled batch for annotating "chyrons". (5 assets overlap with `aapb-collaboration-27-e` batch)
            * cpb-aacip-1c5c6f8385a
            * cpb-aacip-42-54xgxmgs
            * cpb-aacip-4fc500005b7
            * cpb-aacip-80aceff1fc5
            * cpb-aacip-9e207ee0214
        * [`new-hichy-batch`](../batches/new-hichy-batch.txt): newly compiled batch for annotating chyrons in Hawaiian stations. 
    * Other version control information - N/A

## Tooling 

Consistent with the previous project, the Keystroke Labeler tool was utilized. Detailed information, including installation instructions, can be found in the [documentation for the previous project](https://github.com/clamsproject/aapb-annotations/tree/main/scene-recognition#tool-installation-keystroke-labeler).

For transcript annotation, several additional "note" fields were introduced to capture text input.

## Annotation Guidelines

### Preparation
Source images are prepared in the identical way as the previous project. See the [relevant section in the previous project](https://github.com/clamsproject/aapb-annotations/tree/main/scene-recognition#preparation)]

### What to Annotate
The previous project was mostly focused on categorizing extracted still images, while ...

TODO: confirm how much of "labeling" done in this stage? 

### How to Annotate It

TODO: confirm the relevancy and accuracy of contents from `conf.js` files.

#### slate-portion
##### note-3
an3Guidance = "Transcribe verbatim the text on the screen, including every character.<br>";
an3Guidance += "Preserve capitalization, meaningful spacing, and line breaks.";

##### note-4
an4Guidance = "Record values for any of the following elements:<br>";
an4Guidance += "<div class='help-msg'>";
let els = [ "program-title",
"episode-title",
"series-title",
"title",
"episode-no",
"create-date",
"air-date",
"date",
"director",
"producer",
"camera" ];
for (let i=0; i<els.length; i++){
an4Guidance += ("<span class='help-key'>" + els[i] + "</span><br>");
}
an4Guidance += "</div>";
an4Guidance += "Normalize dates as <span class='help-key'>`YYYY-MM-DD`</span>.<br>";
an4Guidance += "Normalize names as <span class='help-key'>`Last, First Middle`</span>.<br>";


#### chyron portion
##### note-3
Leave this area blank unless the frame type is"I", "N", or "Y".<br><br>

If the frame category is "I", "N", or "Y", then transcribe verbatim the text in the "lower third" or "chryon" area of the screen, including every character.  Preserve spacing and line breaks where feasible.<br><br>

Do not, under any circumstances, include text that is in the top half of the frame.<br><br>

Even for text in the bottom half of frame, do not include the text unless it is part of the chyron graphical element.  Easily legible text in a logo that is part of the chyron should be included, but watermarks, background text, and filmed text should be omitted.<br><br>

##### note-4
Leave this area blank unless the frame type is "I".  If the frame type is "I", then identify important parts of the person's name and characteristics as follows:<br><br>

In general:  Add one datum per line, skipping lines between items.<br><br>

<span class='help-em'>First datum:</span>  Copy exactly the person's name as written, including titles (such as "Miss", "Dr.", "Senator", "Rev.", etc.) and designations (such as "M.D." or "Ph.D.").  Preserve capitalization presented on screen.<br><br>

<span class='help-em'>Second datum:</span> Write the normalized form of the person's name.  Normalize capitalization, and change the order to "Lastname, Firstname" or "Lastname, Firstname Middlename, Suffix".  For example: "Murray, Patty" or "King, Martin Luther, Jr."  Do not add names, initials, or forms of the name not appearing on the screen.<br><br>

<span class='help-em'>Additional data:</span>  Copy verbatim any role, location, context, or other characteristics associated with the person, with one attribute per line.  Do not separate attributes into multiple lines unless they could be considered separate attributes of the person <strong>and</strong> are deliberately separated spatially on the screen (as with a hard line break, but not just with wrapping long lines).  In cases of multiple attributes, skip one line between them.<br><br>

TODO: clarify the order and relations between many `img*.js` files

#### PLACEHOLDERfor hi-chy data

### Decisions, Differentiation, and Precision Level during Annotation
TODO: cite fine lines in the conf.js guidelines 

#### Data Quality Efforts (or other subheaders, optional)

TODO: any QC effort made by Owen? 

## Data Format and `process.py`

### `raw` data
`.csv` files named after the source asset GUID, including all the columns from the previous project ([relevant section in the previous project](https://github.com/clamsproject/aapb-annotations/tree/main/scene-recognition#raw-data])), and expanding the `note` column to store manual transcription results. 

* Fields:
    * `filename` (string) - the filename of the image to be labeled. Included within the filename of the image is also its time information in ISO format.
    * `seen` (bool) - indicates whether the item has been seen
    * `type label` (char) - indicates the type label, if any, of seen items
    * `subtype label` (char) - indicates the subtype label, if any, of items with type labels
    * `modifier` (bool) - indicates whether the label has the "modifier" status
    * `note-3` (string) - _verbatim_ transcription of the text in the source image, where a best attempt is made to keep the original reading order intact using spaces and newlines.
    * `note-4` (string) - _normalized_ transcription based on the verbatim text from the previous column. Normalization method is written with more details in the annotation guidelines (see [above](#annotation-guidelines))

### [`process.py`](process.py)
Again, the processing script does the same clean-up and re-organization ([relevant section in the previous project](https://github.com/clamsproject/aapb-annotations/tree/main/scene-recognition#processpy])), then add `note-3` and `note-4` values to new columns. 

### `golds` data
A set of `.csv` files in which each row is a frame timestamped and with relevant labels and transcripts. Rows are sorted by the timestamp.

* Fields:
    * `at` - string representing the ISO timestamp of the frame
    * `scene-type` - string representing the type label (from `type label` in raw data)
    * `scene-subtype` - string representing the subtype label, if applicable (from `subtype label` in raw data)
    * `transitional` - boolean representing if the image is _transitional_ between two scene types (from `modifier` in raw data)
    * `text-transcript` - string transferred from `note-3` (verbatim) column in the raw data
    * `???` - string transferred from `note-4` (normalized) column in the raw data 
    * TODO: pick a name for this
    * all other columns from the raw data are removed
* Example:
```
example here. 
```

## See also (optional, if applicable)
(any related projects, dataset, software, etc.)
