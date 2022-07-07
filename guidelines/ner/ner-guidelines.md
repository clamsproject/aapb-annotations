# Named Entity Annotation Guidelines

These guidelines are based on the [OntoNotes guidelines](https://www2.nict.go.jp/astrec-att/member/mutiyama/ALT/AnotGuideEnNE.pdf), the [EuroParl Named Entity Annotation Guidelines](https://people.csail.mit.edu/andreeab/corpus/annotationGuidelines.pdf) and the [ELDA MAPA guidelines](http://portal.elda.org/media/filer_public/2022/05/10/mapa_annotation-guidelines-v6.pdf):

We annotate six kinds of named entities: Person, Location, Organization, Product, Event and Title.

Some general guiding principles:

- Only annotate noun phrases.

- Always annotation considering the nature of the entity as used in the text.

  - Samsung (referring to the organization) is an Organization. Samsung (referring to a smartphone) is a Product. The same is true for Ford in “Ford opened a new factory" and "She bought a Ford".

  - Charles de Gaulle in “I landed at Charles de Gaulle” is a LOCATION, but in “Charles de Gaulle was born in 1890” it is a PERSON.

- In some cases it may be impossible to decide between two or more types of named entity, in that case the text extent should be annotated multiple times, one for each entity type that is being considered.

- In general do not include determiners and other modifiers.

We now look at the annotation types one by one and give some more details.

### Person

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


### Location

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


### Organization

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




### Product

Name of any product including non-commercial vehicles (automobiles, rockets, aircraft, ships). References including manufacturer and product names are marked together as one entity, products using only their manufacturer’s name (as in “I bought a Ford”) are also marked. Financial products and services are also included in this category.

- Ford Taurus
- Ford
- Space Shuttle Discovery
- Coca Cola
- Roth IRA


### Event

Named events and phenomena including natural disasters, hurricanes, revolutions, battles, wars, demonstrations, concerts, sports events, etc.

Examples:

- Hurricane Hugo
- Vietnam War
- Mexican Revolution
- 2016 World Cup


### Title

Titles of books, songs, films, plays and other creations such as awards, stock price indexes, and social security systems including health insurance systems or pension plans. Newspaper headlines are marked with NE-ART only when they are referential. Headlines used as "headlines" should not be marked. Series names, as in the "Harry Potter series", are also marked.

This could probably be discussed more, but the current tool has actually four separate categories: ProgramTitle, PublicationTitle, ArtworkTitle and WebsiteTitle. ProgramTitle is for program and film titles. PublicationTitle is for titles of books, book series, journals, newspapers, magazines and other published items. ArtworkTitle is for other artworks like paintings, sculptures, albums and songs.


## Entity Linking

Also known as grounding. The idea is to provide a link to some authority. The authority we now use is [Wikipedia](https://www.wikipedia.org/), but we may introduce others, for example the [Library of Congress Authorities](https://authorities.loc.gov/). The link is provided as a property on one of the annotation types above. The annotator should have the Wikipedia main page open and type in the named entity. If this resolves to a Wikipedia article which is about the same entity as mentioned in the text, then add the wikipedia link.

Grounding is not always possible, but in a case like *Jim Lehrer was a news anchor for the PBS NewsHour on PBS* we can add a link to [https://en.wikipedia.org/wiki/Jim_Lehrer](https://en.wikipedia.org/wiki/Jim_Lehrer).
