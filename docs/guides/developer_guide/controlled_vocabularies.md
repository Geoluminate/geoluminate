(controlled-vocabularies)=
# Controlled Vocabularies

This section of the guide will demonstrate how you can make use of published controlled vocabularies in your data schema and how to create and publish your own domain-specific controlled vocabularies.

## What are controlled vocabularies?

Controlled vocabularies are fundamental to research data management, providing semantic meaning and a structured approach to organizing and describing data. They ensure consistency and standardization in terminology across diverse datasets, enhancing the accuracy and precision of data classification. This uniformity facilitates data integration and interoperability, enabling researchers to effectively combine and compare datasets from various sources. Through careful use of controlled vocabularies, researchers can discover and retrieve relevant datasets more efficiently, thanks to standardized keywords and indexing.

In interdisciplinary research settings, controlled vocabularies serve as a common language, fostering collaboration and understanding among researchers from different fields. They support seamless data integration and analysis, allowing researchers to combine heterogeneous datasets for meaningful insights. Additionally, controlled vocabularies promote the reusability of research data and compliance with standards and regulations. By ensuring adherence to specific standards, they contribute to the long-term sustainability and impact of research data.


## What's wrong with doing it the Django way?




## How are they used?

Geoluminate provides two non-standard fields that allow you to add controlled vocabularies to your database:

- ConceptField: A field that allows you to add terms from a specific controlled vocabulary to an entity in the database.
- TaggableConcepts: A generic field that allows you to add terms from any controlled vocabulary to any entity in the database.

These fields enable you to enrich your data with standardized terminology, enhancing its discoverability and interoperability. By incorporating controlled vocabularies into your research data repository, you can ensure that your data is well-organized, searchable, and accessible to a wide audience of researchers and data scientists.


## How do I use them?


Geoluminate provides three ways for you to utilize controlled vocabularies in your data schema. You can:

a) Download an existing vocabulary from an online repository and store it within your codebase.
b) Link to an existing vocabulary from an online repository via URL.
c) Declare and publish your own custom vocabularies specific to your data schema.

<!-- link to existing vocabularies via URL, or declare and publish your own custom vocabularies specific to your data schema. By incorporating controlled vocabularies into your research data repository, you can ensure that your data is well-organized, searchable, and accessible to a wide audience of researchers and data scientists.


Controlled vocabularies are fundamental to research data management, providing semantic meaning and a structured approach to organizing and describing data. Geoluminate provides three ways to utilize controlled vocabularies in your schemas:

1. Download an existing vocabulary from an online repository and store it within your codebase.
2. Directly link to an existing vocabulary from an online repository via URL.
3. Declare and publish your own domain-specific vocabularies within you portal.

Whichever way, controlled vocabularies will ultimately enhance the findability and interoperability of data within your repository.   -->