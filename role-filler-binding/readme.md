# Role Filler Binding

## Project Overview
### What is Role Filler Binding? 
[Explanation](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8019313/#:~:text=These%20structures%20can,understand%20new%20situations.).  
[Explanation 2](https://arxiv.org/pdf/1902.09006.pdf).  
Given a frame of context (such as looking for personnel metadata in videos), linguistics theorizes we do role filler binding, which is when we look to fill categories/roles with more specific Proper Nouns based on the situation.  
e.g. "Director: James Cameron" where "Director" is the role, "James Cameron" is the filler. Binding refers to connecting these two things. 

Provide an annotated dataset of the textual information shown in videos, mostly preferring information related to credits shown usually 
at the start or at the end of the program. Still frames/images are detected by another tool
where OCR (Optical Character Recognition) results upstream can detect and transcribe text from that still image.  
The OCR results often detect text boxes without regard for how a human would read/parse it.   
This annotation project then provides the top-bottom-left-right reading order, other chunk structuring, and corrects OCR spelling.

> This endeavor allows the CLAMS project to return structured, ordered OCR text from pixel data!  
> This information could be used to improve the metadata by which projects are archived by.   

### Specs
* Annotation project name - `role-filler-binding`
* Annotator Demographics
    * Number of annotators - 3
    * Occupational description - College Student, Data Professional
    * Age range - 20s
    * Education - College and Computational Linguistics MSc
* Annotation Environment information
    * Name - annenv-creditparsing, created by: Sam Newman and Keigh Rim
    * Version - unknown
    * Tool Documentation - (see below tool installation)
* Project changes
    * Number of Batches - _TODO: confirm_. There are likely multiple batches to avoid contamination of training data into evaluation data. 
        * One batch can be found [here](aapb-annenv-role-filler-binder-11.txt).
    * Other Version Control Information - Previous versions of the guidelines can be found at the end of the `guidelines.ppt`.
        * The first run of this project will focus on Scenes With Text, while later runs may focus on other Scenes/images without text such as ones with people only.

## Tool Installation: annenv-creditparsing
Annotation Tool is developed in-house specifically for this workflow.  
[The Credit Parsing Project](https://github.com/clamsproject/aapb-annenv-creditparsing) including other information later.  
[An Example Instance](http://shannon.cs-i.brandeis.edu:20001/)  
The above example instance is only a demo instance of the tool.  

The tool must be accessed via log in through Brandeis VPN called [Ivanti](https://www.brandeis.edu/its/services/network-connectivity/vpn.html).
This requires a Brandeis account. 

## Annotation Guidelines
> [!Important]  
> The following section in this readme is simply an overview or repeat of what is said in the `guidelines.ppt`. 
> That `.ppt` document will be the final say on how to annotate this project, in case discrepancies occur in the updating of the two documents. 
> [guidelines.ppt](https://docs.google.com/presentation/d/1vjCeJFLF62PxYs8MJnmR4ipHZ_Q241l5It6PpCRsxHs/edit#slide=id.g1e6db24b1c6_0_0)  

_TODO: Add the `guidelines.ppt` to the project folder when it stabilizes._
### Preparation
INPUT - Still images with OCR-able text are loaded into the annotation tool.  


This tool requires a mouse and keyboard. 
You may wish to zoom your screen out to be able to see most of the "Add Annotation buttons"  
### What to Annotate
The goal is to capture metadata information from the video that is in the role-filler pair format from its credits, slates and titles. 
This generally means from these three categories: Production Roles, Video Subjects, and Video Archival Metadata. 
1. Production Roles - personnel roles for the production of the video, (e.g. "Videographer", "Producer", "Payroll", "Director")
2. Video Subjects - also roles, but usually within context of the video's subject. 
This often can be a guest speaker or topic of the video.
   (E.g. "US President: George H. W. Bush", "Author: LIU Cixin", "Whistleblower: Shelley Smith")
3. Video Archival Metadata - this is a blanket category for other metadata useful for archival purposes.
   (E.g. "Show Title: Sesame Street", Series Title: "New York NOW", "Copyright 1984 Walt Disney Corporation")

As role-filler/rf pairs, this project is looking to recognize:  
1. Personnel/organization roles in the video (e.g. "Videographer", "Special thanks") usually as Role
2. Person/organizations including corresponding information (e.g. "Michael Scott", "Michael Scott Foundation Durham, NC") usually as Filler 
3. Video/Media/Program metadata (e.g. "show title") usually as Role
4. The value of that information (e.g. "Sesame Street") usually as Filler


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
Annotation team will confer in a meeting together what all the annotations should be. Then, Annotation Manager, one Annotator and two Developers will all annotate the same sample set. The resulting json raws will be compared to see how much variation lies between them.

* **Inter-Annotation Agreement** - Because this task is closer to a "parsing" type of project than a simple classification, the complexity scope is much higher than classification projects. 
To quantify the variation between how trained annotators would annotate the same material, a small subset was used to test the differences between in-house annotators and 
to test whether the guidelines along with training sufficiently conveyed the same requested information. 
This will be used to determine what level of annotation cross check is required - single annotation no check, single annotation adjudicated, double annotation, etc. 
An ongoing effort to automatically calculate differences per frame and per character will be (TODO:link here).  

_TODO: Add the number of differences over the number of frames, along with other metrics._

## Data format and `process.py`
### `raw` data
`.json` file of the annotation role-filler pairs of that frame or a set of frames.  
* Fields (possibly referring back to the "what to annotate" section above)
    * `role` - What the Role is, sometimes is blank, usually has 0-1 texts. 
    * `filler` - What the Filler is, sometimes blank, sometimes has multiple texts, 0+ texts. 
    * `frame annotation` - Overarching annotation of what hte frame is, eg. "duplicate", or "skip" with reasons. (See `guidelines.ppt` for reasons.)
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
_TODO: to be added: process.py to convert to gold does not exist yet._

### `golds` data
* Fields:
    * `field-text1` - tba
    * `field-text2` - tba
* Example:
```
example here. 
```
> [!Note]  
>  `<DELIM>` indicates where a delimiter character will be used to separate different pieces of text that are all in the same key or value box.  
> The delimiter is a "new_line" or "\n" typed literally as a new line break in the annotation tool.     

## Links to old guidelines ====
> This is the first version of the [guidelines ppt](https://docs.google.com/presentation/d/1ziiK5aG-WBq1qZy9YA8NC9WPoLFgsOXnrrBTaDJdFnM).
> It is not used anymore. 
> The current guidelines.ppt keeps a copy of some older conversation information during the formation of the guidelines, however older versions are work in progress, as opposed to older complete variants.  