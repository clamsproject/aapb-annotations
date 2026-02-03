# Contributing to AAPB-CLAMS Annotations

This document provides guidelines for data managers and contributors who create and maintain annotation projects in this repository.

## Project Directory Structure

All annotation projects are located in the `projects/` directory. Each project lives in its own subdirectory under `projects/` (e.g., `projects/scene-recognition/`). The subdirectory name is the project name. A project directory must include:

- Raw annotation data (in dated batch directories)
- Gold-formatted output files (in `golds/` directory)
- Conversion scripts (typically `process.py`)
- Project documentation (`README.md`)

### Raw Annotation Data

> [!IMPORTANT]
> `YYMMDD-batchName` directory

This directory contains output files from the manual annotation process created by an annotation tool or by hand.

The raw annotation files are organized by batch name and starting date of the annotation. A single "period" of the annotation is the whole process of a single batch of source data (AAPB assets) being annotated. The `YYMMDD-` prefix _must_ indicate an associated time to a batch of annotation (usually that is when the batch is first prepared and used for annotation, or completed and delivered). The `batchName` part of the directory name _must_ match the basename of one of the `.txt` files in the [annotation batches directory](batches/README.md). The date and batch name prefixes are used for sorting annotation processes and machine ingestion of the raw data.

Different annotation tools create different file formats, hence we need conversion of the raw annotation files to files with a common format for the gold data.


### Gold Dataset Files

> [!IMPORTANT]
> `golds` directory

There are rules on the content and structure of the gold directory:

1. There _must_ be one file per GUID, and the GUID should be part of the filename.
2. The number of gold files in this directory _must_ match the sum of GUIDs in all batches annotated. This means that there cannot be any overlap between assets in batches.
3. The `golds` directory _may_ have subdirectories, but these subdirectories should not reflect batch structure, but rather different division of annotation type (e.g. pure named entity span annotation vs. named entity span + some grounding annotation) or format (same information but formatted as timepoints vs. time intervals).


### Scripts for Format Conversion

> [!IMPORTANT]
> _(usually)_ `process.{sh,py}`

This is typically a single script to process the raw annotation files and generate the gold data.
The input file format (i.e., direct output from the annotation process) can vary (e.g. `.csv`, `.json`, `.txt`). The output file format must be a common machine-readable data format (CSV, TSV, JSON, but definitely not MMIF), and is **subject to change** for any future requirements in the consumption software.

In addition to the main script, if the code requires additional dependencies/scripts, they should be in the same level at that subdirectory. Dependencies on third-party modules can be documented in the `README.md` file or in a machine-friendly file with the list of dependencies (e.g. `requirements.txt` for `pip`).

