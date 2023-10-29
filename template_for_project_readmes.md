# Official Project Name 
(Name for human reader, use capitalization and spaces as usual)

## Project Overview
(About the project goals. Subsections may be used for domain-specific knowledge terminology, etc. )

### Specs
* Annotation Project Name - `Name for machine consumers` (**must be** exactly same typing as the directory name, which usually all lowercase without any spaces or special characters)
* Annotator Demographics
    * Number of annotators - (enter)
    * Occupational description - (enter)
    * Age range - (enter)
    * Education - (enter)
* Annotation Environment Information
    * Name - (enter)
    * Version - (enter)
    * Tool documentation - (see below tool installation)
* Project Changes
    * Number of batches - (enter)
    * Other version control information - (enter, if applicable)

## Tool Installation: Name of Tool
(link for download, if applicable)  
(link for source code, if applicable)  
(link for installation instructions, if applicable)  
(link for documentation, if applicable)  
(link for user manual, if applicable)  
(Any intro needed for tool)  
  
## Annotation Guidelines
(link for guidelines.{md/ppt/pdf/etc}, if separate file)
(Generally, prefer also to have a file copy of the current guidelines. More editable links to ppt/videos may be acceptable where pictures,etc are needed. Sometimes projects may not have a second file needed for guidelines.)

### Preparation
(data preparation, if applicable, including any pre-processing, etc. )

### What to Annotate
(attributes to annotate, if applicable)
* `attrib-name` - explanation

### How to Annotate It
(Explanation of the physical process how to do the annotation, what to press etc. Where needed.)

### Decisions, Differentiation, and Precision Level during Annotation
* **Problem  Name** - Information about Decisions that must be made during Annotation, for instance, Differentiation between two slate types. 
* **Problem  Name** - Information on accuracy, precision, error that may be present in the dataset.

## Data Format and `process.py`

### `raw` data
`.format` file - explanation.
* Fields: (possibly referring back to the "what to annotate" section above)
    * `field-text1`
    * `field-text2`
* Example:
```
example of raw data file here. 
```

### [`process.py`](process.py)
(Describe what the script does in changing the raw to the gold. This may include data formatting conversions.)

### `golds` data
`.format` file - explanation.  
* Fields:
    * `field-text1` - blah
    * `field-text2` - blah
* Example:
```
example here. 
```

## See also (optional, if applicable)
(any related projects, dataset, software, etc.)
