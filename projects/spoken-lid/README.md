# Spoken Language Identification

## Project Overview

Labels of the language spoken in short audio clips of AAPB assets, for training and evaluating spoken language identification (LID). The assets were selected for speech in Samoan, Central Alaskan Yup'ik or Spanish, and most of them also have English. The annotation is part of the Mellon project; see [#130](https://github.com/clamsproject/aapb-annotations/issues/130).

### Specs

* Annotation Project Name - `spoken-lid`
* Annotator Demographics
    * Number of annotators - 3 native speakers, one per target language:
        * `a5` - Samoan
        * `a1` - Central Alaskan Yup'ik
        * `a3` - Spanish
    * Occupational description, age range, education

      > TODO: annotator demographics.
* Annotation Environment Information

  > TODO: name, version and documentation of the annotation tool.
* Project Changes
    * Number of batches - 1: [`mellon-slid-a`](../../batches/mellon-slid-a.txt), the assets fully annotated as of 2026-11-09.

## Tool Installation

> TODO: links to the annotation tool and its documentation.

## Annotation Guidelines

> TODO: link to, or copy of, the instructions given to the annotators.

### Preparation

The audio of each asset is cut into clips, and annotators label one clip at a time. The clips of one segmentation of an asset form a clip set. An asset can have more than one clip set, and clips can overlap, both across clip sets and between consecutive clips of one set. Time outside the clips was never presented to the annotators, so it is not annotated.

> TODO: how the clips were made (the clip-set names end in `_vadish` and `_sampled`), and the clip length.

### What to Annotate

* `label` - the language spoken in the clip, "mixed" when the clip has more than one language, or "other".
* `mixed-order` - for a mixed clip, the order of the languages (e.g. "English to Samoan").
* `notes` - free text, for example the accent or the speakers.

> TODO: the label options of the tool. Raw labels in the data drop come in several spellings, for example `Samoan` and `smo`, `English` and `eng`, `Mixed` and `mixed`, `Central Alaskan Yupik` and `esu`.

### Decisions, Differentiation, and Precision Level during Annotation

The gold data uses these labels (see [#130](https://github.com/clamsproject/aapb-annotations/issues/130)):

* Languages - Central Alaskan Yupik, Non-Central Alaskan Yupik, Samoan, Spanish, English.
* Mixed - a clip with more than one language. When the annotator gave the order of the languages, the gold also has it as a language order: two language labels joined by `>` (`English>Samoan` for English, then Samoan), or by `<>` when the speech goes back and forth between them (`Samoan<>English`).
* Other - any other language, or no language.
* No Label - a clip saved with an empty label.

#### Data Quality Efforts

* Times are clip boundaries, not exact boundaries of speech or of a change of language.
* Only time inside the clips is annotated. An evaluation should score only the time inside the clips of the gold annotator.

## Data Format and `process.py`

### Raw data

The data drop of a batch is a `YYMMDD-batchName` directory with one CSV file per asset, named by its GUID. Each row is the latest label of one annotator for one clip.

* Fields:
    * `annotator` - anonymous annotator ID (`a1`, `a3` or `a5`)
    * `clip-set` - name of the clip set
    * `clip` - number of the clip in its clip set, from 1
    * `start`, `end` - clip boundaries in seconds from the start of the asset
    * `label` - the raw label, as saved in the tool
    * `mixed-order` - order of the languages in a mixed clip, or empty
    * `notes` - free text, or empty
* Example:
```
annotator,clip-set,clip,start,end,label,mixed-order,notes
a1,esu_raw_clips_vadish,1,4.78,22.45,English,,
a3,spa_raw_clips_vadish,1,0.0,16.68,other,,No language audio
a5,smo_raw_clips_vadish,72,1112.96,1132.91,Mixed,English to Samoan,
```

### [`process.py`](process.py)

```bash
python3 process.py
```

The script reads every data drop next to it and writes one gold file per GUID to a fresh `golds/` directory. It stops if a GUID is in two data drops. It

* maps each raw label to its gold label (see [Decisions](#decisions-differentiation-and-precision-level-during-annotation)), case-insensitively; for example `smo` becomes `Samoan` and `esu` becomes `Central Alaskan Yupik`, and an unknown raw label stops the script;
* writes the language order of a mixed clip in the `>` or `<>` form: "A to B" (or "A -> B") and "A and B" (or "A & B") become `A>B`, and "A and B back and forth" becomes `A<>B`. The order comes from `mixed-order`, or from `notes` when `mixed-order` is empty and the whole note is such an order; the tool had no `mixed-order` field at first, so earlier orders are in the notes. The label wins: a clip with an order but a single-language label keeps its label, without an order;
* cuts each overlap between consecutive clips at its midpoint, so that the gold has one label at a time (the overlaps in this batch are 0.4 s);
* converts the times to `hh:mm:ss.mmm`.

The `annotator`, `clip-set`, `clip` and `notes` fields are not in the gold. The script reports on stderr the clips to check by hand: an order on a clip that is not mixed, an unreadable `mixed-order`, a `mixed-order` that differs from the order in the notes, and an order without the target language of the annotator.

### `golds` data

CSV files, one per GUID, with the clips of the asset in time order.

* Fields:
    * `start`, `end` - clip boundaries in `hh:mm:ss.mmm`
    * `scene-label` - the gold label (see [Decisions](#decisions-differentiation-and-precision-level-during-annotation))
    * `language-order` - for a `Mixed` clip, the order of its languages (`A>B` or `A<>B`), or empty
* Example:
```
start,end,scene-label,language-order
00:42:01.950,00:42:16.950,English,
00:42:16.950,00:42:31.950,Mixed,English>Samoan
00:42:31.950,00:42:46.950,Samoan,
```
