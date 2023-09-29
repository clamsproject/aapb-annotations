# Official Project Name (Caps no dashes)

## Project Overview

### (Domain Knowledge Term Explanation optional?)
About the project goals.

### Specs
* Annotation project name - proj name exactly same typing as the directory name, lowercase with dashes
* Annotator Demographics
    * Number of annotators - enter
    * Occupational description - enter
    * Age range - enter
    * Education - enter
* Annotation Environment information
    * Name - Annotation tool name (no specifics) 
    * Version - enter
    * Link/Tool Used/User Manual - (See below Tool Installation)
* Project changes
    * Number of Batches - enter 
    * Other Version Control Information - None

## Tool Installation: Name of Tool
Tool Link Here  
Any intro needed for tool.

## Annotation Guidelines
guidelines.{md/ppt/pdf/etc} Link Here.  
Generally, prefer also to have a file copy of the current guidelines. 
More editable links to ppt/videos may be acceptable where pictures,etc are needed. 
Sometimes projects may not have a second file needed for guidelines.  

### Preparation
Things needed to be done before annotating begins. 

### What to Annotate
Per column:  
* `col-header` - explanation

### How to Annotate It
Explanation of phsyical how to do the annotation, what to press etc. Where needed. 

### Decisions, Differentiations, and Precision during Annotation
**Problem  Name** - Information about Decisions that must be made during Annotation, for instance, Differentiation between two slate types. 
**Problem  Name** - Information on accuracy, precision, error that may be present in the dataset.

## Data format and `process.py`
### `raw` data
`.format` file where - explanation.
* Fields
    * `field-text1`
    * `field-text2`
* Example:
    ```
    example of raw data file here. 
    ```

### [`process.py`](process.py)
Describe what the script does in changing the raw to the gold. This may include data formatting conversions. 

### `golds` data
`.format` file - explanation.  
* Fields:
    * `field-text1` - blah
    * `field-text2` - blah
    * all other columns from the raw data are removed
* Example:
    ```
    $ cat file name
    example here. 
    ```

## (See also , optional?) 

### (Optional Fields?) 
Validation sets, evaluations sets. 
