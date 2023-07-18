
***Needs to be updated***

## Named Entity Linking

### Gold Data Generation
The input to this annotation project was from the `newshour-namedentity` annotation project in this repository. The `golds` directory contains the public gold dataset, generated using `process.py`. Files are in .tsv format. The relevant data fields are summarized below:

- __GUID__: The AAPB GUID of the annotated transcript. (_string_)
- __entity__: The span of text containing the entity. (_string_)
- __type__: The entity category. (_string_)
- __instances__: The number of instances of the entity within the source file. (_int_)
- __wiki_url__: The Wikipedia URL grounding the entity. (_string_)
- __QID__: The Wikidata URI linking the entity via Q identifier. (_string_)