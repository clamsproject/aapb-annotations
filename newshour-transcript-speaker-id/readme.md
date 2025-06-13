# NewsHour Gold Generator for Speaker Diarization 

## Project Overview
The gold generator project creates a dataset of gold `rttm` files that record 
the start and end time of each speaker's speech in a NewsHour video. This dataset
is used to do speaker diarization.


### Specs
* Annotation Project Name - `newshour-transcript-speaker-id`
* Annotator Demographics
    * Number of annotators - 1
    * Occupational description - College student
    * Age range - 20s
    * Education - College 
* Annotation Environment Information
    * Name - N/A
    * Version - N/A
    * Tool documentation - N/A
* Project Changes
    * Number of batches - 1
    * Other version control information - N/A

## Tool Installation: Name of Tool
N/A

## Annotation Guidelines
N/A

### Preparation
All transcripts listed in `gold_transcripts` are from [this repo](https://github.com/clamsproject/aapb-collaboration/tree/3642731e7dd8d1183e16aa70f4c45e93665f2597/21),
specifically under the head `e83cd8a1`.  

All tsv files under `gold_tsv` are preprocessed by `process.py` in [newshour-transcript-sync](https://github.com/clamsproject/aapb-annotations/tree/main/newshour-transcript-sync).
For more information on what `process.py` does, please refer to the code and the `readme.md` in `newshour-transcript-sync`. 

All data included in the current subdirectory are ready to be passed as input. 

### What to Annotate
N/A

### How to Annotate It
N/A

### Decisions, Differentiation, and Precision Level during Annotation
There can be multiple speakers' words included in one speech slice in the `tsv` file. Without running some ASR tools again
or manually annotate the start and end time again, which takes lots of time, we have no idea when exactly each speaker 
starts or ends their talking. When there is a slice including multiple speakers' words, we can only mark the whole slice 
under one speaker. 

We have multiple choices to deal with this situation, as listed in [issue #96](https://github.com/clamsproject/aapb-annotations/issues/96). 
The current method we use to make the decision is method 1. Specifically, we use the majority speaker as "the" speaker. 

For example, for the following transcript:
```
A: How are you, Jim?
B: I am good. Thanks for asking. 
```

The corresponding speech slices in the tsv file are:

| index | start        | end          | content              |
|-------|--------------|--------------|----------------------|
| 1     | 00:02:05.570 | 00:02:09.393 | How are              |
| 2     | 00:02:09.393 | 00:02:10.243 | you, Jim? I am good. |
| 3     | 00:02:10.243 | 00:02:11.000 | Thanks for asking.   |

The second slice contains a mix of words from A and from B. In this case, mark the whole slice under the speaker who 
has more tokens in the slice. In the second slice, B is the majority speaker, because there are 3 out of 5 tokens 
coming from B, so the speaker in the time range of 00:02:234 and 00:03:345 is thus B. 


#### Data Quality Efforts (or other subheaders, optional)
A brief description of the problem can be found in [issue #96](https://github.com/clamsproject/aapb-annotations/issues/96). 

In short, the time stamps of each person's speech does not perfectly match with the fact. The preprocessed tsv files 
marks the start and end time of every 10 spoken words without consideration on who the speaker is.

## Data Format and `process.py`

### `raw` data
`.txt` file - explanation.
* Fields: N/A. Most lines starts with a speaker's name followed by the words that speaker said. 
* Example:
```
MacNEIL: I guess what you`re saying is that they said the more coal produced, the more money would go into the funds. 
```

`.tsv` file - explanation.
* Fields: 
  * `index`: the index of the line 
  * `start`: start time of a speech slice 
  * `end`: end time of a speech slice 
  * `content`: the words of a speech slice 
* Example:
 
| index | start        | end          | content                                                           |
|-------|--------------|--------------|-------------------------------------------------------------------|
| 1     | 00:02:05.570 | 00:02:08.570 | Good evening. I'm Jim Lehrer. On the NewsHour tonight coverage    |
| 2     | 00:02:08.580 | 00:02:12.390 | of the Salt Lake City Olympics investigation, some perspective on |


### [`process.py`](process.py)
According to the start time and the end time listed in the tsv files, and the speakers listed in the transcripts,      
`process.py` lists the starting time and the duration of each person's speech and write those information into a `rttm` file. 

To use the script, first make sure `clams_utils` is installed, 

`pip install clams-utils `

then run the following:

`python process.py --gold_tsv_dir <directory_for_gold_tsv> --gold_transcript_dir <directory_for_gold_newshour_transcripts>`  

Parameters:                                                                                
* `--gold_tsv_dir`: the directory that contains all preprocessed `tsv` files.               
* `--gold_transcript_dir`: the directory that contains corresponding NewsHour transcripts (`txt` files).  

### `golds` data
`.rttm` file - explanation.  
* Fields (there is no head as in tables, but each line has 10 fields):
  * Type: type of the record (in the gold, always SPEAKER).
  * File ID: The name of the audio file that the annotation corresponds to.
  * Channel ID: The channel number (in the gold, always 1).
  * Turn Onset: The start time of the speech segment in seconds.
  * Turn Duration: The duration of the speech segment in seconds.
  * Orthography Field: Speakers' words (in the gold, always N/A)
  * Speaker Type: Indicates the type of speaker (in the gold, always N/A).
  * Speaker Name: The name of the speaker.
  * Confidence Score: A confidence score for the recognition or diarization (in the gold, always N/A).
  * Signal Lookahead Time: (in the gold, always N/A).

* Example:
```
  SPEAKER cpb-aacip-507-4t6f18t178 1 162.21 61.39 <NA> <NA> ROBERT_MacNEIL <NA> <NA>
  SPEAKER cpb-aacip-507-v11vd6pz5w 1 705.28 20.7 <NA> <NA> MARGARET_WARNER <NA> <NA>
```



