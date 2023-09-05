[CLAMS.ai](https://clams.ai/) team  
Author: Jeremy Huey, Data Annotation Manager @jarumihooi  
Annotator: Gabriel Michael Alexander, Annotator  
readme.md: version a.a - this version still requires gold generation information update.   
09/01/2023  
# News Hour Named Entity Wikipedia Link

## Goal of the Project
This project adds a wikipedia media [QID](https://en.wikipedia.org/wiki/Wikidata#:~:text=Obligatorily%2C%20an%20identifier%20(the%20QID)) link to the previous annotated dataset from the [Named Entity project](https://github.com/clamsproject/aapb-annotations/tree/main/newshour-namedentity).  
The concept is to provide an authoritative grounding to what the identification of a named entity is. 
Using Wikipedia as this authoritative source is a common practice in similar technology projects, including surfacing a Wikipedia result from Google and Siri searches.  

### Project Information
```
Annotation project name - NewsHour Named Entity Wikipedia Link
Annotator Demographics (1) -  
Gabriel Michael Alexander (College student age, (other demographic information), Lang: Eng US native speaker, Organization: GBH)  
Annotation Environment information -    
    Name: Brat  
    Version: Unknown  
    Link/Tool Used/User Manual: (See below Tool Installation)  
Project changes -  
    Project Version: Unknown/1.0  
    Number of Batches: 1
    Other Version Control Information: None
```

### Data Overview
INPUT - `transcript that has already had named entities annotated in brat`. _TODO: What are the file formats required for the transcripts to import into brat?_  
INTERMEDIATE RAW OUTPUT - `.tab` file where each line is a new instance of a named entity. This seems to be a tab spaced text file. 
Each file also squishes duplicate entities into one entry and writes how many times that entry appeared.
_TODO: What is the [base-ner.url](https://github.com/clamsproject/aapb-annotations/tree/b5de0d6b48ba9835c9bf6eaacbf46019dcc12203/newshour-namedentity/golds/aapb-collaboration-21
) used for? It seems to be a dependency/reference for something._  
Note, different spellings are not considered duplicates. eg. in the [raw file](https://github.com/clamsproject/aapb-annotations/blob/main/newshour-namedentity-wikipedialink/221201-aapb-collaboration-21/annotations.tab)
line 15 is "Judy Woodruff" while line 54 is "JUDY WOODRUFF".
Note2, see below for single link only issue.  
```
FORMAT:
anno_id_tag#\tdate_time_of_annotation\tsource_transcript.ann_file\tentity_text\tcategory\tduplicate_count\tWikipedia_link(normal_url)
```
```
EXAMPLE:
1	2022-11-10 14:38:22	cpb-aacip-507-154dn40c26-transcript.ann	ROBERT MacNEIL	person	1	https://en.wikipedia.org/wiki/Robert_MacNeil	
2	2022-11-10 14:38:54	cpb-aacip-507-154dn40c26-transcript.ann	U.S.	location	4	https://en.wikipedia.org/wiki/United_States	
3	2022-11-10 14:39:11	cpb-aacip-507-154dn40c26-transcript.ann	Health and Human Services Secretary Margaret Heckler	person	1	https://en.wikipedia.org/wiki/Margaret_Heckler	
```
FINAL PREPARED GOLD OUTPUT - `.tsv` file named after the GUID of the transcript.  
The wikidata QID link has been automatically added by `process.py`.
```
FORMAT & EXAMPLE:
guid	anno_id(tag)	type	begin_offset	end_offset	text	wiki_url	qid
cpb-aacip-507-1v5bc3tf81-transcript.ann	T1	person	2	12	JIM LEHRER	https://en.wikipedia.org/wiki/Jim_Lehrer	https://www.wikidata.org/wiki/Q931148
cpb-aacip-507-1v5bc3tf81-transcript.ann	T2	person	32	42	Jim Lehrer	https://en.wikipedia.org/wiki/Jim_Lehrer	https://www.wikidata.org/wiki/Q931148
cpb-aacip-507-1v5bc3tf81-transcript.ann	T3	title	51	59	NewsHour	https://en.wikipedia.org/wiki/PBS_NewsHour	https://www.wikidata.org/wiki/Q7118447
```

## Tool Installation: Brat
brat rapid annotation tool    
[Brat and Installation Instructions](https://brat.nlplab.org/index.html)   
TODO: Find the specific usage of the tool.  

## Annotation Guidelines: Transcribing/Closed Captioning
This project builds upon Named Entity Project [aka the previous project](https://github.com/clamsproject/aapb-annotations/blob/main/newshour-namedentity/guidelines.md).
The `guidelines.md` for [this project](https://github.com/clamsproject/aapb-annotations/blob/main/newshour-namedentity-wikipedialink/guidelines.md) is currently an exact copy of the one previous. 
### Preparation
Import the transcripts through brat. This tool seems to require a mouse.  
### Process of Annotating
**Wikipedia Link** - Search the web for the humanly-findable link to the correct version of this named entity. _TODO: add how this is added to the annotation._   

### Decisions and Differentiations during Annotation
**Category Disambiguation** - The disambiguation issue of the previous project becomes an even more difficult issue with this project. 
In the previous project, one could label different references from a named entity text as different categories. eg. "Washington" as an `organization`, `person`, or `location`.
In this project, once a deduplicated entry of a certain text is linked to one wikipedia link. 
The tool believes this is the only link that should match that text. 
This seems to imply an important limitation to the brat tool or an unfound way to work around this issue.  
  
**Lack of Authoritative Mention/Article** - Not everything mentioned in broadcasts has a wikipedia article. 
In those cases, search the web for other acceptable/wikipedia links, but when no such source exists, the annotator must simply move on.  

**Only One Link Per Text!!** - A bigger issue actually stems from a feature that initially seems convenient. 
Once an annotation has been linked, any annotations within the same transcript that have the same label and spelling (case-sensitive) will be linked automatically. 
While this can be useful, that usefulness is impacted by the fact that the same word or phrase can mean different things. 
For example, "President Bush" and "the Bush administration" can refer to [George H.W. Bush senior](https://en.wikipedia.org/wiki/George_H._W._Bush) or his son [George W. Bush](https://en.wikipedia.org/wiki/George_W._Bush). 
Since there's no way to give different links to annotations that have the same label and spelling, **one set will invariably be wrong**. As far as the annotator knows, there is no workaround.

## Gold Generation and Dependencies - Codebase
The input to this annotation project was from the `newshour-namedentity` annotation project in this repository. 
It is assumed either the brat tool handles the deduplication or a pre-processing for preparation into this project does that. 
The `golds` directory contains the public gold dataset, generated using `process.py`. 
Gold files are in `.tsv` format. The relevant data fields are summarized below:

`FORMAT:`
- __guid__: The AAPB GUID of the annotated transcript. (_string_)
- __anno_id__: The text-bound annotation ID. (_string_)
- __type__: The entity category-- person, location, event, organization, title (_string_)
- __begin_offset__: The character offset beginning the text span. (_int_)
- __end_offset__: The character offset ending the text span. (_int_)
- __text__: The entity. (_string_)
- __type__: The entity category. (_string_)
- __wiki_url__: The Wikipedia URL grounding the entity. (_string_)
- __qid__: The Wikidata URI linking the entity via Q identifier. (_string_)  
  
The gold generation process automatically adds the QID.  
Note: for purposes of evaluation, the subtypes of the 'title' category are collapsed into one group.  

_TODO: Provide more information about the process._   