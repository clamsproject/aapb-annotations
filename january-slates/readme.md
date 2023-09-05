[CLAMS.ai](https://clams.ai/) team  
Author: Jeremy Huey, Data Annotation Manager @jarumihooi  
Annotators: Unknown (GBH), Samantha Driscoll (GBH)
Slates readme.md: version a.a - this version still requires gold generation information.   
09/02/2023
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
Annotation project name - January Slates
Annotator Demographics (2) -  
Unknown (Unknown age, (other demographic information), Lang: Unknown, Organization: GBH)  
Samantha Driscoll (Working Professional age, (other demographic information), Lang: Eng US native speaker, Organization: GBH)  
Annotation Environment information -    
    Name: TODO - Unknown  
    Version: Unknown  
    Link/Tool Used/User Manual: (See below Tool Installation)  
Project changes -  
    Project Version: Unknown/1.0  
    Number of Batches: 1
    Other Version Control Information: None
```

### Data Overview
INPUT - a set of video files to be annotated. _TODO: Which tool?_   
INTERMEDIATE RAW OUTPUT - `.csv` file where each line is the time of when the slate frames appear in that video. 
```
FORMAT:
GUID,",","Series/Group              ,","Slate Start ,","Slate End   ,","Writing Types,",Recorded/Digital,,,",",format of most of the information,",",Anything moving on screen during slate?,
Note the extra commas added in and extra blank columns and extra space within the column names. 
```
```
EXAMPLE:
cpb-aacip-81-881jx33t,",","Woman                     ,","00:00:00;00 ,","00:00:05;04 ,","handwriting  ,",recorded,,,",",boxes to fill in,",",no,
cpb-aacip-41-34fn32g7,",","Carolina Journal          ,","00:00:00;00 ,","00:00:14;28 ,","typed        ,",digital?,,,",",key-value pairs,",",countdown,
```
FINAL PREPARED GOLD OUTPUT - `.tsv` file that seems to be actually comma-separated anyway. The gold files conform to the repository readme guideline that each 
gold must relate to only one GUID. Therefore, each of these gold files is only 1 video/GUID each. Note: the column headers are added to each file.  
```
FORMAT & EXAMPLE:
GUID,Series/Group,Slate Start,Slate End,Writing Types,Recorded/Digital,format of most of the information,Anything moving on screen during slate?
cpb-aacip-29-01pg4g2x,Prime Time Wisconsin,00:00:00;00,00:00:08;14,typed,digital,key-value pairs,no
```

## Tool Installation: Unknown
_TODO: Tool used is unknown. Follow up questions with Sammy should illuminate this._

## Annotation Guidelines: Transcribing/Closed Captioning
_What guidelines were used for this?_
### Preparation
Multiple videos must be prepared for annotation.  
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
* Recorded/Digital - _unknown what this column pertains to_  
* (empty)  
* (empty)  
* (comma)  
* format of most of the information - visually how is the textual information presented in the slate? e.g. "boxes to fill in", "key-value pairs", "free text"  
* (comma)  
* Anything moving on screen during slate? - are there things like animations and other things that are moving during the slate information

_Note: in some columns there is a comma within the raw value of the column._

### Decisions and Differentiations during Annotation
**What denotes start and end** - Decisions as to what exactly constitutes the start and end of the slate times is unknown. Is it when it first starts fading in, or when its fully done fading? 

**Errors in the raw** - There are errors in the raw format, notably, in `CLAMS_slate_annotation_metadata.csv` line 203 "cpb-aacip-394-150gbd75", column(Writing Types F) is a typo "typeed" instead of "typed". 
Further work should be done to check for other errors of this type. A bash script search would likely need to be run to find out if that error made it into the gold format `.tsv` files also.

**Time format check** - It is not fully verified what the time format is, however the assumption is as above since the highest last number goes up to 29.
Yet another typo seems to appear however in two cases of numbers like this: `CLAMS_slate_annotation_metadata.csv` line 77 Slate End "00:00:27;110,",
`CLAMS_slate_annotation_metadata.csv` line 97 Slate Start "00:00:05;119,", 

**Time format change** - At around line203 or 202 is a note that "sammy started annotating here.". 
Shift of time format to only 3 numbers: "xx:xx:xx" assumptively "mn:sc:fr"(?).  

**No slate** - there are valid instances where a video does not have slate information shown within the actual video. Annotate as "no slate" in both Slate Start and Slate End.  

**Skip to new material in raw** - The raw `.csv` file also has an area that is skipped and annotation moved onto new/different videos. 
It starts at line 624 and it resumes at line 1409. This might be because all of those GUIDs are the same and more variety in the dataset was needed for better results.
Annotation by Sammy paused/ended with line 1672 being the last annotated row.  

## Gold Generation and Dependencies - Codebase
`requirements.txt` for running the codebase is stored here.  
_TODO: to be added_