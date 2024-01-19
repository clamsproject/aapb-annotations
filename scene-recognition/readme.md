# Scene Recognition 

## Project Overview

> The essential goal for scene recognition is to assign the semantic labels to the given images, these semantic labels are defined by human beings including different natural views, indoor scenes, outdoor environments and etc.
> -- [Scene recognition: A comprehensive survey](https://www.sciencedirect.com/science/article/pii/S003132032030011X)

This project is an attempt at developing a dataset for a new CLAMS app that detects "frames of interest" or "scene recognition" in general as an update to the previous efforts of seeking different frames out separately. 
"Frames of Interest" tend to be frames from a video that contain information (primarily in some overlaying textual forms) on screen that is useful for archiving purposes. This can include slates, chyrons, credits, images of people or other visual objects. 

From the annotation side, the project is done by sampling videos at a certain rate (e.g. currently 1 frame every 2 seconds) to create a diverse set of frames as a collection of stills (going forward called "image sets"). 
The frames are then annotated for if they fit one of the interest categories or not. 

Conceptually, the annotation project simply annotates stills found at recurring intervals (but arbitrarily chosen) that do not themselves describe the start and end times of a _scene_. Additional post-processing by software can stitch together these still level annotations into time interval annotations, but manually annotating time intervals is not under scope of the project. 

### Specs
* Annotation Project Name - `scene-recognition`
* Annotator Demographics
    * Number of annotators - 2
    * Occupational description - College Student and Metadata Operation Specialist GBH
    * Age range - 20-40s
    * Education - Higher education
* Annotation Environment Information
    * Name - Keystroke Labeler
    * Version - unknown
    * Tool documentation - (see below tool installation)
* Project Changes
    * Number of batches - 3
        * Batch information: There are three batches annotated in two ways. [`27-a`](231002-aapb-collaboration-27-a) and [`27-c`](231204-aapb-collaboration-27-c) were densely-seen/labeled (40 GUIDs), while [`27-b`](231002-aapb-collaboration-27-b) was sparsely-seen/labeled (21 GUIDs). See below for more information on the differences between "dense" and "sparse" ways of annotating.
    * Other version control information - none

## Tool Installation: Keystroke Labeler
We use [Keystroke Labeler](https://github.com/WGBH-MLA/keystrokelabeler), an annotation tool that is developed in GBH for this project.  
Documentation of the tool, including explanation of inner parts and fields in the labeler can be found [in its repository](https://github.com/WGBH-MLA/keystrokelabeler/blob/main/labeler_data_readme.md).  
Please refer to the tool source code repository for instructions for installation and usage.  

### Tool Access
Currently, annotators are accessing the tool via web app instances locally on their personal devices or deployed on servers that Brandeis team manages. When deployed to remote servers, each instance is one GUID/video on its own, and once annotation is done for a video, annotators must _export_ the annotation data into csv or json file and upload to a shared cloud storage space (google drive). This is because the tool doesn't support save-on-server, and during the export process annotators must rename the file name to match the video GUID. 

## Annotation Guidelines
> [!Important]  
> Please read this explanation of the types of frames first. 
> [`Types of frames`](https://docs.google.com/document/d/1IyM_rCsCr_1XQ39j36WMX-XnVVBT4T_01j-M0eYqyDs/edit) is the guidelines for this project along with more specific instructions from this `readme.md`.   

### Preparation
The annotation project manager first needs to extract still images from chosen videos, using the extraction script included in the tool source code (so far all annotation is done with images sampled at 1 frame every 2 seconds). 
This intends to give some diversity to the frames extracted from the video. 
The set of frames must be then loaded into the [tool](https://github.com/WGBH-MLA/keystrokelabeler/blob/main/labeler_data_readme.md). 

### What to Annotate
This tool creates an annotation file that has different columns for each frame.  
For each frame, pick which category of Frame of Interest or none.   
Then choose a subtype if needed.   
Enter the needed keystrokes, including modifier key if needed.  
In [keystroke mode](https://github.com/WGBH-MLA/keystrokelabeler/tree/main#starting-and-restarting:~:text=explicitly%20defined%20categories%22.-,Modes%3A,-The%20labeler%20has), the tool will move on to the next frame. In editor mode, you can add a `subtype label`. 

- `seen` (bool) - This attribute describes whether the annotator/tool has annotated the frame. If "seen", that piece of data can be used for ML training.  
- `type label` (char) - This is which category of Frame of Interest or none. "No label" plus "seen" is the same as not a frame of interest. 
- `subtype label` (char) - Indicates if there is a `subtype` within that frame category/`type label`. E.g. "Slates (`type`)" can be "Handwritten (`subtype`)", or "Digital (`subtype`)" or other options. Only "Slates" currently have a `subtype`. 
- `modifier` (bool) - This indicates if there is a modifier to the `type label`. e.g. Currently the only `modifier` is "[Transitional](https://docs.google.com/document/d/1IyM_rCsCr_1XQ39j36WMX-XnVVBT4T_01j-M0eYqyDs/edit#heading=h.xnfilznsrhpe)" meaning the frame in question is fading in or out from one `type`/category to another.  

(Other columns are not used)

Other non-data-field terminology/hyper-definitions:  
- "proceed" - This means to move onto the next image, without "seeing" it. 
- "jump factor" - Not to be confused with the already sampled rate of the image set from the video. Now that the image set is loaded, you can skip through the images by using the jump factor to increase the size of step.  
- "mode" - Mode of the tool.
- "sample rate" - This is a parameter that is used before the annotation tool is ready to use. It refers to how the image set is extracted from the video; at what sampling rate. 
- "annotation density" - This is a qualitative distinction of image sets and how annotated/labeled/seen they are. In the densely-seen `27-a` & `27-c`, each image from the image set is seen by an annotator and labeled. No label is synonymous with a negative-case: seen, labeled as not-of-interest. 
Conversely, `27-b` is sparsely-seen, which means that only some images from the image set are annotated/labeled/seen. The rest are essentially providing no manual annotation (and thus are "held out" from being used in training our in-house SR model).

The most important types to annotate are highlighted in (green) on the `types of frames` above. These should be clearly delineated from each other in the guideline. 
The subtypes of slates (blue) is also important to annotate.  
However, the non-important cases (grey) are various different negative cases that are not frames of interest. These may be similar to positive cases. These are sometimes less distinct between each other. Do the best possible, but move on if too much time is spent figuring out the distinctions.  
Add the [modifier](https://docs.google.com/document/d/1IyM_rCsCr_1XQ39j36WMX-XnVVBT4T_01j-M0eYqyDs/edit#heading=h.xnfilznsrhpe) where needed. I.e. Pick the most preferred, clearest `type label`, add "Shift" when making the key combo. 

### How to Annotate It
The tool uses one or two key-combination presses to annotate the different kinds of frames. A key combination can be a single key, or could be a combo like "Shift + P". Press the relevant one to annotate the `type`. 
To add a `subtype`, you will need to enter editor mode, use "Esc" key to do that. 
In editor mode, you will be able to use the up and down arrows to move between `type` and `subtype` entering.
Press the key combo needed to annotate the main `type`. The press down to move to `subtype` and press another key combo for the relevant choice. Move on with "Enter" or "Return". 
This will keep you in Editor Mode. To leave editor mode, press "esc". 
Only Slates has `subtype`s.    

Add the `modifier` by holding "Shift" and the key of the preferred label. Pick the most preferred, clearest `type label`, add "Shift" when making the key combo. 

If you are using the annotation tool via local-host instance, note that there is no save feature. You must do the annotation in one session. 
Leaving the browser tab for a short moment is fine. However, extended absence will likely cause the browser to refresh, losing your progress. 
At the end of your session, "Export" both "JS array" and "CSV".

Tip: Zoom in your browser with "Ctrl/Cmd Plus" if the text is too small. You will only need "Export"s at the end.  
Tip2: You should stay in Editor Mode until you get out of labelling Slates.  

### Decisions, Differentiations and Precision during Annotation
Please see the guidelines for the differentiation guide.  

#### Data Quality Efforts
It is assumed, due to the low difficulty of the annotation, that high accuracy of the data in one pass is reasonably plausible.

One annotation check was done on the 10 videos added to `27-a` batch by @jarumihooi. 2 videos were checked closely, the other 8 were checked only for beginning Slate labels. 
The check only looked at frames that were labeled and at the transitions between different labels. 
Sections with all the same label were also skimmed unless something caught the eye of the checker. 
No `.csv` files were edited to corrections/checker-decisions.  

Results:  

* `cpb-aacip-516-8c9r20sq57.csv` #1 
  * There are many ones where Shift should have been used. Not counting these, but suspect about 12/920. 
  * Important errors: 3/920 (all classified as positive, should be negative. False Pos.) 
  * Non-important Non-shift errors: 3/920 
  * **0.3%** Important Non-shift Error rate (ie. less than 1%).
* Approximately after `cpb-aacip-516-8c9r20sq57.csv` #1, `cpb-aacip-512-3f4kk95f7h.csv` #2, `cpb-aacip-512-416sx65d21.csv` #3 The annotator started using Shift+ for Transitional modifiers. 
* `cpb-aacip-d8ebafee30e.csv` #10
  * Important errors: 0/902 
  * Non-important errors: 27/902
  * **0.0%** Important Error rate 

#### Bounding 
* **subinterval** - Because of the sampling, it is typically best to think of the annotation of frames (at a certain time) as enclosing borders for a subinterval. The annotation should be within the timeframe of the phenomena. Eg. The real onscreen time for a chyron might peek past its annotated time. 

## Data format and `process.py`
### `raw` data
`.csv` file - The file contains columns of the labeling of each frame. 
The file can contain arbitrary amounts of frames that are "unseen"; these are basically not used for ML Training. 
* Fields:
    * `filename` (string) - the filename of the image to be labeled. Included within the filename of the image is also its time information in ISO format. 
    * `seen` (bool) - indicates whether the item has been seen
    * `type label` (char) - indicates the type label, if any, of seen items
    * `subtype label` (char) - indicates the subtype label, if any, of items with type labels
    * `modifier` (bool) - indicates whether the label has the "modifier" status
    * `transcript` (string) - not implemented; not used; always an empty string
    * `note` (string) - not implemented; not used; always an empty string
* Example:
```
$ head -5 cpb-aacip-08fb0e1f287.csv
"filename","seen","type label","subtype label","modifier","transcript","note"
"cpb-aacip-08fb0e1f287_02194825_00000000.jpg",true,"","",false,"",""
"cpb-aacip-08fb0e1f287_02194825_00002002.jpg",true,"","",false,"",""
"cpb-aacip-08fb0e1f287_02194825_00004004.jpg",true,"B","",false,"",""
"cpb-aacip-08fb0e1f287_02194825_00006006.jpg",true,"B","",false,"",""
```

### [`process.py`](process.py)
_TODO: This does not exist yet and the gold format has not been determined._  

### `golds` data
_TODO: This does not exist yet and the gold format has not been determined._  
`.format` file - tba.  
* Fields:
    * `field-text1` - tba
    * `field-text2` - tba
    * all other columns from the raw data are removed
* Example:
```
example here. 
```
