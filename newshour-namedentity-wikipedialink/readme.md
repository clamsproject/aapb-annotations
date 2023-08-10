
***Needs to be updated***

## Named Entity Linking

### Gold Data Generation
The input to this annotation project was from the `newshour-namedentity` annotation project in this repository. The `golds` directory contains the public gold dataset, generated using `process.py`. Files are in .tsv format. The relevant data fields are summarized below:

- __guid__: The AAPB GUID of the annotated transcript. (_string_)
- __anno_id__: The text-bound annotation ID. (_string_)
- __type__: The entity category-- person, location, event, organization, title (_string_)
- __begin_offset__: The character offset beginning the text span. (_int_)
- __end_offset__: The character offset ending the text span. (_int_)
- __text__: The entity. (_string_)
- __type__: The entity category. (_string_)
- __wiki_url__: The Wikipedia URL grounding the entity. (_string_)
- __qid__: The Wikidata URI linking the entity via Q identifier. (_string_)

note: for purposes of evaluation, the subtypes of the 'title' category are collapsed into one group.