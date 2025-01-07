# Background

```{epigraph}
The problem with the current research data portal landscape is not that there are too many chefs in the kitchen, but that each chef insists on using their own recipe.
```

(open-science)=
## Open Science

Open Science is a movement and set of practices aimed at making scientific research and its outputs more accessible, transparent, and collaborative. It represents a departure from traditional, closed models of scientific research in which data, methods, and findings are often kept behind paywalls, restricted to a select few, or not disclosed in a timely manner. Open Science promotes greater openness and accountability in the research process, with the goal of accelerating scientific discovery and fostering trust in scientific results.

Some key aspects of Open Science are:

(os/access)=
**Open Access** - refers to the practice of making research publications, such as journal articles and conference papers, freely available to the public. This allows anyone, regardless of institutional affiliation or financial resources, to access and read scientific research.

(os/data)=
**Open Data** - involves sharing the raw data collected during the research process with the public or the scientific community. This allows others to verify and reproduce research findings, promoting transparency and accountability.

(os/software)=
**Open Source Software** - Many scientific tools and software used in research are made open source, meaning their source code is freely available for inspection, modification, and redistribution. This fosters collaboration and innovation in software development for research.

(os/preprints)=
**Preprints** - Preprint servers are platforms where researchers can share early versions of their research papers before they undergo formal peer review. This accelerates the dissemination of research findings and allows for feedback from the scientific community.

(os/reproducibility)=
**Reproducibility and Replicability** - Open Science emphasizes the importance of conducting research in a way that makes it easy for others to reproduce or replicate the results. This includes providing detailed methods, code, and data to ensure the robustness of scientific findings.

(os/peer-review)=
**Open Peer Review** - Some Open Science initiatives advocate for more transparent and open peer review processes, where the identities of reviewers and their comments are made public, promoting accountability and fairness in the review process.

(os/citizen-science)=
**Citizen Science** - Open Science encourages the participation of non-professional scientists or citizens in the research process, often involving them in data collection, analysis, or problem-solving.

(os/collaboration)=
**Collaboration and Interdisciplinary Research** - Open Science promotes collaboration and knowledge sharing among researchers from different disciplines, institutions, and geographic locations, fostering a more inclusive and global research community.

The Open Science movement aims to address issues like the reproducibility crisis in science, reduce barriers to access scientific knowledge, and make research more democratic and accountable. It has gained traction in various scientific disciplines and is supported by organizations, governments, and funding agencies around the world.

(fair-data)=
## FAIR Data

"FAIR data" is a set of guiding principles and best practices designed to make data Findable, Accessible, Interoperable, and Reusable. These principles are intended to improve the management and usability of research data, especially in the context of scientific research. FAIR data principles were developed to address the challenges of data sharing and data management in the digital age, with the goal of enhancing the transparency, accessibility, and reuse of research data.

Here's what each component of the FAIR acronym stands for:

(fair-data/findable)=
**Findable** - data should have clear and machine-readable metadata associated with it. Metadata includes information about the data's content, context, and how to access it. Proper metadata ensures that data can be easily located through online search engines and data repositories.

(fair-data/accessible)=
**Accessible** - accessibility means that once data is found, it should be easy to access. This involves ensuring that data is stored in a location that is accessible to both humans and machines. Data should be available under clear terms and conditions, including any necessary access permissions or restrictions.

(fair-data/interoperable)=
**Interoperable** - interoperability ensures that data can be used and understood by different systems and applications. To achieve this, data should follow common standards and formats. This allows for the seamless exchange and integration of data from diverse sources.

(fair-data/reusable)=
**Reusable** - to promote data reuse, it should be well-documented and structured in a way that makes it understandable to others. This includes providing information on how the data was collected, processed, and can be properly cited. Data should also be available for long-term preservation.

The FAIR data principles are important for advancing scientific research, as they facilitate data sharing, collaboration, and the verification of research findings. They are particularly relevant in fields where data plays a central role, such as genomics, climate science, and various areas of biomedical research. Adhering to FAIR data principles not only benefits researchers but also contributes to the overall transparency and reliability of scientific research. Many funding agencies, institutions, and research communities are adopting FAIR data practices to support data-driven research.

## A Fragmented Landscape

The establishment of the FAIR data principles has kicked off an arms race in the world of research data management, as research and government organisations scramble to make their data FAIR. This arms race has led to a proliferation of research data portals, each with its own unique design, data structure, and functionality.
When cost is not an issue, development of research data portals can be handed to professional web developers who create bespoke portals tailored to the specific needs of their client. However, the cost of developing and maintaining such a portal can be prohibitive, and the lack of standardisation can make interoperabilty between portals a nightmare.
In the more common scenario, research data portals are developed in-house by researchers or data managers with limited web development experience. Given the enormous complexity of modern web development, such an undertaking can be overwhelming, leading to poorly designed, inconsistent, and difficult-to-use portals. Ultimately, the research world is left with a fragmented landscape of research data portals that are difficult to navigate, integrate, and reuse.


## The role of FairDM

FairDM embraces both Open Science and FAIR Data principles. Metadata related to research projects, datasets, contributors, samples, measurements and observations are stored in a structured format that is both machine- and human-readable. This metadata is then used to generate a web portal that is both Findable and Accessible. The web portal is designed to be Interoperable with other web portals that adhere to the same schema. Finally, the web portal is designed to be Reusable by other research communities.

FairDM aims to address these challenges by providing a simplified framework for constructing modern and intuitive research portals that adhere to the FAIR data principles. By offering a consistent design, reusable components, and a streamlined development and deployment process, FairDM empowers research institutions and organizations to create high-quality data portals efficiently and effectively.

<!-- 
# FairDM

## What is FairDM?

FairDM is a Python-based micro web framework that allows research communities to easily and declaratively define data models that capture and describe any information relevant to their specific research domain. It is designed to help researchers adhere to metadata schemas that make it easy to formally publish their datasets and properly attribute all individuals and organisations involved in their data collection and processing lifecycle. FairDM leverages the established tools and features of the Django Web Framework in order to build lasting research portals that will grow with your community's expectation into the future.


You can host your own community portal online, publish a container that others can install and run on their own servers or distribute a lite version that runs completely offline on a field laptop. All of this is possible with FairDM!

## What problems does FairDM solve?

### Data Quality and Metadata Standards

FairDM-powered portals are designed to help researchers adhere to metadata schemas that make it easy to formally publish their datasets and properly attribute all individuals and organisations involved in their data collection and processing lifecycle.

, making it easier for them to publish their datasets while ensuring that the necessary information for attribution is captured accurately. By following these established schemas, we streamline the process of documenting and sharing datasets, facilitating proper credit attribution throughout the research community.


### Data Ownership

Ownership and control of research data is perhaps one of the biggest barriers to open science and FAIR data.

Ownership of data is not just an issue for individuals looking to maintain control over their scientific data. Data ownership and proper accreditation are also incredibly important at both the institutional and national level.




### Data Interoperability

In order to decentralize the research data landscape, it is extremely important to facilitate data interoperability across numerous systems and platforms. This is where FairDM comes in. By providing a standardized schema for research data, FairDM ensures that data can be easily shared and integrated across different research communities and platforms.

## What other benefits does FairDM offer?

### Community building

FairDM allows you to focus on cultivating a strong sense of belonging within your research community. Through interactive features and engaging functionalities, you can nurture meaningful connections and foster a spirit of collaboration that transcends geographical boundaries.

### Collaboration


### Publication

FairDM provides a platform for researchers to publish their datasets, confident that their contributions will be appropriately acknowledged within the scholarly community.

 -->

