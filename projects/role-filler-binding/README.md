# Role Filler Binding

## Project Overview
### What is Role Filler Binding?
[Explanation](https://arxiv.org/pdf/1902.09006.pdf).
Given a frame/schema of context (such as looking for video production metadata in videos), the role-filler binding concept (RFB) is when we look to fill categories/roles with new specific fillers/proper-nouns based on the situation.
In doing so, we use the expected similarities of a situation to understand a new but similar situation.
e.g. Our minds have a schema of expected information we would learn from watching a video. We watch a new video, with the goal of understanding the new video in a similar way.
"Director: James Cameron" where "Director" is a role, "James Cameron" is a filler. Binding refers to connecting these two things.

Provide an annotated dataset of the textual information shown in videos, starting from an inputted set of frames from a video, outputting a dataset of structurally-paired text of expected rf-pairs.

Videos are converted to sets of still images.
OCR (Optical Character Recognition) and RO (Reading Order apps) transcribes/annotates text from each image into a simple, barely-ordered string.
This annotation project then provides the top-bottom-left-right reading order, and chunk structuring guidance for structured key information extraction from videos.
The RFB annotation dataset provides the ground truth labels for how humans would read a video image and structure the text information that is presented.

> This endeavor allows the CLAMS project to return structured, ordered OCR text from pixel data!

### Specs
* Annotation project name - `role-filler-binding`
* Annotator Demographics
    * Number of annotators - 3 (1 currently uploaded as raws, College Student)
    * Occupational description - College Student, Data Professional
    * Age range - 20s
    * Education - College and Computational Linguistics MSc
* Annotation Environment information
    * Name - [annenv-rfbparsing](https://github.com/clamsproject/aapb-annenv-role-filler-binder)  (a.k.a creditparsing)
    * Version - unknown
    * Tool Documentation - (see below tool installation)
* Project changes
    * Number of Batches - (1 uploaded).
        * "Round2" - Raws are from the [aapb-annotations-44.txt](batches/aapb-annotations-44.txt). These are un-adjudicated raws annotated by annotator20007. The scope of this round was solely "credits" scenes.
        * "Round1" - a practice batch can be found [here](batches/aapb-annenv-role-filler-binder-11.txt). The raws from this batch are not uploaded and were used to develop the annotation tool and guidelines.
    * Other Version Control Information - Previous versions of the guidelines can be found at the end of the `guidelines.ppt`.
        * The first run of this project will focus on textual frames and credits for video production rf-pairs, while later runs may focus on other images such as identifying chyrons.

## Tool Installation: annenv-rfbparsing
Annotation Tool is developed in-house specifically for this workflow.
[The Credit Parsing Project](https://github.com/clamsproject/aapb-annenv-creditparsing) including other information later.

## Annotation Guidelines
> [!Important]
> The following section in this readme is simply an overview or repeat of what is said in the [`current guidelines link`](https://docs.google.com/document/d/1Kxa99JMfDuy-y2xFqmgPkuLnLqEGhNB8iMxBT3E1Tx4/edit?usp=sharing).
> The most updated guideline will be linked here.
> Access to this link must be approved due to IP/copyright issues.
> The above live link document will be the final say on how to annotate this project, in case discrepancies occur in the updating between this read and the above live link.

### Preparation
INPUT - Still images with OCR-able text are loaded into the annotation tool.

### What to Annotate
The goal is to capture metadata information from the video that is in the role-filler pair format from suspected images with text.
This generally means from these three categories: Production Roles, Thematic Content Roles, and Video Archival Metadata.
1. Production Roles - personnel roles for the production of the video, (e.g. "Videographer", "Producer", "Payroll", "Director")
2. Thematic Content Roles - roles of people/information based on the video's subject and content.
This often can be a guest speaker or topic of the video. It can also include Named Entities related to the video content.
   (E.g. "US President: George H. W. Bush", "Author: LIU Cixin", "Whistleblower: Shelley Smith")
   (E.g. "(implied date role):Dec 7, 1941" <- this date is informative about the subject of a Pearl Harbor video)
3. Video Archival Metadata - this is a blanket category for other metadata useful for archival purposes.
   (E.g. "Show Title: Sesame Street", Series Title: "New York NOW", "Copyright 1984 Walt Disney Corporation")

For a more comprehensive guide on expected rf-pairs, please see the guideline.


### How to Annotate It
> [!Important]
> Please see the above linked `guidelines.ppt` for Annotation directions.

### Decisions, Differentiation, and Precision Level during Annotation
> [!Important]
> Please see the above linked `guidelines.ppt` for discussion of Decisions made during Annotation.

#### Precision / Data Quality
* **Errors in Annotation** - The largest differences in annotation will likely be cases of judgment between two annotators and guideline changes.
Since this is not time based, generally, the errors will be typos. Else, it will be differences of judgment on how to specifically annotate certain features (such as possibly continuing credits).

* **Guidelines updating concurrently with annotation** - The guidelines are often being changed while the project is occurring, this can cause a lower inter-annotator agreement.

#### Data Quality Efforts
The planned execution is as follows.
Annotation team confers together on what the guidelines should be.
Then, different members will all annotate the same sample set. The resulting raws will be compared to see how much variation lies between them.

* **Inter-Annotation Agreement** - Because this task is closer to a "parsing" type of project than a simple classification, the complexity scope is much higher than classification projects.
To quantify the variation between how trained annotators would annotate the same material, a small subset was used to test the differences between in-house annotators and
to test whether the guidelines along with training sufficiently conveyed the same requested information.
This will be used to determine what level of annotation cross-check is required - single annotation no check, single annotation adjudicated, double annotation, etc.
A visualizer for the RFB annotations and for understanding inter-annotator agreement is [here](https://github.com/clamsproject/RFB_annotation_visualizer).
Inter-annotation agreement calculation and "evaluation" is [here](https://github.com/clamsproject/aapb-annenv-role-filler-binder/tree/iaa_calculation).

#### Current Numbers for Round 2
Total images: 3700
Non-skip images from annotator20007: 367
Non-skip images from annotator20008: 236
Non-skip images intersection across both annotators: 171


## Data format and `process.py`
### `raw` data
`.json` file of the annotation role-filler pairs of that frame.
* Fields
    * (Fields listed here do not have field-names explicitly named. The square brackets denote the structure.)
    * `role` - What the Role is, sometimes is blank, usually has 0-1 texts.
    * `filler` - What the Filler is, sometimes blank, sometimes has multiple texts, 0+ texts.
    * `frame annotation` - Overarching annotation of what the frame is, eg. "duplicate", or "skip" with reasons. (See `guidelines.ppt` for reasons.)
    * (each set of roles and fillers are keyed by the frame number in the video)
* Example:
    ```
    [
      [
        "Videography",
        "Doug Steffer<DELIM>
         Kris Nestle"
      ]
    ]
    ```

### [`process.py`](process.py)
The python file for processing all raw-format gold annotations made to the batch whose name follows the format `YYMMDD-batchName`, for example, it's `231117-aapb-annotations-44` under this directory.

Besides, the basic logistics of `process.py` is to convert annotations made to each video (i.e. GUID) to a comma-separated value (`.csv`) table which contains 4 columns:
* `GUID`: the unique GUID for each video
* `FRAME`: the frame number of a certain frame in the video of GUID
* `SKIPPED`: an indication representing if an annotation towards the frame is skipped by the annotator
* `ANNOTATIONS`: the annotations made by human annotators

that's to say, the number of `.csv` files generated by `process.py` is equal to the number of files in `231117-aapb-annotations-44`.

### `golds` data
* The `golds` directory contains no sub-directory and only `.csv` files.
* The naming convention for every file under this directory is `<GUID>-gold.csv`
* As mentioned by `process.py`, each `.csv` file contains 4 columns `GUID, FRAME, SKIPPED, ANNOTATIONS`
    * In particular, the value for the column `ANNOTATIONS` when the value of `SKIPPED` is `false` has the rule similar to CSV format wrapping up raw annotations to a csv-string:
      * Every role-filler binding annotation is led by a comma `','` and separated by a newline character `'\n'`, and the role and filler within the binding is separated by a comma `','`
      * For example, if the raw annotation has multiple bindings:
        ```
        "Production Assistants": [
            "PATTI BONNET",
            "DEMETRIA GALLEGOS",
            "RONDA LENNON",
        ],
        ```
        the corresponding csv-string would look like:
        ```
        ,Production Assistants,PATTI BONNET\n
        ,Production Assistants,DEMETRIA GALLEGOS\n
        ,Production Assistants,RONDA LENNON\n
        ```
> [!Note]
>  `<DELIM>` indicates where a delimiter character will be used to separate different pieces of text that are all in the same key or value box.
> The delimiter is a "new_line" or "\n" typed literally as a new line break in the annotation tool.

## Links to old guidelines ====
> This is the first version of the [guidelines ppt](https://docs.google.com/presentation/d/1ziiK5aG-WBq1qZy9YA8NC9WPoLFgsOXnrrBTaDJdFnM).
> It is not used anymore.
> The current guidelines.ppt keeps a copy of some older conversation information during the formation of the guidelines, however older versions are work in progress, as opposed to older complete variants.
