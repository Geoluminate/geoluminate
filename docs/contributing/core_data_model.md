(core-data-model)=
# Core Data Model

```{figure} ./images/core_data_model.png
---
alt: Geoluminate data model
---
The anonymous user toolbar toggle which opens the anonymous user toolbar.
```

## Introduction

The core data model of Geoluminate is designed to capture and describe any information relevant to a specific research domain. It is a set of structured data models that are used to capture metadata related to research projects, datasets, contributors, samples, measurements, and observations. The core data model is designed to be both machine- and human-readable, allowing researchers to formally publish their datasets and properly attribute all individuals and organizations involved in the data collection and processing lifecycle.

<!-- insert core data model image -->
![Core Data Model](../images/core_data_model.png)

Metadata are collected within the Geoluminate framework at four distinct levels:

Level 1. **Project**: A project is a collection of one or more datasets that are related to a specific research topic or theme. Metadata collected at this level includes various textual descriptions, generic dates, collaborators, funding and more.

Level 2. **Dataset**: A dataset is a collection of data related to a specific research domain or hypothesis. Dataset-level metadata roughly align with the Datacite schema in order to facilitate formal publication of datasets. Formal publication is not provided explicitly within the Geoluminate framework, however, mechanisms are in place to easily pursue this option via external services such as GFZ Data Services which support the Datacite schema.

Level 3. **Sample**: A sample is a physical or digital object that is collected, processed, and analyzed as part of a research project. A sample can have one or more measurements associated with it. Samples may be self-referencing, meaning the core data model allows you to break down a sample into discrete sub-samples (e.g. a borehole may be sub-sampled into discrete depth-intervals). Included fields at this level aim to facilitate minting of International Generic Samples Numbers (IGSNs) and other persistent identifiers for physical samples.

Level 4. **Measurement**: A measurement is a quantifiable observation of a sample. The core data model specifies a generic schema for capturing measurement metadata, which can be extended to accommodate domain-specific measurement types. The role of defining schemas for domain-specific measurements is left to the research community as a collaborative undertaking.





# Centralization and decentralization

Data structures and metadata schemes at the measurement level should be designed collaboratively by the research community to ensure that information necessary to calculated data quality metrics is captured.

Therefore, a centralized authority should be established (or assigned) to oversee the development and maintenance of a measurement level schema that accurately captures the necessary information for measurement types relevant to a specific research domain.
