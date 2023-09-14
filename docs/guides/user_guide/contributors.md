# Users, Organisations & Contributors


## What is a user?

A user is any person who has signed up for an account with the online platform and has verified their email address. Users can create and manage datasets, upload files, and publish their datasets to make them publicly available. Users can also create and manage organizations, which are groups of users that can collaborate on datasets and share resources. Information stored with the user account is used to ensure the application runs smoothly and to provide a personalized experience for each user. 

<!-- Each user is associated with a public ContributorProfile containing data that can be displayed within the application. This data includes the user's preferred name, related identifiers (ORCID, etc) and institutional affiliation. Users can also add additional information to their profile, such as a biography, website, and social media links. This information is used to identify and properly attribute the user's contributions to data submissions within the context of the application. -->

<!-- Include an ERD here of the relationship between user/profile/contribution objects -->


## What is a Contributor?

In order to facilitate formal publishing of datasets, Geoluminate closely follows the DataCite metadata schema for contributors. Within the DataCite schema, a contributor can be assigned to either a person **or** an organization. To handle this within the application, users and organisations are both associated with a public ContributorProfile, which is used to populate the required fields for a contributor as per the DataCite schema.

A ContributorProfile is a public profile associated with a user account. It contains information about the user, such as their preferred name, institutional affiliation, and related identifiers (ORCID, etc). Users can also add additional information to their profile, such as a biography, website, and social media links. This information is used to identify and properly attribute the user's contributions to data submissions within the context of the application.


## What is a contributor?




```{atttention}
A contributor is not necessarily associated with a user.
```

In the DataCite metadata schema, contributors play a crucial role in acknowledging the individuals or entities that have contributed to the creation of a dataset. Contributors can include researchers, authors, institutions, funding agencies, and other parties involved in different aspects of dataset creation and dissemination. The DataCite schema defines various contributor types to categorize these different roles. 

By utilizing these contributor types in the DataCite schema, datasets can properly recognize and attribute the efforts of individuals and organizations involved in their creation, maintenance, and dissemination. This enhances transparency and facilitates proper citation and credit within the scientific community.

## Contributor Types

Here's an explanation of the main contributor types:

1. **Creator:**
The primary individuals or entities responsible for conceiving and creating the dataset. Creators are typically the main authors or researchers who have directly contributed to the dataset's content and intellectual property.

2. **Editor:**
Individuals or entities who have reviewed, revised, or curated the dataset but might not be the original creators. Editors may play a role in improving the dataset's quality, structure, or metadata.

3. **DataCollector:**
Contributors who have collected or assembled the data that constitutes the dataset. They are responsible for gathering and compiling the raw data used in the research.

4. **DataManager:**
Individuals or entities who have managed the dataset, ensuring its proper organization, storage, and maintenance. Data Managers are responsible for data curation and data stewardship.

5. **Producer:**
Entities responsible for generating the dataset or making it publicly available. Producers can include data repositories, archives, or data centers that host and maintain the dataset.

6. **ProjectLeader:**
The principal investigator or lead researcher who has overseen the project or research that led to the dataset's creation.

7. **Researcher:**
Other contributors who have made substantial contributions to the dataset but do not fit into the categories mentioned above. Researcher can include collaborators, team members, or partners involved in the research project.

8. **RightsHolder:**
Individuals or entities that hold copyright or other rights to the dataset. The RightsHolder might not be the same as the Creator, especially in cases where datasets are produced within an institution or organization.

9. **Sponsor:**
Funding agencies or organizations that have provided financial or other support for the research project leading to the dataset's creation.

10. **Other:**
A catch-all category for contributors whose roles do not fit into the predefined types mentioned above. This allows flexibility for acknowledging various contributions.


## Additional Information

In the DataCite metadata schema, each contributor can be associated with additional information to provide more context about their role and contribution to the dataset. Here is the additional information that can be stored with each contributor:

1. **Contributor Name:**
The name of the individual or entity associated with the contributor role. This can include the full name, organization name, or both.

2. **Contributor Identifier:**
An optional field that allows for the inclusion of a unique identifier associated with the contributor. This identifier can be an ORCID (Open Researcher and Contributor ID) for individual researchers, or other identifier systems for organizations.

3. **Contributor Type:**
The specific role or type of contribution the contributor has made to the dataset. This corresponds to the contributor types mentioned earlier, such as Creator, Editor, DataCollector, DataManager, Producer, ProjectLeader, Researcher, RightsHolder, Sponsor, or Other.

4. **Contributor Affiliation:**
The institutional or organizational affiliation of the contributor. This field helps identify the institutional context of the contributor's involvement in the dataset creation.

5. **Contributor ORCID:**
If applicable, the ORCID (Open Researcher and Contributor ID) associated with the contributor. ORCID is a unique identifier for researchers, ensuring proper attribution and disambiguation of authorship.

6. **Contributor Role:**
An optional field that provides more specific details about the contributor's role or responsibilities related to the dataset.

7. **Contributor Email:**
The email address of the contributor. Including contact information can be beneficial for establishing communication with contributors if needed.

8. **Contributor URL:**
A URL associated with the contributor, such as their personal website or institutional profile. This provides additional context and allows users to learn more about the contributor.

By storing this additional information with each contributor, the DataCite metadata schema enables comprehensive attribution and proper citation of contributors' contributions to the dataset. Researchers, funding agencies, and other stakeholders can access this information to understand the dataset's origin, the roles of various contributors, and ensure appropriate credit is given to those involved in the dataset's creation and dissemination.

