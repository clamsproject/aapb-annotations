# News Hour Named Entity

## Project Overview
The namedentity project creates a dataset of the [named entities](https://www.techtarget.com/searchbusinessanalytics/definition/named-entity#:~:text=In%20data%20mining%2C%20a%20named,phone%20numbers%2C%20companies%20and%20addresses.)
that appeared in the transcripts of old news broadcasts. Named Entities are used in Natural Language Processing to identify named subjects of interest from media.
This dataset provides a learnable dataset of what named entities  are specifically found in a piece of media, which can aid in the automatic searching for other named entities in other media or other language processing after finding those named entities.
For CLAMS, one use case is to extract these named entities as metadata tags, allowing for quicker searching of topics or keywords from within videos. (E.g. Someone searching for President Jimmy Carter with the AAPB collection via text search.)

The namedentity project was the first annotation project Gabe annotated for WGBH. It precedes the namedentitywiki project which builds on this.

### Specs
* Annotation project name - `newshour-namedentity`
* Annotator Demographics
    * Number of annotators - 1
    * Occupational description - College student
    * Age range - 20s
    * Education - College
* Annotation Environment information
    * Name - (enter)
    * Version - (enter)
    * Tool Documentation - (see below tool installation)
* Project changes
    * Number of Batches - (enter)
    * Other Version Control Information - (enter, if applicable)
Gabriel Michael Alexander (College student age, (other demographic information), Lang: Eng US native speaker, Organization: GBH)
Annotation Environment information -
    Name: Brat
    Version: Unknown
    Link/Tool Used/User Manual: (See below Tool Installation)
Project changes -
    Project Version: Unknown/1.0
    Number of Batches: 1
    Other Version Control Information: None


### Data Overview
INPUT - transcripts in `.txt` format that match the audio or other information in a video.
INTERMEDIATE RAW OUTPUT - `.ann` file where each line is a new instance of a named entity.
```
FORMAT:
tag#\tcategory first_character last_character\tentity_text
```
```
EXAMPLE:
T1	person 2 12	JIM LEHRER
T2	person 32 42	Jim Lehrer
T3	program_title 51 59	NewsHour
```
FINAL PREPARED GOLD OUTPUT - same `.ann` file again.
```
the raw .ann file is directly copied for gold.
```
Information on the `.ann` [file format](https://brat.nlplab.org/standoff.html) is here.

## Tool Installation: Brat
brat rapid annotation tool
[Brat and Installation Instructions](https://brat.nlplab.org/index.html)
_TODO: Find the specific usage of the tool._

## Annotation Guidelines: Transcribing/Closed Captioning

### What to annotate

These guidelines are based on the [OntoNotes guidelines](https://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/AnotGuideEnNE.pdf), the [EuroParl Named Entity Annotation Guidelines](https://people.csail.mit.edu/andreeab/corpus/annotationGuidelines.pdf) and the [ELDA MAPA guidelines](http://portal.elda.org/media/filer_public/2022/05/10/mapa_annotation-guidelines-v6.pdf).

We annotate six kinds of named entities: Person, Location, Organization, Product, Event and Title.

Some general guiding principles:

- Only annotate noun phrases.

- Always annotate considering the nature of the entity as used in the text.

  - Samsung (referring to the organization) is an Organization. Samsung (referring to a smartphone) is a Product. The same is true for Ford in “Ford opened a new factory" and "She bought a Ford".

  - Charles de Gaulle in “I landed at Charles de Gaulle” is a LOCATION, but in “Charles de Gaulle was born in 1890” it is a PERSON.

- In some cases it may be impossible to decide between two or more types of named entity, in that case the text extent should be annotated multiple times, one for each entity type that is being considered.

- In general do not include determiners and other modifiers.

### NE types
We now look at the annotation types one by one and give some more details.

#### Person

Proper names of people including first names, last names, individual or family names, fictional names and unique nicknames. Include the following in the extent of the annotation:

- Titles including names of posts and job titles:
	Mr., Ms, Queen, Sir, Dr., Judge, CEO
- Generational markers such as Jr. and IV.

Do not annotate definite descriptions like "the plumber" or "the CEO of Microsoft" even though they may uniquely identify a person.

Examples:
- Ray Parker Jr.
- Dr. Brown
- St. Marks
- Queen Elizabeth II
- Charlie Brown
- President Kennedy
- First Lady Michelle Obama
- Judge Brown

With cases like "Microsoft CEO Bill Gates" we annotated "Microsoft" as an Organization and "CEO Bill Gates" as a Person.


#### Location

Names of geographical administrative entities including countries, villages, cities, states, provinces, prefectures, and other forms of municipalities.

Examples:
- Paris
- California
- United Kingdom

Names of man-made structures, including buildings, airports, stations, infrastructures (bridges and streets), monuments, oil fields, golf courses, hospitals, zoos, shopping centers, etc. Facility names can be ORG depending on context.

Examples:
- Brooklyn Bridge, Fenway Park
- Madison Avenue
- 42nd Street
- Eiffel Tower
- Statue of Liberty
- City Library

Names of celestial bodies, stars, continents, mountains, oceans, coasts, rivers, lakes, borders, etc. Named regions, areas, and neighborhood such as "Middle East", "Europe", and "East Village" are included in this category.

- Hudson River
- Europe
- Brighton Beach
- Long Island
- Latin America
- Silicon Valley
- Earth
- Greenwich Village

Annotate colloquial names for locations, for example "Southie".

With cases like "Greenwich Village, New York", use just one tag, not two.

Some organization names include locations, for example "University of Colorado at Boulder". Here, "Boulder" is a Location, but we annotate the full span as an Organization. The same holds for "University of California, Berkeley" where we annotate the entire span.

The distinction between Location and Organization can be tricky. With "Russia" invaded Ukraine" we annotate "Russia" as an Organization and "Ukraine" as a Location.

Open questions:

- What to do with "university campus at Berkeley", the "candy store on High Street", etcetera? These examples narrow down the location given another location. My hunch is to only annotate "Berkeley" and "High Street".


#### Organization

Names of companies, government agencies, political parties, educational institutions, sport teams, hospitals, museums, libraries etc.

Examples:
- IBM
- Capitol Hill / White House
- Democratic Party
- Hilton Hotel
- New York Stock Exchange
- LIFE Magazine / New York Times
- Japanese government
- Obama administration

New York Times-CBS --> annotate as two different annotations

Carnegie-Mellon --> one org




#### Product

Name of any product including non-commercial vehicles (automobiles, rockets, aircraft, ships). References including manufacturer and product names are marked together as one entity, products using only their manufacturer’s name (as in “I bought a Ford”) are also marked. Financial products and services are also included in this category.

- Ford Taurus
- Ford
- Space Shuttle Discovery
- Coca Cola
- Roth IRA


#### Event

Named events and phenomena including natural disasters, hurricanes, revolutions, battles, wars, demonstrations, concerts, sports events, etc.

Examples:

- Hurricane Hugo
- Vietnam War
- Mexican Revolution
- 2016 World Cup


#### Title

Titles of books, songs, films, plays and other creations such as awards, stock price indexes, and social security systems including health insurance systems or pension plans. Newspaper headlines are marked with NE-ART only when they are referential. Headlines used as "headlines" should not be marked. Series names, as in the "Harry Potter series", are also marked.

This could probably be discussed more, but the current tool has actually four separate categories: ProgramTitle, PublicationTitle, ArtworkTitle and WebsiteTitle. ProgramTitle is for program and film titles. PublicationTitle is for titles of books, book series, journals, newspapers, magazines and other published items. ArtworkTitle is for other artworks like paintings, sculptures, albums and songs.

### Preparation
Import the transcripts through brat. This tool seems to require a mouse.
### Process of Annotating
**Named Entity Phrase Text** - After importing the transcripts through brat, annotation is done by highlighting words or phrases.
**Category** - Then right click to categorize the highlighted phrase.
Options include `person, organization, program_title, publication_title, product, location, & event`.
**Character Start Offset** & **Character End Offset** - These two numbers entail which chars in the text file span the named entity's text.
This information is automatically added to the raw dataset file by the brat tool.
e.g. "Jim Lehrer" spans from character 32 inclusive to character 42 exclusive, taking up 10 letters. The first character of a file is 0.
_(Note, Wikipedia link is not used in this project. It's used in the [next project](https://github.com/clamsproject/aapb-annotations/tree/main/newshour-namedentity-wikipedialink).)_

### Decisions, Differentiations, and Precision during Annotation
**Category Disambiguation** - While this process is relatively straightforward, there are times when it can be difficult to place an item under one category umbrella.
For example, Washington can refer to the US capital, the organization within it, or the northwestern state.
A similar issue can arise with colleges, many of whom are named after the state or city they're located in. In these cases, context is key.
A relatively reliable rule of thumb is, if a location is mentioned, but no politicians or professors are brought up, then file it under location. Otherwise, file it under organization.
Aside from that, this annotation does not tend to be too demanding.

**Transcript Match** - Please ensure the transcripts accurately reflect the video that they are supposed to match.
Please also consider whether the transcripts and labelling should label only spoken text or also extraneous script information such as the name of who is speaking, non-spoken information, etc.

**General Typos** - As with anything with text, there is a possibility of typos. Data Quality checks such as for typos have not been done either dataset.

## Gold Generation and Dependencies - Codebase
_TODO: to be added_
_TODO (discrepancy): It seems that the process.py information to transform from raw to gold is no longer needed. This requires continued investigation. If the process here is not necessary, it should be deleted._

