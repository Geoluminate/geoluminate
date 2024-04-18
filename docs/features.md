# Features

## Deployment Ready

![Included services with new Geoluminate projects](/_static/deployment.png)

New Geoluminate projects are designed to be easily deployable to a variety of hosting environments. This is achieved through the use of Docker, a popular containerization technology that allows you to package your application and its dependencies into a single, portable unit. Geoluminate comes with a pre-configured docker-compose file that allows you to run a production-ready instance of your application with a single command. This makes it easy to deploy your research data portal alongside other mission-critical services such as PostgreSQL and Redis in a single, reproducible tech stack. Additionally, it allows other to replicate your work, deploying their own instance of your portal with minimal effort, which facilitates the decentralized [vision](#vision) of Geoluminate.


## Database Administration

![Database administration backend provided by Django](/_static/database_administration.png)

Geoluminate-powered applications inherit the full administrative capabilities provided by Django's built-in admin site. The admin site provides database administrators the ability to graphically interact with database tables, allowing them to easily view, add, modify, and delete entries. This streamlined interface simplifies database management tasks, even for users with limited technical expertise. From here, administrators can also manage user accounts, groups and roles, as well as configure global application settings and permissions.

```{seealso}
For more information on how to administer your research portal, check out the [Administration Guide](#admin-guide)
```


## User Accounts & Authentication

Django itself provides a built-in authentication system that works out of the box. Proper authentication measures ensure that only authorized users can create, edit or delete data, protecting the integrity and security of the underlying database. While the Django authentication method is useful, it lacks some of the functionality expected of a modern web application.

Geoluminate incorporates a 3rd party package called `django-allauth` (⭐8.8k, MIT License) to provide additional features such as social authentication, email verification, and password reset. Email verification is an essential mechanism to ensure that users are who they claim to be, while password reset functionality helps users regain access to their accounts if they forget their password. Social authentication allows users to sign up and log in using various external providers such as ORCID, Google, Facebook, and many more. 

`django-allauth`s social authentication allows users to sign up and log in using various external providers such as ORCID, Google, Facebook, [and many more](https://docs.allauth.org/en/latest/socialaccount/providers/index.html). By default, Geoluminate supports authentication via ORCID only but this is easily customizable.

```{note}
Geoluminate enables ORCID authentication by default, however, the developer of your portal will need to sign up for an ORCID developer account, request an access token, and configure Geoluminate to use that token. This can be done in the administration backend.
```

```{seealso}
How to [set up an alternative social authentication service](#social-accounts)
```

## Contributor Profiles

Geoluminate stores contributor profiles that can be linked to projects, datasets, and other entries within the core data model. These profiles can be used to store information about the contributor such as their name, email address, ORCID, and other relevant information. By linking contributors to entries within the core data model, you can easily track who contributed to a particular project, dataset, or any other entry. This information can be used to generate citations, track contributions, and provide credit to those who have contributed to the research.

Contributor profiles are completely public (except for the email address, which is hidden by default) and can be viewed by anyone who has access to the portal. Database administrators are welcome — and encouraged for the purpose of the scientific record — to create and maintain unclaimed contributor profiles using publicly available data, in particular ORCIDs. Being proactive in this regard will ensure that the scientific record is as accurate as possible, that contributors receive the credit they deserve, and that new users can claim an existing profile by signing up with (and verifying) either a matching email or authenticated ORCID. 

```{seealso}
- [The Contribution Framework](#contribution-framework)
- [How to manage contributor profiles](#contributor-profiles)
```

## Core Data Model

![Core data model of Geoluminate](/_static/core_data_model.png)

Metadata are collected within the Geoluminate framework at four distinct levels:

1. Project - a collection of one or more datasets that are related to a specific research topic or theme. Metadata collected at this level includes various textual descriptions, generic dates, collaborators, funding and more.

2. Dataset - a collection of data related to a specific research domain or hypothesis. Dataset-level metadata roughly align with the Datacite schema in order to facilitate formal publication of datasets. Formal publication is not provided explicitly within the Geoluminate framework, however, mechanisms are in place to easily pursue this option via external services such as GFZ Data Services which support the Datacite schema.

3. Sample - a physical or digital object that is collected, processed, and analyzed as part of a research project. A sample can have one or more measurements associated with it. Samples may be self-referencing, meaning the core data model allows you to break down a sample into discrete sub-samples (e.g. a borehole may be sub-sampled into discrete depth-intervals). Included fields at this level aim to facilitate minting of International Generic Samples Numbers (IGSNs) and other persistent identifiers for physical samples.

4. Measurement - a quantifiable observation of a sample. The core data model specifies a generic schema for capturing measurement metadata, which can be extended to accommodate domain-specific measurement types. The role of defining schemas for domain-specific measurements is left to the research community as a collaborative undertaking.


## Declarative Schema Definition

![Declarative schema declaration with Geoluminate and Django](/_static/schema_declaration.png)

Geoluminate makes it easy to declare fields and validators for your database tables in familiar, easy-to-understand syntax according to the exact specifications required by your research community. With Geoluminate, domain-specific data structures are defined by you so there is no need to adapt your requirements to fit generic structures defined elsewhere. Geoluminate provides a base `Measurement` class that you can extend to define your own data structures. This class allows you to leverage the full power of Django's model layer while also providing necessary metadata to properly describe your measurement. 

Unlike text-based, NoSQL alternatives, all fields listed in your measurement classes will directly alter your database schema, allowing you to harness the full capabilities of your underlying PostgreSQL database. Additionally, you can use Django's built-in ORM to interact with your database tables, making it easy to query, filter, and manipulate your data.


## Research Specific Fields

In addition to Django's standard database fields, Geoluminate provides custom fields that are particularly useful for research data:

- `QuantityField`: A numeric field that also stores basic units of measurement (e.g. meters, seconds, etc.) alongside the value and allows you to perform unit conversions.
- `ConceptField`: A field that stores a concept from a controlled vocabulary.
- `TaggableConcepts`: A generic relationship that allows you to tag any model with concepts from a controlled vocabulary. Great for keyword tagging.
- `FuzzyDateField`: A field that stores a date with an associated level of uncertainty.


## Multi-lingual

Geoluminate is fully internationalized, meaning the user interface can be translated into multiple languages. However, the user interface is only partially localized, meaning that it is not yet fully adapted to the specific needs of different countries or regions. We are working to improve this in future versions.


## Controlled Vocabularies

Geoluminate makes it easy to incorporate published vocabularies from an online repository into your data structures. Simply download the vocabulary and store it within your codebase, or link to it via URL. Alternatively, you can declare and publish your own domain-specific vocabularies that are specific to your data schema. By incorporating controlled vocabularies into your research data repository, you can ensure that your data is well-organized, searchable, and accessible to a wide audience of researchers and data scientists.


```{seealso} 
[How to use controlled vocabularies in your data structure](#controlled-vocabularies).
```
## Extendable


## Interoperable



## Community-Driven

Active community members are the lifeblood of Geoluminate-powered research data portals. Community members contribute data, share expertise, and shape the long-term future and sustainability of the online platform. By fostering a vibrant community, your research portal can become a hub for networking, collaboration, community-related news, knowledge sharing, and innovation.

Geoluminate aims to provide tools that foster community-engagement, collaboration, and support. These include discussion boards, activity feeds, member-to-member contact, and other features that enable users to connect and engage with each other. By helping to build a strong online community, Geoluminate ensures that your portal remains a valuable resource for researchers and data scientists around the world.


## Data Publishing

Geoluminate's core data model, especially at the Dataset level, is designed to facilitate data publishing within the [DataCite](https://datacite.org) ecosystem. While Geoluminate does not provide direct integration with DataCite, users may export their data and metadata in a format that is compatible with DataCite's requirements. This export can then be passed on to any one of the many DataCite member repositories for formal publication. 


## Standardized API

Standardized API access is crucial in order for research data portals to adhere to the FAIR data principles. APIs (Application Programming Interfaces) provide a structured and standardized way for users to interact with data, facilitating its accessibility and interoperability. Geoluminate-powered portals automatically generate and publish a RESTful API based on the core data model, enabling users to easily discover and access relevant information, regardless of the platform or tool they are using. This promotes data findability and accessibility, as researchers, organisations, commercial entities or members of the public can efficiently locate and retrieve relevant data without navigating through disparate systems or formats. Moreover, standardized APIs support interoperability by ensuring that data can be seamlessly integrated and exchanged between different systems, applications, and disciplines. This interoperability enhances collaboration and facilitates the reuse of data across diverse research endeavors. 

## Integrations

**ORCID**

ORCID (Open Researcher and Contributor ID) is a persistent digital identifier that helps in accurately and reliably attributing work to its creators, thereby reducing confusion over authorship and ensuring proper recognition for contributions to research. ORCIDs are increasingly being adopted by publishers, funders, universities, and other research-related organizations as a standard way of identifying and linking researchers to their work.

Geoluminate integrates with ORCID in order to facilitate proper accreditation of researchers and contributors. By leveraging ORCID, Geoluminate ensures that the necessary information for attribution is captured accurately, making it easier for researchers to publish their datasets while ensuring that their contributions will be appropriately acknowledged within the scholarly community.

Geoluminate makes it easy to associate an authenticated ORCID iD with a user account via 3rd party authentication during sign up.

**Research Organization Registry (ROR)**

ROR is a community-led project to develop an open, sustainable, usable, and unique identifier for every research organization in the world. ROR IDs are machine-readable, and they provide a way to link research organizations and their affiliations with research outputs, funding, and other scholarly activities.

<!-- Within the core Geoluminate data model, organizations  -->


## Modern Frontend

Geoluminate comes with a modern frontend that is built using the latest web technologies. The frontend is designed to be responsive, accessible, and user-friendly, ensuring that users can easily navigate the portal and interact with its features across a variety of devices and screen sizes. 
<!-- The frontend is also customizable, allowing you to tailor the look and feel of your research portal to suit your specific needs and branding requirements. By providing a modern and intuitive user interface, Geoluminate enhances the user experience and encourages engagement with the research data and resources available on the platform. -->



## Can't find what you're looking for?

Suggest a feature or improvement at our github repository [here](https://github.com/Geoluminate/geoluminate/discussions/new?category=features).

```{note}
You will need a Github account to suggest a feature or improvement.
```
