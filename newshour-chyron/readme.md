# Chyrons

## Goal of the Project
This project provides a dataset used for the detection of chyrons/banner-text that appears onscreen in video media.  
[Chyron](https://www.merriam-webster.com/dictionary/chyron) - a caption superimposed over *usually* the lower part of a video image (as during a news broadcast). Note, not neccesarily lower third. Sometimes they are temporary and will fade/blink in and out. 
Named after the company that made this technology. aka: the text that appears under people during broadcasts.  
### Project Information
```
Annotation project name - newshour-chyron
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
INPUT - The annotator watches a video using the annotation tool, and labels chyrons in time.  
INTERMEDIATE RAW OUTPUT - `.json` file of the annotations.  
(See the [file](https://github.com/clamsproject/aapb-annotations/blob/feaf342477fc27e57dcdcbb74c067aba4a02e40d/newshour-chyron/220701-batch2/3a054b38_18Jul2022_16h18m12s.json) for format.)   
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

### Decisions, Differentiations, and Precision during Annotation
The decisions within the annotation process are described above.  
One issue is time format.  
First, the time format is to be standardized along the aapb-annotations repository. This includes choosing one format and using that format for all gold annotation formatting and the use of that formatting within the tools/evaluations/software that ingests the gold annotation.  
The choice is `hr:mn:sc.msc`. 
  
**Time Precision** - There is some lack of granularity in the annotator's creation. Even at slower speeds, precise accuracy beyond .1-.2sec is suspect. 
The project data here has divisions of seconds of ".5271, .7771, .2371". 
It is assumed this is some default in the tool and that precision of the annotation beyond xx.x is not in the data.  
_TODO: This gold annotation should be updated to use the standard format WITH A DOT._  

## Gold Generation and Dependencies - Codebase
_TODO: to be added_
