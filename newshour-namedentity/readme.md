# NewsHour Named Entity

## Project Overview
The namedentity project creates a dataset of the [named entities](https://www.techtarget.com/searchbusinessanalytics/definition/named-entity#:~:text=In%20data%20mining%2C%20a%20named,phone%20numbers%2C%20companies%20and%20addresses.) 
that appeared in the transcripts of old news broadcasts. Named Entities are used in Natural Language Processing to identify named subjects of interest from media. 
This dataset provides a learnable dataset of what named entities  are specifically found in a piece of media, which can aid in the automatic searching for other named entities in other media or other language processing after finding those named entities.
For CLAMS, one use case is to extract these named entities as metadata tags, allowing for quicker searching of topics or keywords from within videos. (E.g. Someone searching for President Jimmy Carter with the AAPB collection via text search.)  
  
The namedentity project was the first annotation project annotated for GBH. It precedes the namedentitywiki project which builds on this.  

### Specs
* Annotation Project Name - `newshour-namedentity`
* Annotator Demographics 
    * Number of annotators - 1
    * Occupational description - College student
    * Age range - 20s
    * Education - College
* Annotation Environment Information
    * Name - Brat
    * Version - Unknown
    * Tool documentation - (see below tool installation)
* Project Changes
    * Number of batches - 1
    * Other version control information - None
    
## Tool Installation: Brat
brat rapid annotation tool    
[Brat and Installation Instructions](https://brat.nlplab.org/index.html)    

## Annotation Guidelines
> [!Important]  
> **PLEASE FIRST SEE the `guidelines.md` [for this project](https://github.com/clamsproject/aapb-annotations/blob/main/newshour-namedentity/guidelines.md) for the general guidelines and differentiations!** 
> After that, this `readme.md` has more specific instructions for this project.   

### Preparation
Import the transcripts through brat. This tool seems to require a mouse.   
INPUT - transcripts in `.txt` format that match the audio or other information in a video.  
### What to Annotate
* **Named Entity Phrase Text** - Text that symbolizes the whole named entity. Labelling is done by highlighting words or phrases.  
* **Category** - Which category of entity is this an example of. Right click to categorize the highlighted phrase. 
Options include `person, organization, program_title, publication_title, product, location, & event`.  
* _**Character Start Offset** & **Character End Offset** - These two numbers entail which chars in the text file span the named entity's text. 
This information is **automatically added** to the raw dataset file by the brat tool. 
e.g. "Jim Lehrer" spans from character 32 inclusive to character 42 exclusive, taking up 10 letters. The first character of a file is 0._    
* _(Note, Wikipedia link is not used in this project. It's used in the [next project](https://github.com/clamsproject/aapb-annotations/tree/main/newshour-namedentity-wikipedialink).)_ 
### How to Annotate It
(See Above)
### Decisions, Differentiation, and Precision Level during Annotation
* **Category Disambiguation** - While this process is relatively straightforward, there are times when it can be difficult to place an item under one category umbrella. 
For example, "Washington" can refer to the person, US capital, the organization within it, or the northwestern state. 
A similar issue can arise with colleges, many of whom are named after the state or city they're located in. In these cases, context is key. 
A relatively reliable rule of thumb is, if a location is mentioned, but no politicians or professors are brought up, then file it under location. Otherwise, file it under organization.  

* **Transcript Match** - Annotation Leads and Project Managers should ensure the transcripts accurately reflect the video that they are supposed to match before annotators begin.  
Please also consider whether the transcripts and labelling should label only spoken text or also extraneous script information such as the name of who is speaking, non-spoken information, etc. 

* **General Typos** - As with any labelling with text, there is a possibility of typos. Data Quality checks such as for typos have not been done on these datasets.  

## Data Format and `process.py`
### `raw` data
`.ann` file where each line is a new instance of a named entity. Information on the `.ann` [file format](https://brat.nlplab.org/standoff.html) is here. 
* Fields:
    * `category` - which type of named entity the text is. 
    * `first_character` - first char that starts the text string within the transcript, inclusive. The first character of a file is 0.
    * `last_character` - last char of the text string in the transcript, exclusive. 
    * `entity_text` - what the text of the named entity is. 
* Format:
```
tag#\tcategory first_character last_character\tentity_text
```
* Example:
```
T1	person 2 12	JIM LEHRER
T2	person 32 42	Jim Lehrer
T3	program_title 51 59	NewsHour
```
### [`process.py`](process.py)
Historically, the `process.py` used for this project simply copies the `.ann` files from the raw directory into new directories based on batches for the golds.
This is done by requesting `.ann` as the format during the running of the `process.py`. 
This script can also convert the `.ann` files to other formats and to create `.mmif`. 

The other code files (`anntoconll.py`, `sentencesplit.py`, `ssplit.py`, `sspostproc.py`) in this repository were copied from the brat repository for conversion into other formats such as `.conll.tsv`. 

Please see the docstring of [`process.py`](process.py) for further information. 

### `golds` data
exact same `.ann` file again.  
* Fields:  
    * (See Above)
* Example:  
    * (See Above)
