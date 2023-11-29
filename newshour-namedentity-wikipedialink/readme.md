# News Hour Named Entity Wikipedia Link

## Project Overview
This project adds a wikipedia media [QID](https://en.wikipedia.org/wiki/Wikidata#:~:text=Obligatorily%2C%20an%20identifier%20(the%20QID)) link to the previous annotated dataset from the [Named Entity project](https://github.com/clamsproject/aapb-annotations/tree/main/newshour-namedentity).  
The concept is to provide an authoritative grounding to what the identification of a named entity is. 
Using Wikipedia as this authoritative source is a common practice in similar technology projects, including surfacing a Wikipedia result from Google and Siri searches.  

### Specs
* Annotation Project Name - `newshour-namedentity-wikipedialink`
* Annotator Demographics   
    * Number of annotators - 1
    * Occupational description - College Student
    * Age range - 20s
    * Education - College
* Annotation Environment Information  
    * Name: `entitylinking` tool
    * Version: [5ed0ad7](https://github.com/clamsproject/aapb-annenv-entitylinking/tree/5ed0ad7ac8504f928ca9225a5c8c50f75bb615d3)
    * Link/Tool Used/User Manual: (See below Tool Installation)  
* Project Changes -  
    * Project version: Unknown/1.0  
    * Number of batches: 1
    * Other version control information: None

## Tool Installation: ELA
Entity Link Annotator (Tool env)    
[aapb-annenv-entitylinking](https://github.com/clamsproject/aapb-annenv-entitylinking) by @marcverhagen.  
To install, see [this](https://github.com/clamsproject/aapb-annenv-entitylinking/blob/main/docs/install.md).  

## Annotation Guidelines

### Overview

Named entity linking, also known as grounding. The idea is to provide a link from a named entity to some authority. The authority we now use is [Wikipedia](https://www.wikipedia.org/), but we may introduce others, for example the [Library of Congress Authorities](https://authorities.loc.gov/). The link is provided as a property on one of the annotation types above. The annotator should have the Wikipedia main page open and type in the named entity. If this resolves to a Wikipedia article which is about the same entity as mentioned in the text, then add the wikipedia link.

Grounding is not always possible, but in a case like "Jim Lehrer was a news anchor for the PBS NewsHour on PBS" we can add a link to [https://en.wikipedia.org/wiki/Jim_Lehrer](https://en.wikipedia.org/wiki/Jim_Lehrer) for "Jim Lehrer".

> [!Important]  
> This project builds upon Named Entity Project [aka the previous project](https://github.com/clamsproject/aapb-annotations/blob/main/newshour-namedentity).  
> See the guidelines for that project for more information on what named entities are and how they were annotated. 

### Preparation
Import brat outputs (`.ann` files) from the base NE annotation project into the above tool along with the set of source files (`.txt` files). 
The `ann`-`txt` pairs must already have named entities annotated in brat.   
The NEL annotation environment will start by creating `.tab` files for collecting the annotations with duplicate entities squashed into a number. 

#### Preprocessing before Raw Annotation
The input to this annotation project was from the `newshour-namedentity` project in this repository. 
It is assumed pre-processing for raw annotation does that. 
Each file also squishes duplicate entities into one entry and writes how many times that entry appeared.
The [base-ner.url](https://github.com/clamsproject/aapb-annotations/tree/b5de0d6b48ba9835c9bf6eaacbf46019dcc12203/newshour-namedentity/golds/aapb-collaboration-21
) file seems to be the url where the transcriptions from the NAMED ENTITY project to be used for this project.   

### What to Annotate
* `Wikipedia human-searchable link` - to the correct entity described in the videos. 
### How to Annotate It
Search the web for the humanly-searchable link to the correct version of this named entity. 
Paste this into the `.tab` file or into the annotation tool to update the raw annotation. 

### Decisions, Differentiation, and Precision Level during Annotation
* **Category Disambiguation** - The disambiguation issue of the previous project becomes an even more difficult issue with this project. 
In the previous project, one could label different references from a named entity text as different categories. eg. "Washington" as an `organization`, `person`, or `location`.
In this project, once a deduplicated entry of a certain text is linked to one wikipedia link. 
The tool believes this is the only link that should match that text. 
This seems to imply an important limitation to one of the tools/processes, or an unfound way to work around this issue.

* **Only One Link Per Text!!** - A bigger issue actually stems from a feature that initially seems convenient. 
Once an annotation has been linked, any annotations within the same transcript that have the same label and spelling (case-sensitive) will be linked automatically. 
While this can be useful, that usefulness is impacted by the fact that the same word or phrase can mean different things. 
For example, "President Bush" and "the Bush administration" can refer to [George H.W. Bush senior](https://en.wikipedia.org/wiki/George_H._W._Bush) or his son [George W. Bush](https://en.wikipedia.org/wiki/George_W._Bush). 
Since there's no way to give different links to annotations that have the same label and spelling, **one set will invariably be wrong**. As far as the annotator knows, there is no workaround.

* **Lack of Authoritative Mention/Article** - Not everything mentioned in broadcasts has a wikipedia article. 
In those cases, search the web for other acceptable/wikipedia links, but when no such source exists, the annotator must simply move on.  
## Data Format and `process.py`

### `raw` data
`.tab` file where each line is a new instance of a named entity. This seems to be a [tab](https://file.org/extension/tab) spaced text file.
* Format:
```
anno_id_tag#\tdate_time_of_annotation\tsource_transcript.ann_file\tentity_text\tcategory\tduplicate_count\tWikipedia_link(normal_url)
```
* Fields: 
  * `anno_id_tag#` - entry number
  * `date_time_of_annotation` - _TODO: Unverified what this refers to_
  * `source_transcript.ann_file` - which GUID's transcript this entry comes from
  * `entity_text` - text of the named entity
  * `category` - which category it belongs to
  * `duplicate_count` - NEW, added by preprocessing before raw, how many times this entry appears probably within one transcript
  * `Wikipedia_link(normal_url)` - NEW, this is to be annotated now, the relevant human-readable/searchable link to this specific entity. 
* Example:
```
1	2022-11-10 14:38:22	cpb-aacip-507-154dn40c26-transcript.ann	ROBERT MacNEIL	person	1	https://en.wikipedia.org/wiki/Robert_MacNeil	
2	2022-11-10 14:38:54	cpb-aacip-507-154dn40c26-transcript.ann	U.S.	location	4	https://en.wikipedia.org/wiki/United_States	
3	2022-11-10 14:39:11	cpb-aacip-507-154dn40c26-transcript.ann	Health and Human Services Secretary Margaret Heckler	person	1	https://en.wikipedia.org/wiki/Margaret_Heckler	
```
> [!Note]  
> Different spellings are not considered duplicates. eg. in the [raw file](https://github.com/clamsproject/aapb-annotations/blob/main/newshour-namedentity-wikipedialink/221201-aapb-collaboration-21/annotations.tab)
line 15 is "Judy Woodruff" while line 54 is "JUDY WOODRUFF".  
> Also, see below for single link only issue.  

### [`process.py`](process.py)
_TODO: Add detail to summary._  
_TODO: get rid of `goldretriever.py` and change `process.py` to always read in local "raw" files_  
Please see the docstring of [`process.py`](process.py).   

The wikidata QID link has been automatically appended to the previous columns by `process.py`.
The gold generation process automatically adds the QID.  

### `golds` data
`.tsv` file named after the GUID of the transcript.
* Fields:
  - __guid__: The AAPB GUID of the annotated transcript. (_string_)
  - __anno_id__: The text-bound annotation ID, in other words, the entry number. (_string_)
  - __type__: The entity category-- person, location, event, organization, title (_string_)
  - __begin_offset__: The character offset beginning the text span. (_int_)
  - __end_offset__: The character offset ending the text span. (_int_)
  - __text__: The entity. (_string_)
  - __type__: The entity category. (_string_)
  - __wiki_url__: The Wikipedia URL grounding the entity. (_string_)
  - __qid__: The Wikidata URI linking the entity via Q identifier. (_string_)  
* Example:
```
guid	anno_id (tag)	type	begin_offset	end_offset	text	wiki_url	qid
cpb-aacip-507-1v5bc3tf81-transcript.ann	T1	person	2	12	JIM LEHRER	https://en.wikipedia.org/wiki/Jim_Lehrer	https://www.wikidata.org/wiki/Q931148
cpb-aacip-507-1v5bc3tf81-transcript.ann	T2	person	32	42	Jim Lehrer	https://en.wikipedia.org/wiki/Jim_Lehrer	https://www.wikidata.org/wiki/Q931148
cpb-aacip-507-1v5bc3tf81-transcript.ann	T3	title	51	59	NewsHour	https://en.wikipedia.org/wiki/PBS_NewsHour	https://www.wikidata.org/wiki/Q7118447
```

## Evaluation Information
A number of [evaluations](https://github.com/clamsproject/aapb-evaluations/tree/main/nel_eval) of NEL tools have been done. 
For the purposes of evaluation, the subtypes of the 'title' category are collapsed into one group.  
