# Named Entity Annotation Guidelines

These guidelines are based on the Ontonotes guidelines, the EuroParl Named Entity Annotation Guidelines and the ELDA MAPA guidelines.

Some Guiding Principles:

- Only annotate noun phrases.

- Annotation always needs to be done considering the nature of the entity as used in the text.

  - Samsung (referring to the organisation) is an organization. Samsung (referring to a smartphone) is a product. The same is true for Ford in “Ford opened a new factory" and "She bought a Ford".

  - Charles de Gaulle in “I landed at Charles de Gaulle” is a LOCATION, but in “Charles de Gaulle was born in 1890” it is a PERSON.


## Annotation types

We annotate four kinds of named entities: Person, Location, Organization and Product.


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
- Microsoft CEO Bill Gates
- First Lady Michelle Obama
- Judge Brown


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


### Organization

Names of companies, government agencies, political parties, educational institutions, sport teams, hospitals, museums, libraries etc.

Examples:
- IBM
- Capitol Hill / White House
- Democratic Party
- Hilton Hotel)
- New York Stock Exchange)
- LIFE Magazin / New York Times
- Japanese government
- Obama administration


### Product

Name of any product including non-commercial vehicles (automobiles, rockets, aircraft, ships). References including manufacturer and product names are marked together as one entity, products using only their manufacturer’s name (as in “I bought a Ford”) are also marked. Financial products and services are also included in this category.

- Ford Taurus
- Ford
- Space Shuttle Discovery
- Coca Cola
- Roth IRA


## Entity Linking

Also known as grounding. The idea is to provide a link to some authority. The authority we use is probably going to be [Wikipedia](https://www.wikipedia.org/). Grounding is not always possible, but in a case like *Jim Lehrer was a news anchor for the PBS NewsHour on PBS* we can add a link to [https://en.wikipedia.org/wiki/Jim_Lehrer](https://en.wikipedia.org/wiki/Jim_Lehrer).

As an alternative to Wikipedia we may use the [Library of Congress Authorities](https://authorities.loc.gov/).