Check the [Repository-level Conventions](#repository-level-conventions) section for naming conventions for common field/column names for gold data.


### README File and Other Project Documentation

> [!IMPORTANT]
> `README.md` (_and possibly `guidelines.{md,ppt}`_)

Project-specific information, including but not limited to:

* Annotation project name

* One-line summary of the project

* Annotator summary. Some basic demographic information about the annotators: age group, language proficiency, occupational characteristics, etc. No [personally identifiable information](https://en.wikipedia.org/wiki/Personal_data), unless the annotator wants to be credited.

* Annotation environment/tool information (name, version, link, user manual, etcetera). In most cases, there is a separate codebase (ideally on [https://github.com/clamsproject/](https://github.com/clamsproject/)) for the annotation tool which includes the manual.

* Project changes: version changes, selection of asset batches, change in annotator personnel, etc.

* Raw-to-gold conversion code explanation
    * dependencies, short description of `process.py`
    * formats of raw and gold files
    * field description, with data types
    * differences, added information, discarded information during `process.py`

* Annotation guidelines - sometimes as a separate file named `guidelines.{md,ppt}`. This section should give sufficient documentation for how the annotation was done and what the conditions/assumptions are under which the dataset exists:
    * What tool is used, and how it is used.
    * What to annotate
    * Options of label choices
    * Label formatting.
    * Differentiation between labels, edge cases, other decisions made during annotation.
    * Concerns, limitations, precision details. (e.g. time imprecision)

> [!NOTE]
> `README.md` & `guidelines.{md,ppt}` files are supposed to be actively maintained by the project manager. All guideline files are recommended to be version-controlled.


## Batch File Format

Each batch is defined by a `BATCH_NAME.txt` file in the `batches/` directory.

* Batches are often named after their relevant GitHub issue from the [AAPB-CLAMS collaboration repository](https://github.com/clamsproject/aapb-collaboration).

* Each line in the file must be either a single AAPB GUID or a comment starting with a `#`. The first lines are typically batch-level comments, while later comment lines may specify sources for subsequent AAPB GUIDs.

Typically, batch-level comments start and end with a comment line with just hyphens, for example:

```
# --------------------------------------------------------------------------------
# A set of videos that have various instances of "scenes with text" that are ideal
# for creating labeled data for roles and fillers (key-value pairs) extraction.
#
# See https://github.com/clamsproject/aapb-annotations/issues/44 for the selection
# process and other additional information.
# --------------------------------------------------------------------------------
```


## Repository-level Conventions

> [!IMPORTANT]
> Media Time = `hh:mm:ss.mmm` with a **DOT**  
> Annotation times are usually a little imprecise because audiovisual phenomena are, or visualizing/labelling of such is.  
> Some estimates of imprecision are given by Margin of Error.  
> Directionality definitions help frame the boundaries meant by annotated times.  
> The fields in the gold datasets should be standardized.

### Field Naming Conventions

> [!NOTE]
> Also often referred to as "column names" (mainly because we tend to use tabular data formats like CSV, TSV, etc.). 

The field name in the "gold" data should indicate the type of data in the field. 
That is, fields that contain the same (or similar enough) data should have the same name across different annotation task subdirectories.
The following table provides a ledger for commonly used names and their data types (see [#117](https://github.com/clamsproject/aapb-annotations/issues/107) for discussion). Some names are **standardized** and must be used when applicable, while others are **common** conventions that are recommended for consistency.

| Field(s) Name | Description                                                                         |
|---------------|-------------------------------------------------------------------------------------|
*   `at` | **Standardized.** A time point in a time-based source media. Replaces `timestamp`.
*   `start`/`end` | **Standardized.** A time interval in a time-based source media (e.g., character offsets and time intervals).
*   `scene-label` | **Standardized.** A label used for classifying a still shot or a scene from a video source.
*   `scene-subtype-label` | **Standardized.** A sub-label providing more specific classification for a `scene-label`.
*   `text-transcript` | **Standardized.** A text transcription of text visually appearing in the video or image source media.
*   `speech-transcript` | **Standardized.** A text transcription of language spoken in the video or audio source media.
*   `index` | **Common.** An autonumber for annotations, starting from "1".
*   `label` | **Common.** The label for an annotation, similar to the MMIF Vocabulary label property.
*   `text` | **Common.** The text content of an annotation. Use of more specific names like `text-transcript` or `speech-transcript` is preferred.
*   `GUID` | **Discouraged.** The AAPB ID for a video (e.g., "cpb-aacip-81-881jx33t"). Since gold data files are named after the GUID, this field is redundant.

#### Notes on Specific Fields

*   **`GUID`**: While some older `golds` data might contain a `GUID` column, this is now discouraged. The file-per-GUID structure for `golds` data makes this column redundant. New `process.py` scripts should avoid adding it.

*   **`at` vs. `timestamp`**: The standardized field for a time point is `at`. The name `timestamp` was used in some older datasets but should be considered deprecated in favor of `at` for new datasets.

### Time Point Notation

> [!IMPORTANT]
> `hh:mm:ss.mmm` with a **DOT**  

The time format for all (gold) datasets in this repository is [ISO 8601 Time Format](https://en.wikipedia.org/wiki/ISO_8601#Times), with time precision of up to hours and down to milliseconds placed after seconds with a **DOT**, where `00:00:00.000` means the very beginning of a time-based media (not midnight real-time). This instruction is for the "gold" data formats throughout this repository, except where exceptions are required and documented.

> _TODO: Some gold datasets and tools have not yet been converted._

During raw annotation however, third-party annotation tools may use different time formats. The expectation for any in-house tools and apps is to use this standard. If configurable, annotation tools should be configured to use this format. If possible, the annotator should also be instructed to use this format.

> _TODO: the following prose is unclear_

Due to algorithmic differences in compression/decompression and their implementations in video players for human watchers, we may lose temporal precision. However, this is most likely to be in the order of a few milliseconds and hence not a significant problem.

### Imprecision in Annotation in General

Currently, data quality processes are still being designed and datasets do not have a data quality checklist applied to them. This means that general data messiness including typos are always possible.
 
Two semi-preventative measures are: 

1. If only a few value options are expected in one column, using a pie chart/counter in Excel to search/count for typos to manually correct is possible. 
2. Annotators should use copy-paste wherever possible instead of typing, and annotation tools should have buttons to add items, reducing typos during typing.  

The current convention is that annotators are asked to be as careful as possible, and some datasets are "quality-assumed" upon faith in annotators/environment until such time a quantitative analysis of errors is done.

### Imprecision in Time-based Annotation

Time-based annotations are almost inherently imprecise. This is due usually to either perception or manipulation of the tool within the limits of meaningful task-speed constraints. Furthermore, the features of audiovisual materials do not always have clear-cut beginning and end points.    

The conventions here attempt to provide clarity for when generally the annotations can be considered precise or not. 

1. **MARGIN OF ERROR** _(+/- in both directions)_. The margin of error depends on how an annotation project was conducted and how the tool was used. For instance, if the annotator is playing a video at half speed (audio listenable) and pressing a button when a chyron appears (and not stopping to correct or precisely verify), we can assume the following:

   1. Precision is limited by on-screen-and-discern-to-press [reaction time](https://www.reddit.com/r/truegaming/comments/hu0p3a/comment/fylge12/?utm_source=reddit&utm_medium=web2x&context=3),
which is approximately .200 to .250 seconds. This time amount is somewhat similarly shown in feedback from musicians using digital keyboards and video gamers complaining about [ping or framerate](https://www.pcgamer.com/how-many-frames-per-second-can-the-human-eye-really-see/).
   2. If the video is playing at half speed, we can then assume the margin of error from this factor is approximately 0.100-0.200 seconds. 
   3. Being able to pause and visually move a time slider with high precision would increase the precision but likely lead to excessive annotation labor cost. 
   4. It is highly likely there will be cases where margin of error will pass over the Directionality limit given below. 
However, the convention requested during annotation is to attempt to preserve **Directionality** instructions over reducing **Margin of Error**.   
  
2. **DIRECTIONALITY** _(as close to a certain boundary but not past it)_. We attempt to give instructions and explanation for when we want an annotation to be up to the limit of something as close as possible. There are times when a project requires one thing to be the superinterval and times when other projects require the other way around. (See 3rd point.)

   1. E.g. Let's say we are annotating a fading-in-and-out chyron. 
   We want the start time of the chyron to be "as close as possible but after" the moment when the chyron is fully solid and no longer transparent.
   And we want the end time of the chyron to be "as close as possible but before" the moment when the chyron begins to start fading-out. 
   Here are two ways to describe one Directionality convention: 
      1. **Instructions for human annotators** - For time-based media, annotated times are to be labeled as within the duration of the phenomenon.
   Eg. if a text-based label fades on-and-off screen, 
   the annotated start time should be the moment it has become fully solid and the end time should be the moment just before it begins to fade.  
      2. **Interpreting [MMIF](https://github.com/clamsproject/mmif) or annotations** - For time-based media, assume that the interval defined in the MMIF annotation is contained within the relevant interval in the actual media.  

3. **SUPERINTERVAL/SUBINTERVAL/SUPERSET** - Another way to explain Directionality. This explanation originates from the mathematical terms "superset" and "subset", where if groupA is a "superset" containing groupB, then that means that groupA wholly contains the bounds of groupB.  
So, if an annotated time interval label with a start and end time (as is above) is wholly within the time where a phenomenon (e.g. a chyron) appears, then the annotation is considered a subinterval of the phenomenon.  
i.e. The phenomenon is a superinterval to the labeled time.  
i.e. Any time given by the annotated time interval of the chyron should return an image of the chyron being present in the media at that time.   

Finally, a reminder that at 30 frames per second, each frame is 0.033_ seconds long - meaning a tenth of a second has 3 frames within it. Practically speaking, there is only a small percentage of cases where the variation between one frame to its neighbor is relevant, especially in cases of human perception. The conventions for precision hold until new needs of the project are required. 

### Batch File Naming Conventions

Batch names should be in lower case. If a batch is named after a GitHub issue it should be in this format:

```
issueName-issueNumber(-identifier+).txt
```

The `issueName-issueNumber` part points to a GitHub issue (usually on the [AAPB Collaborations Repository](https://github.com/clamsproject/aapb-collaboration)) that contains the discussion/documentation of how this batch was chosen and created. Optionally, any other `identifier` come after this, and can be used to denote different batches created from the same issue. Because batches can be reused for disparate projects, an identifier can indicate some property about the GUIDs in that batch, but should not indicate any particulars of the annotation project that the batch was used for. If no real discerning quality can be used as an identifier, use `abcd` lettering to denote numbering.

Examples: `aapb-collaboration-27-a.txt` and `aapb-collaboration-27-b.txt`

If a batch is not named after a GitHub issue then the name should be informative and be a decent abbreviation of the description in the batch comment.
