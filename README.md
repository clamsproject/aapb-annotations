# AAPB-CLAMS Annotation Repository
This repository contains datasets from manual annotation projects in [AAPB](https://americanarchive.org/)-[CLAMS](https://clams.ai) collaboration.

## Project Information
American Archive of Public Broadcasting (AAPB) has involved the CLAMS team to develop information extraction systems for digital archives of public media (primarily video and audio from publicly-funded tv shows and radio broadcasts). 
This will facilitate the research and preservation of significant historical content from this media collection. 
Some parts of the process of archiving, summarizing and extracting metadata from media assets could eventually be automatic. 
This repository/endeavor provides training and evaluation data for the machine learning-based CLAMS apps in this process. 

## Structure of This Repository/Directory
 - `batches` subdirectory
 - project subdirectories
 - this README file

### `batches` Subdirectory 
The first subdirectory is the special `batches` subdirectory. 
This special subdirectory maintains tracking source data for the whole repository/annotation endeavor. 

Smaller selections of the AAPB collection are chosen and cataloged as batches in this subdirectory. 
These sets are chosen for variety or utility needed for the applications developed here.  
A batch is the set of the identifying GUIDs/tags for that group of media assets. 

Batches are decided some time before annotations begin. 
Annotation projects then choose appropriate batches for each moment/period of annotation work.
(See [raw annotation](#raw-annotation-files) section.)

Specifically, this directory contains `.txt` files named after the batch name. 
* Batches are usually named after their relevant GitHub issue from [AAPB-CLAMS collaboration repository](https://github.com/clamsproject/aapb-collaboration). 
* A GUID is a unique identifying string that can be used at the AAPB website to find one particular media and its supporting files, eg. `cpb-aacip-96d289b264c` at https://americanarchive.org/catalog/cpb-aacip-96d289b264c.
* **Each line in the file _must_ be a single AAPB GUID**, with an exception to any lines starts with `#` - which denotes a comment.
* The first line of each batch now is a comment that explains the Github issue that documents how that batch was created. 
* All the batches for projects should be saved in this `batches` folder, and each project's raw directory will be named with which batch was used. 
This can then be used to collate a list of all the used batches, by which projects.

> [!NOTE]
> AAPB-GUID is not [Universally unique identifier](https://en.wikipedia.org/wiki/Universally_unique_identifier), but just a unique identifier within the scope of the AAPB system.  

### Project Subdirectories 
Every other subdirectory in this repository represents a specific annotation project, its datasets and processing tools.   
This includes its raw annotated data file, gold-formatted final output data file for tool ingestion, software-suite for converting from raw to gold, 
and a project-specific `readme.md` explaining it and its annotation guidelines.

The subdirectory name is the name of the project. Each subdirectory contains the following files:

#### Raw annotation files
> [!IMPORTANT]
> `YYMMDD-batchName` directory 
 
This contains raw output files from the manual annotation process created by the annotation tool (or by hand like a `.csv` file). 

As the name of this subdirectory suggests, the raw annotation files are organized by the batch name and the date of the annotation. 
Namely, a single "period" of the annotation is the whole process of a single batch of source data (AAPB assets) being annotated.
The `YYMMDD-` prefix _must_ indicate the time when a batch of annotation is conducted. 
(e.g., when the batch is decided to be annotated)
These prefixes are used for the sorting of annotation processes and machine ingestion of the raw data. 
The `batchName` part of the directory name _must_ match only one of `.txt` files in the [`batches` directory](#batches-subdirectory). 

Different annotation tools create different file formats with diverse formatting. 
Hence, we need conversion of the raw annotation files to files with a common format that we call `golds`.

#### Gold dataset files
> [!IMPORTANT]
> `golds` directory
> 
> This directory contains the public "gold" dataset generated by the above script.

The gold dataset is a set of files that are in a format that is ready for machine consumption primarily for
1. training ML models for CLAMS apps,
2. evaluation of CLAMS app outputs,
3. other public usage

In other words, the distinction between `raw` and `golds` are purely for machine consumption.
As we keep some rules for how `golds` files are organized (see below), users of the AAPB-CLAMS dataset may find it easier to use `golds` data than `raw` data for machine consumption.

#### Codebase for format conversion
> [!IMPORTANT]
> _(usually)_ `process.{sh,py}` _and dependencies_

A piece of software to process the `raw` annotation files and generate the `gold` dataset.
The input file format (i.e., direct output from the annotation process) can vary (e.g. `.csv`, `.json`, `.txt`).
The output file format must be a common machine-readable data format (CSV, JSON, [definitely not MMIF](https://github.com/clamsproject/mmif/issues/153#issuecomment-1485513488)), and **subject to change** for any future requirements in the consumption software. 
Thus, users of a gold dataset should be aware of the version of the gold dataset they are using, and are recommended to use [permalinks](https://docs.github.com/en/repositories/working-with-files/using-files/getting-permanent-links-to-files) to refer to a specific version of the gold dataset in their code or documentation.

To ensure consistency between data consumption software, there are a few requirements for the `process.py`.
1. The script _must_ generate one file per GUID.
2. The number of gold files in this directory _must_ match the sum of GUIDs in all batches (`YYMMDD-xxx` subdirectories) annotated.
    * Namely, there must not be any overlap between assets in batches.
3. `golds` directory _must not_ have subdirectories.

In addition to the main code file, if the code requires additional dependencies/scripts, they can stay in the same level at that subdirectory.
The dependencies information can be written down in the `README.md` file or in a machine-friendly file with the list of dependencies (e.g. `requirements.txt` for `pip`).

And finally, check the [conventions section](#repository-level-conventions) for the naming conventions for common field/column names for `golds` data. 

#### Information README
> [!IMPORTANT] 
> `README.md` (_and possibly `guidelines.{md,ppt}`_)

Project-specific information, including but not limited to:
* Annotation project name
* One-line summary of the project 
* Annotator summary: Some basic demographic information about the annotators. Age group, language proficiency, occupational characteristics, etc.
    * no [PII](https://en.wikipedia.org/wiki/Personal_data), unless the annotator wants to be credited
* Annotation environment/tool information (name, version, link, user manual, etc.)
    * In most cases, there is a separate codebase (ideally on `clamsproject` GitHub) for the annotation tool, and the user manual is there to be linked here.
* Project changes: version changes, selection of asset batches, change in annotator personnel, etc.
* Raw-to-gold conversion code explanation 
    * dependencies, short description of `process.py`
    * file formats of raw and gold
    * field description, _datatype_
    * differences, added information, discarded information during `process.py`
* Annotation guidelines - sometimes this is a separate file: `guidelines.{md,ppt}`: How to annotate in this project, aka scheme. 
This section should give sufficient documentation for how the annotation was done and the conditions/assumptions under which the dataset exists. 
    * What tool is used, and how it is used. 
    * What to annotate
    * Options of label choices
    * Label formatting. 
    * Differentiation between labels, edge cases, other decisions made during annotation.
    * Concerns, limitations, precision details. (e.g. time imprecision)

> [!NOTE]
> `readme.md` & `guidelines.{md,ppt}` files are supposed to be actively maintained by the project manager. All guideline files are recommended to be version-controlled. 

## Repository-level Conventions

> Please see the [Repository-level Conventions file](repository_level_conventions.md) for standardizations, explanations and conventions. 

### TL;DR
> [!IMPORTANT]
> Media Time = `hh:mm:ss.mmm` with a **DOT**  
> Annotation times are usually a little imprecise because audiovisual phenomena are, or visualizing/labelling of such is.  
> Some estimates of imprecision are given by Margin of Error.  
> Directionality definitions help frame the boundaries meant by annotated times.  
> The fields in the gold datasets should be standardized.
 
## List of Current Projects/Subdirectories
_This section is currently manually updated and may be incomplete. It contains information up to the readme's editing date._ 
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
* `role-filler-binding` - This project uses the [role filler binding](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8019313/#:~:text=These%20structures%20can,understand%20new%20situations.) linguistic theory to attempt to extract and organize Optical Character Recognized (OCR) text into a structured and readable set of metadata pairs. 
The pairs are usually a role of a production-collaborator or role of a person-within-the-video... and the named, capitalized person name that fills that role. 
* `scene-recogntion` - This project builds the dataset meant to train ML models to recognize scenes/frames/timeframes that interest GBH/AAPB/CLAMS for extracting metadata such as slates, chyrons, credits, important-people-being-interviewed. 
This is a combined effort to recognize these kinds of frames and find the timeframes where they exist in aggregate, drawing upon findings in previous projects.

## Issue Tracking and Conversation Archive
Progress and other discussion by AAPB/CLAMS/WBGH is tracked via the open and closed [Github Issues](https://github.com/clamsproject/aapb-annotations/issues) feature. 
Finally, please email [CLAMS.ai admin](mailto:admin@clams.ai) for other inquiries. 
