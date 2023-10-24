# Scene Recognition 

## Project Overview
This project is a new attempt at detecting "frames of interest" or "scenes with text" in general as an update to the previous efforts of seeking different frames out separately. 
"Frames of Interest" tend to be frames from a video that contain textual information on screen that is useful for archiving purposes. This can include slates, chyrons, images of people/video subjects, and credits. 

From the annotation side, the project is done by sampling videos at a certain rate (e.g. currently 1 frame every 2 seconds) to create a diverse set of frames as a collection of stills. 
The frames are then annotated for if they fit one of the interest categories or not. 

Later, results from the Scene Recognition detection can be used to stitch together larger time intervals that describe a time interval containing an audiovisual phenomenon in time within the video. 
Conceptually, while the annotation project simply annotates stills found at recurring intervals (but arbitrarily chosen) that do not themselves describe
the start and end times of a phenomena, a model trained with this information could label up to a certain segment all as one kind of phenomena, 
and post-processing (and data smoothening) could be used to determine when the phenomena truly starts and ends via computer vision.

### Specs
* Annotation project name - `scene-recognition`
* Annotator Demographics
    * Number of annotators - 2
    * Occupational description - College Student and Metadata Operation Specialist GBH
    * Age range - 20-40s
    * Education - College & PhD
* Annotation Environment information
    * Name - Keystroke Labeler
    * Version - unknown
    * Tool Documentation - (see below tool installation)
* Project changes
    * Number of Batches - 2 
        * Batch Information: There are two batches used for training and evaluation split during the first iteration: Scenes With Text. `batchA` was densely-seen/labeled (20 GUIDs), while `batchB` was sparsely-seen/labeled (21 GUIDs). 
        * It seems likely that the split is done at the video/image_set level to avoid adding similar images from one video in training to evaluation also. 
    * Other Version Control Information - (enter, if applicable)
    
## Tool Installation: Keystroke Labeler
[Keystroke Labeler](https://github.com/WGBH-MLA/keystrokelabeler) Annotation Tool is developed in collaboration with GBH by Owen King.  
Explanation of inner parts and fields in the labeler [here](https://github.com/WGBH-MLA/keystrokelabeler/blob/main/labeler_data_readme.md)  
Please see the first link for installation and usage.  

#### Tool Access
Currently CLAMS annotators are accessing the tool via a local-host instance built through Ivanti. Each instance is one GUID/video on its own, and changing the name of the saved file is not possible nor necessary. 

## Annotation Guidelines
> [!Important]  
> Please read this explanationof the types of frames first. 
> [`Types of frames`](https://docs.google.com/document/d/1IyM_rCsCr_1XQ39j36WMX-XnVVBT4T_01j-M0eYqyDs/edit) is the guidelines for this project along with more specific instructions from this `readme.md`.   
### Preparation
The tool must be downloaded or accessed via Ivanti.  
Then still images must be extracted from chosen videos. 
A sampling rate is recommended, e.g. 1 frame every 2 seconds. 
This intends to give some diversity to the frames extracted from the video. 
The set of frames must be then loaded into the [tool](https://github.com/WGBH-MLA/keystrokelabeler/blob/main/labeler_data_readme.md). 



### What to Annotate
This tool creates an annotation file that has different columns for each frame.  
For each frame, pick which category of Frame of Interest or none.   
Then choose a subtype if needed.   
Enter the needed keystrokes, including modifier key if needed.  
In [keystroke mode](https://github.com/WGBH-MLA/keystrokelabeler/tree/main#starting-and-restarting:~:text=explicitly%20defined%20categories%22.-,Modes%3A,-The%20labeler%20has), the tool will move on to the next frame. In editor mode, you can add subtype. 

- `seen` (bool) - This attribute describes whether the annotator/tool has annotated the frame. If "seen", that piece of data can be used for ML training.  
- `type label` (char) - This is which category of Frame of Interest or none. "No label" plus "seen" is the same as not a frame of interest. 
- `subtype label` (char) - Indicates if there is a `subtype` within that Frame category/`type label`. e.g. "Slates (`type`)" can be "Handwritten (`subtype`)", or "Digital (`subtype`)" or other options. Only "Slates" currently have a `subtype`. 
- `modifier` (bool) - This indicates if there is a modifier to the `type label`. e.g. Currently the only `modifier` is "[Transitional](https://docs.google.com/document/d/1IyM_rCsCr_1XQ39j36WMX-XnVVBT4T_01j-M0eYqyDs/edit#heading=h.xnfilznsrhpe)" meaning the frame in question is fading in or out from one `type`/category to another.  

(Other columns are not used)

Other non-data-field terminology/hyper-definitions:  
- "proceed" - This means to move onto the next frame, without "seeing" it. 
- "jump factor" - Not to be confused with the already sampled rate of the frames set from the video. Now that the frame set is loaded, you can skip through the frames by using the jump factor to increase the size of step.  
- "mode" - Mode of the tool.
- "sample rate" - This is a parameter that is used before the annotation tool is ready to use. It refers to how the frame set is extracted from the video; at what sampling rate. 
- "seen-density" - This is a qualitative distinction of image sets and how annotated/labeled/seen they are. In the densely-seen `batchA`, each image from the image set is seen by an annotator and labeled. No label is synonymous with a negative-case: seen, labeled as not-of-interest. 
Conversely, `batchB` is sparesely-seen, which means that only some of the images from the image set are annotated/labeled/seen. The rest are "held out" from use in training, as they have no label whatsoever. 

The most important types to annotate are highlighted in (green) on the `types of frames` above. These should be clearly delineated from each other in the guideline. 
The subtypes of slates (blue) is also important to annotate.  
However, the non-important cases (grey) are various different negative cases that are not frames of interest. These may be similar to positive cases. These are sometimes less distinct between each other. Do the best possible, but move on if too much time is spent.  
Add the [modifier](https://docs.google.com/document/d/1IyM_rCsCr_1XQ39j36WMX-XnVVBT4T_01j-M0eYqyDs/edit#heading=h.xnfilznsrhpe) where needed. I.e. Pick the most preferred, clearest `type label`, add "Shift" when making the key combo. 

### How to Annotate It
The tool uses one key-combination press to annotate the different kinds of frames. A key combination can be a single key, or could be a combo like "Shift P". Press the relevant one to annotate the `type`. 
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
Tip2: You should stay in Editor until you get out of slates.  

### Decisions, Differentiations and Precision during Annotation
Please see the guidelines for the differentiation guide.  

#### Data Quality Efforts 
No data validation checks were conducted. 
It is assumed, due to the low difficulty of the annotation, that high accuracy of the data in one pass is reasonably plausible.

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
