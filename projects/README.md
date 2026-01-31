# Annotation Projects

All annotation projects for the AAPB-CLAMS collaboration are located in this directory. Each project contains gold datasets, documentation, and raw annotation data.

## Project Structure

Each project directory contains:

- **`golds/`** - The gold dataset files ready for machine consumption (training, evaluation, or other use)
- **`readme.md`** - Project-specific documentation and annotation guidelines
- **Raw annotation data** - Original annotation files organized by batch and date

## Using Gold Dataset Files

The gold dataset is a set of files in a format ready for machine consumption, primarily for:

1. Training ML models for CLAMS apps
2. Evaluation of CLAMS app outputs
3. Other public usage

Users of a gold dataset should be aware of the version they are using. We recommend using [permalinks](https://docs.github.com/en/repositories/working-with-files/using-files/getting-permanent-links-to-files) to refer to a specific version of the gold dataset in your code or documentation.

## Data Format Conventions

- **Media Time** = `hh:mm:ss.mmm` with a **DOT** (not a colon before milliseconds)
- Annotation times may have some imprecision due to the nature of audiovisual phenomena

See [CONTRIBUTING.md](../CONTRIBUTING.md#repository-level-conventions) for detailed information on data formats and field naming conventions.

## Current Projects

_This section is manually updated and may be incomplete._

* **[`january-slates`](january-slates/)** - Slates are actual visible frames within the video media that contain the metadata and other identifying information of that video (e.g. program name, director, producer). Project done in January; this is an outdated naming convention.

* **[`newshour-chyron`](newshour-chyron/)** - Drawn from the [NewsHour](https://americanarchive.org/special_collections/newshour) TV broadcast, this project annotates text appearing on screen, usually above or below the main action saying things such as "Breaking News", "Joan, author".

* **[`newshour-namedentity`](newshour-namedentity/)** - From NewsHour. This project annotated [named entities](https://www.techtarget.com/searchbusinessanalytics/definition/named-entity) found within the video _transcript_ along with which characters denoted that named entity and its type.

* **[`newshour-namedentity-wikipedialink`](newshour-namedentity-wikipedialink/)** - From NewsHour. This project used the previous project's dataset and added an extra label of which wikimedia link referred to the named entity annotated (e.g. https://www.wikidata.org/wiki/Q931148).

* **[`newshour-transcript-sync`](newshour-transcript-sync/)** - From NewsHour. This project found the start and end times for 10 tokens of closed captioning at a time from the transcript to the video.

* **[`role-filler-binding`](role-filler-binding/)** - This project uses the [role filler binding](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8019313/) linguistic theory to extract and organize OCR text into structured metadata pairs (typically a production role and the person filling that role).

* **[`role-filler-binding-seqtag`](role-filler-binding-seqtag/)** - Sequence tagging approach to role-filler binding.

* **[`scene-recognition`](scene-recognition/)** - This project builds the dataset meant to train ML models to recognize scenes/frames/timeframes of interest (slates, chyrons, credits, important people being interviewed) for metadata extraction.

* **[`understanding-chyrons`](understanding-chyrons/)** - Follow-up to scene-recognition focused on chyron text transcription.

* **[`understanding-slates`](understanding-slates/)** - Follow-up to scene-recognition, transcribing slate content.
