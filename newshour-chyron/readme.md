[CLAMS.ai](clams.ai) team  
Original Author: Gabriel Michael Alexander, Annotator @gmalexander29  
Editor: Jeremy Huey, Data Annotation Manager @jarumihooi
readme.md: version b.b - this version still requires "Gold Generation and Dependencies - Codebase"  
08/28/2023
# Chyrons

## Goal of the Project
This project provides a dataset used for the detection of chyrons/banner-text that appears onscreen in video media.  
[chyron definition](https://www.merriam-webster.com/dictionary/chyron) - a caption superimposed over *usually* the lower part of a video image (as during a news broadcast). Note, not neccesarily lower third. Sometimes they are temporary and will fade/blink in and out.  Named after the company that made this technology. aka: the text that appears under people during broadcasts.  
### Project Information
```
Annotation project name - Newshour Chyron
Annotator Demographics (1) -  
Gabriel Michael Alexander (College student age, (other demographic information), Lang: Eng US native speaker, Organization: GBH)  
Annotation Environment information -    
    Name: VIA  
    Version: Unknown  
    Link/Tool Used/User Manual: (See below Tool Installation)  
Project changes -  
    Project Version: Unknown/1.0  
    Number of Batches: 1, (The batch is named batch2 - needs further investigation.)
    Other Version Control Information: None  
```

### Data Overview
INPUT - The annotator watches a video using the annotation tool, and marks the start and end times of when chyrons appear plus the text included within the chyron.  
INTERMEDIATE RAW OUTPUT - `.json` file of the annotations. (See the [file](https://github.com/clamsproject/aapb-annotations/blob/feaf342477fc27e57dcdcbb74c067aba4a02e40d/newshour-chyron/220701-batch2/3a054b38_18Jul2022_16h18m12s.json) for format.)   
FINAL PREPARED GOLD OUTPUT - `.csv` file of which chyrons appear within one GUID/media. Ready for software ingestion.  
```
FORMAT & EXAMPLE:
start_time  end_time    text  
1162.43976  1168.06476  MATHILDE KRIM, PhD.\nAIDS Medical Foundation  
275.7771    279.7771    JOHN BLOCK\nSecretary of Agriculture  
923.5271    927.5271    "ROBERT"  
```
_TODO: Standardization within the project will see the time formats become consistent. See below Decisions and Details for more information._  

## Annotation Guidelines: Chyron Text + Times
### Tool Installation: VIA tool
_The following section is recalled from memory and may not be fully accurate._  
[VIA3](https://www.robots.ox.ac.uk/~vgg/software/via/). This project used [this version](https://github.com/kelleyl/clams-via3/blob/master/app.py#L16) and the Video Annotator tool.  
A video must be imported. Docker is likely used.  


### What to Annotate
Usually, chyrons will fade in and out.  
**START TIME** - When a chyron has fully appeared/solid and is no longer see through, pause the video and highlight the chyron via a bounding box. It's not too dissimilar from taking a screenshot.  
**TEXT** - When the chyron is highlighted, double-click it and in the DESCRIPTION box, copy/write out what was said in the chyron exactly as it was displayed. When a chyron consists of more than one line, use the enter/return key (becomes \n in the gold output) to make a new line in the description.  
**END TIME** - After that, submit how long the chyron was onscreen: annotating the end time as when it begins to become transparent.  
_Time format: (sec.ten-thousandths of sec)_   

### Decisions and Differentiations during Annotation
The decisions within the annotation process are described above.  
The only known issue is time format.  
First, the time format is a todo to be standardized along the aapb-annotations repository. This includes choosing one format and using that format for all gold annotation formatting and the use of that formatting within the tools/evaluations/software that ingests the gold annotation.  
The most probable choice will be some sort of floating point notation of division of seconds, eg. 100th of a second xx:xx or ten-thousandth of a second xx:xxxx.  The reason is to avoid a mechanical propagation to an extreme extent.
  
**PRECISION ISSUE WITH TIME** - However, one must account for lack of granularity in the annotator's creation. Even at slower speeds, precise accuracy beyond .1-.2sec may be suspect. We notice in the project data here has divisions of seconds of ".5271, .7771, .2371". We assume this is basically some default in the machine and that granularity of the annotation beyond xx.x is not recorded in the data.  
  
_TODO: This gold annotation should be updated to use the standard format WITH A COLON._  

## Gold Generation and Dependencies - Codebase
_TODO: to be added_
