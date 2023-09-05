[CLAMS.ai](https://clams.ai/) team   
Author: Jeremy Huey, Data Annotation Manager @jarumihooi  
Project Manager: Keigh Rim @keighrim  
aapb-annotations-readme version b.b  
08/28/2023

# AAPB-CLAMS Annotation Repository
## Project Information
> This repository contains datasets from manual annotation projects in [AAPB](https://americanarchive.org/) - [CLAMS](https://clams.ai) collaboration.

AAPB has involved the CLAMS team in a collaboration to develop archiving technology for public media (primarily video and audio from publically-funded tv shows and radio broadcasts). This will facilitate the research and preservation of significant historical content from such media.  
The process of archiving, summarizing and extracting-metadata from this media could eventually be automatic.  
This repository/endeavor provides training and evaluation data for the Computer Vision and Machine Learning tools in this process.  
Data collected is used to evaluate the success of the tools. Then, the tools will be trained on larger batches of data to automatically retrieve information important to the archival process.

## Structure of This Repository/Directory
 - `batches` subdirectory (1)
 - project subdirectories (5)
 - this repository's `readme.md`

### Batches Subdirectory 
The first directory is the special `batches` directory. This special directory maintains tracking information for the whole repository/annotation effort -  
Batches are the identity tags of a group of media/GUID annotated for a project-found-below in one go. 
There are possibly multiple times/events where data is annotated/created for this dataset. Each event is a batch.
Specifically, this directory contains `.txt` files named after the batch name. Batches are usually named after their relevant GitHub issue from [AAPB-CLAMS collaboration repository](https://github.com/clamsproject/aapb-collaboration).  
  * Each line in a `.txt` file _must_ be a single AAPB GUID, with an exception of any lines starts with `#` which denotes a comment.  
  * A GUID is a unique identifying string that can be used at their website to find one particular media and its supporting files, eg. `cpb-aacip-96d289b264c` at https://americanarchive.org/catalog/cpb-aacip-96d289b264c.

### Project Subdirectories 
Each directory in this repository represents a specific annotation project, its datasets and processing tools.    
This includes its `raw annotated data file`, `software-suite for converting from raw to gold`, `gold-formatted-final-output data file for tool ingestion`,
and `that project's readme.md explaining it plus its annotation guidelines`.  
The directory name is the name of the project. Each directory contains the following files:

* **RAW INTERMEDIATE DATASET FILES**: `YYMMDD-batchName` directory - these sub-directories contains raw output files from the manual annotation process created by the annotation tool (or by hand like a `.csv` file). 
Different annotation tools create different file formats with diverse formatting. 
  * The `YYMMDD-` prefix _must_ indicate the time when a batch of annotation is conducted. 
The `batchName` part of the directory name _must_ match only one of `.txt` files in the batches. 
* **CODEBASE FOR CONVERSION**: `process.{sh,py}` - a script to process the raw manual annotations and generate the publically-available "gold" dataset. In addition to this file, if the code requires additional dependencies/scripts, they can stay in the same directory. In case the dependencies are managed by a package manager (e.g., `pip`), the project manager _must_ provide relevant information in the `README.md` file.
* **FINAL READY-TO-USE DATASET FILES**: `golds` directory - this directory contains the public "gold" dataset generated by `process.py` script. The script _must_ generate one file per GUID (video/audio/text document) and the number of gold files in this directory _must_ match the sum of GUIDs in all batches annotated. 
The gold dataset is a set of files that are in a format that is ready for use with the newly developed tools. I.e. The raw file must be properly formatted so that tools in the next step of the process can use this dataset.
* **INFORMATION README** `README.md` - project-specific information:
    * annotation project name
    * annotator demographics _TODO - Confirm: Possibly age range, sex/gender (maybe?), language proficiency, occupational characteristics_  
    * annotation environment information (name, version, link, tool used, user manual, etc.)
    * project changes: eg: version changes, addition of new batches, change in annotator personnel, etc.
    * raw-to-gold generation code explanation - (dependencies, short description of process.py, file formats of raw+gold, column description + _datatype_, version/progress differences, discarded info during process.py, added info during process.py, etc.)  
    * _ANNOTATION GUIDELINES_ - sometimes this is a separate file `guidelines.md`. How to annotate in this project, aka scheme. This section should give sufficient information for the replication of the annotation to produce almost exact similar raw datasets.
      * How the tool is used
      * What to annotate
      * Options of label choices
      * Label formatting. eg. Time format in the annotation tool
        * eg. Raw format is `seconds:1000th_sec` `123:4567` 
        * _TODO - Time format should be made consistent by CLAMS management for the gold formats. Likely either `seconds:1000th_sec` or `hr:mn:sc:ms`._
      * Differentiation between labels, edge cases, other decisions made during annotation. 
      * Concerns, limitations, accuracy details. (eg. Annotation of time accuracy is likely only down to 0.1-0.2 seconds)
  > `readme.md` files are supposed to be actively maintained by the project manager. All `guideline.md` files are recommended to be version-controlled.  

## List of Current Projects/Subdirectories
_This section is currently manually updated and may be incomplete. It contains information up to the above editing date._  
* (`batches`)
* `january-slates` - slates are actual visible frames within the video media that contain the metadata and other identifying information of that video. 
  * eg. program name, director, producer, etc.
  * Project done in January. This is an outdated naming convention.
* `newshour-chyron` - drawn from the [NewsHour](https://americanarchive.org/special_collections/newshour) TV broadcast, 
this project annotates text appearing on screen, usually above or below the main action saying things such as "Breaking News", "Joan, author".
* `newshour-namedentity` - from NewsHour. This project annotated [named entities](https://www.techtarget.com/searchbusinessanalytics/definition/named-entity#:~:text=In%20data%20mining%2C%20a%20named,phone%20numbers%2C%20companies%20and%20addresses.)
found within the video _transcript_ along with which characters denoted that named entity and its type
 (see `newshour-namedentity/{guidelines,readme}.md`).
* `newshour-namedentity-wikipedialink` - from NewsHour. This project used the previous project's dataset and added
an extra label of which wikimedia link referred to the named entity annotated, eg. https://www.wikidata.org/wiki/Q931148.
* `newshour-transcript` - from NewsHour. This project found the start and end times for 10 tokens of closed captioning at a time from the transcript to the video. 

## Issue Tracking and Conversation Archive
Progress and other discussion by AAPB/CLAMS/WBGH is tracked via the open and closed [Github Issues](https://github.com/clamsproject/aapb-annotations/issues) feature.  
Finally, please email [CLAMS.ai admin](admin@clams.ai) for other inquiries.  