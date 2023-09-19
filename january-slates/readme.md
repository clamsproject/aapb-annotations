# Slates

## Goal of the Project
What is a film slate? - "The term film slate is still used to reference the clapper board that appears on the screen when filming. Just like early clappers. 
The slate is shown at the beginning of a take immediately prior to the commencement of action." - [Beverly Boy Productions](https://beverlyboy.com/filmmaking/what-does-slate-mean-in-film/#:~:text=The%20term%20film%20slate%20is,the%20term%20slate%20in%20film.).  
[More information about slates](https://www.youtube.com/watch?v=Heg6kDxXZ8k&t=13).  
[What goes on a slate](theblackandblue.com/2012/11/05/deciphering-film-slate-1/).  
This project creates a dataset that annotates where informational frames about the video are located timewise from many videos/GUIDs. 
This dataset is needed to power automatic detection of slate information in the video collection at the AAPB. 
Many of the collection pieces have incomplete or unverified information about what the video is. 
This detected information could be used to verify and update metadata about that collection piece.

### Project Information
```
Annotation project name - january-slates
Annotator Demographics (2) - Public Broadcasting Organization Media Librarians and Volunteers, age range 20-30, college or masters education  
Annotation Environment information -    
    Name: Manual google sheets entry + AAPB video viewer + unknown video viewer with frame time 
    Version: n/a  
    Link/Tool Used/User Manual: (See below Tool Installation)  
Project changes -  
    Project Version: Unknown/1.0  
    Number of Batches: 1
    Other Version Control Information: None
```

### Data Overview
* INPUT - a set of video files to be annotated, preferably openable in mass in a video viewer/tool that has some fraction of a second denomination.  
* INTERMEDIATE RAW OUTPUT - `.csv` file where each line is the time of when the slate frames appear in that video.
  * Format  
    * Fields: ```GUID,",","Series/Group              ,","Slate Start ,","Slate End   ,","Writing Types,",Recorded/Digital,,,",",format of most of the information,",",Anything moving on screen during slate?,```  
    [!Note] there are extra commas added in and extra blank columns and extra space within the column names.
    * Example:
        ```
        cpb-aacip-81-881jx33t,",","Woman                     ,","00:00:00;00 ,","00:00:05;04 ,","handwriting  ,",recorded,,,",",boxes to fill in,",",no,
        cpb-aacip-41-34fn32g7,",","Carolina Journal          ,","00:00:00;00 ,","00:00:14;28 ,","typed        ,",digital?,,,",",key-value pairs,",",countdown,
        ```
* FINAL PREPARED GOLD OUTPUT - `.tsv` file that seems to be actually comma-separated anyway. The gold files conform to the repository readme guideline that each 
gold must relate to only one GUID. Therefore, each of these gold files is only 1 video/GUID each. 
  * Format
    * Fields: `GUID,Series/Group,Slate Start,Slate End,Writing Types,Recorded/Digital,format of most of the information,Anything moving on screen during slate?`
    * Example:
    ```
    GUID,Series/Group,Slate Start,Slate End,Writing Types,Recorded/Digital,format of most of the information,Anything moving on screen during slate?
    cpb-aacip-29-01pg4g2x,Prime Time Wisconsin,00:00:00;00,00:00:08;14,typed,digital,key-value pairs,no
    ```
    [!Note] Each file has the column header in it. 

## Tool Installation: None
This annotation was done manually by entering information into a Google Sheet. 
Multiple videos were prepared or downloaded or were accessed from an AAPB terminal. 
Videos were opened in the AAPB viewer or in some unknown tool that had time information up to division by 30 frames per second.  

## Annotation Guidelines: Transcribing/Closed Captioning
For a quick overview of [slate types](https://docs.google.com/document/d/1Xf43EpVzQbIOB-7KTadEyU3eam9xIvLlSGkjy4Ff2v4/edit) please see this.  
The verbal guidelines for this project were to annotate as a superinterval/superset times the slate appeared, and details about its appearance.  
### Preparation
A google sheet must be prepared to annotate the below columns.  
Multiple videos must be prepared to be opened for annotation.  
### Process of Annotating

Per column:  
* GUID - the AAPB id for that video e.g. "cpb-aacip-81-881jx33t". 
CPB is the [Corporation for Public Broadcasting](https://cpb.org/faq#1-1:~:text=Public%20Broadcasting%20(CPB)%3F-,CPB,-is%20a%20private).
"aacip" is likely a collection name (unverified).
The first number seems to be series number. Eg. 81 is "Woman", and "29" is both Prime Time Wisconsin" and "Wisconsin Week".
The final number which includes letters is the unique guid number.  
* (comma) - column of commas: ","  
* Series/Group              ,- what tv series or group this video belongs to.  
* Slate Start ,- When the slate starts appearing. (See Decisions). Format likely "hr:mn:se:fr" out of 30 fps.     
* Slate End   ,- When the slate stops being shown on screen. (See Decisions)  
* Writing Types,- Slates contain written information. Much of this material is from the early days of tv. eg. "handwritten", "typed" or "other"   
* Recorded/Digital - _TODO:unknown what this column pertains to_  
* (empty)  
* (empty)  
* (comma)  
* format of most of the information - visually how is the textual information presented in the slate? e.g. "boxes to fill in", "key-value pairs", "free text"  
* (comma)  
* Anything moving on screen during slate? - are there things like animations and other things that are moving during the slate information

_Note: in some columns there is a comma within the raw value of the column._

### Decisions, Differentiations, and Precision during Annotation
**What denotes start and end** - This project was done with the annotation time as a superinterval.
This means the annotation will begin on a time/frame without the slate where possible (or 00:00:00.000) 
and is annotated as ending after the slate has disappeared.
(This is currently unvalidated.)
> [!Note]  
>  This is opposite to the decision made in the January Chyrons project. 

**Errors in the raw** - There are errors in the raw format, notably, in `CLAMS_slate_annotation_metadata.csv` [line 203](https://github.com/clamsproject/aapb-annotations/blob/f884e10d0b9d4b1d68e294d83c6e838528d2c249/january-slates/230101-aapb-collaboration-7/CLAMS_slate_annotation_metadata.csv?plain=1#L203) "cpb-aacip-394-150gbd75", column(Writing Types F) is a typo "typeed" instead of "typed". 
Further work should be done to check for other errors of this type. A bash script search would likely need to be run to find out if that error made it into the gold format `.tsv` files also.

**Time format non-conformant** - This is an older project. The time format does not conform to ISO 8601 `hr:mn:sc.msc` yet.

**Time format typos** - A typo seems to appear however in two cases of numbers like this: `CLAMS_slate_annotation_metadata.csv` line 77 Slate End "00:00:27;110,",
`CLAMS_slate_annotation_metadata.csv` line 97 Slate Start "00:00:05;119,", 

**Time format change** - At around line203 is a note that "sammy started annotating here.". 
Shift of time format to only 3 numbers: "xx:xx:xx". This is confirmed as hh:mm:ss (no frames!) since the AAPB viewer used did not
offer frame precision. 

**No slate** - there are valid instances where a video does not have slate information shown within the actual video. Annotate as "no slate" in both Slate Start and Slate End.  

**Skip to new material in raw** - The raw `.csv` file also has an area that is skipped and annotation moved onto new/different videos. 
It starts at line 624 and it resumes at line 1409. This might be because all of those GUIDs are the same and more variety in the dataset was needed for better results.
Annotation by Sammy paused/ended with line 1672 being the last annotated row.  

**Time Precision** - Because of the time format change, it should be assumed that the numbers without frames is only precise down to the second.
The precision of the other annotations with frame precision is unverified. 



## Gold Generation and Dependencies - Codebase
`requirements.txt` for running the codebase is stored here.  
_TODO: to be added_

## Evaluation Dataset   
> [Evaluation dataset](https://docs.google.com/spreadsheets/d/1VHEpYmAtBHkIHTzbYtUexRNqALEHLi-3rwzIXtfQG-E/edit#gid=0)  
 
In 2020, an evaluation of the performance of the slates app tool was done by GBH. This is the result of it, comparing the output 
prediction of the app to the judgment of a human annotator. 