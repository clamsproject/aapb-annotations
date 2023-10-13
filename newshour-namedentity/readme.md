# News Hour Named Entity

## Project Overview
The namedentity project creates a dataset of the [named entities](https://www.techtarget.com/searchbusinessanalytics/definition/named-entity#:~:text=In%20data%20mining%2C%20a%20named,phone%20numbers%2C%20companies%20and%20addresses.) 
that appeared in the transcripts of old news broadcasts. Named Entities are used in Natural Language Processing to identify named subjects of interest from media. 
This dataset provides a learnable dataset of what named entities  are specifically found in a piece of media, which can aid in the automatic searching for other named entities in other media or other language processing after finding those named entities.
For CLAMS, one use case is to extract these named entities as metadata tags, allowing for quicker searching of topics or keywords from within videos. (E.g. Someone searching for President Jimmy Carter with the AAPB collection via text search.)  
  
The namedentity project was the first annotation project Gabe annotated for WGBH. It precedes the namedentitywiki project which builds on this.  

### Specs
* Annotation project name - `newshour-namedentity`
* Annotator Demographics 
    * Number of annotators - 1
    * Occupational description - College student
    * Age range - 20s
    * Education - College
* Annotation Environment information
    * Name - (enter)
    * Version - (enter)
    * Tool Documentation - (see below tool installation)
* Project changes
    * Number of Batches - (enter)
    * Other Version Control Information - (enter, if applicable)
Gabriel Michael Alexander (College student age, (other demographic information), Lang: Eng US native speaker, Organization: GBH)  
Annotation Environment information -    
    Name: Brat  
    Version: Unknown  
    Link/Tool Used/User Manual: (See below Tool Installation)  
Project changes -  
    Project Version: Unknown/1.0  
    Number of Batches: 1
    Other Version Control Information: None


### Data Overview
INPUT - transcripts in `.txt` format that match the audio or other information in a video.   
INTERMEDIATE RAW OUTPUT - `.ann` file where each line is a new instance of a named entity. 
```
FORMAT:
tag#\tcategory first_character last_character\tentity_text
```
```
EXAMPLE:
T1	person 2 12	JIM LEHRER
T2	person 32 42	Jim Lehrer
T3	program_title 51 59	NewsHour
```
FINAL PREPARED GOLD OUTPUT - same `.ann` file again.  
```
the raw .ann file is directly copied for gold.
```
Information on the `.ann` [file format](https://brat.nlplab.org/standoff.html) is here.  

## Tool Installation: Brat
brat rapid annotation tool    
[Brat and Installation Instructions](https://brat.nlplab.org/index.html)   
_TODO: Find the specific usage of the tool._  

## Annotation Guidelines: Transcribing/Closed Captioning
> **PLEASE FIRST SEE the `guidelines.md` [for this project](https://github.com/clamsproject/aapb-annotations/blob/main/newshour-namedentity/guidelines.md) for the general guidelines and differentiations!**
### Preparation
Import the transcripts through brat. This tool seems to require a mouse.  
### Process of Annotating
**Named Entity Phrase Text** - After importing the transcripts through brat, annotation is done by highlighting words or phrases.  
**Category** - Then right click to categorize the highlighted phrase. 
Options include `person, organization, program_title, publication_title, product, location, & event`.  
**Character Start Offset** & **Character End Offset** - These two numbers entail which chars in the text file span the named entity's text. 
This information is automatically added to the raw dataset file by the brat tool. 
e.g. "Jim Lehrer" spans from character 32 inclusive to character 42 exclusive, taking up 10 letters. The first character of a file is 0.    
_(Note, Wikipedia link is not used in this project. It's used in the [next project](https://github.com/clamsproject/aapb-annotations/tree/main/newshour-namedentity-wikipedialink).)_

### Decisions, Differentiations, and Precision during Annotation
**Category Disambiguation** - While this process is relatively straightforward, there are times when it can be difficult to place an item under one category umbrella. 
For example, Washington can refer to the US capital, the organization within it, or the northwestern state. 
A similar issue can arise with colleges, many of whom are named after the state or city they're located in. In these cases, context is key. 
A relatively reliable rule of thumb is, if a location is mentioned, but no politicians or professors are brought up, then file it under location. Otherwise, file it under organization. 
Aside from that, this annotation does not tend to be too demanding.  

**Transcript Match** - Please ensure the transcripts accurately reflect the video that they are supposed to match.  
Please also consider whether the transcripts and labelling should label only spoken text or also extraneous script information such as the name of who is speaking, non-spoken information, etc. 

**General Typos** - As with anything with text, there is a possibility of typos. Data Quality checks such as for typos have not been done either dataset.  

## Gold Generation and Dependencies - Codebase
_TODO: to be added_  
_TODO (discrepancy): It seems that the process.py information to transform from raw to gold is no longer needed. This requires continued investigation. If the process here is not necessary, it should be deleted._
