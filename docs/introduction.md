```{attention}
FairDM is still in the early stages of development. We are actively seeking contributors to help us build, test, and shape the future of the framework. If you are interested in contributing, please see our [Contributing](getting-started) page. If you want to keep up to date with the latest developments, please star the [GitHub repository](github.com/FairDM/geoluminate).
```

# Introduction

FairDM is an open-source web framework for building modern research data portals that strongly adhere to the FAIR data principles. It is designed to greatly simplify the process of creating, deploying and maintaining a research portal using a modern and well-supported technology stack. FairDM abstracts away many of the complexities of web development, allowing researchers and data managers to focus on their data and research, rather than the technical details outside their expertise.

FairDM is built around the popular Django Web Framework and provides a set of pre-defined design patterns, templates, and reusable components that enable the rapid development of high-quality research portals. By following a consistent design and development approach, FairDM ensures that all portals built using the framework are user-friendly, accessible, and interoperable. This standardization makes it easier for researchers and data users to navigate and interact with different portals, enhancing the overall user experience and promoting data sharing and collaboration.

## Mission Statement

```{epigraph}
Establish, maintain and support a framework for creation and deployment of decentralized, self-hosted and community-driven research data portals.
```

## Goals

1. **Simplify the process of declaring and distributing reuseable data structures**
   
   FairDM provides a set of pre-defined data structures and fields that are commonly used in research data management. These structures can be easily extended and customized to meet the specific requirements of individual research communities. By simplifying the process of defining data structures, FairDM enables researchers to focus on their data and research, rather than the technical details of the portal.

2. **Facilitate the deployment of research data portals**

   FairDM provides a set of pre-defined templates, design patterns, and components that enable the rapid development and deployment of research data portals. By following a consistent design and development approach, FairDM ensures that all portals built using the framework are user-friendly, accessible, and interoperable. This standardization makes it easier for researchers and data users to navigate and interact with different portals, enhancing the overall user experience and promoting data sharing and collaboration.

3. **Foster collaboration and networking within individual research communities**

   At the heart of FairDM lies a profound commitment to community building and fostering collaboration among researchers. Our web-framework is not just a technical solution; it's a catalyst for empowering research communities to thrive together. FairDM provides the perfect platform to unite researchers, innovators, and experts from various fields, facilitating seamless collaboration and knowledge exchange.

4. **Credit where credit is due**

   Proper attribution of credit for contributions towards scientific data collection and publication is vital for the integrity of the scientific record. It is also vital to the wider adoption of FairDM as a research data management tool. FairDM provides a robust system for tracking and attributing contributions to research data, ensuring that all contributors receive the recognition they deserve. 

5. **Community Driven**

   Research data portals should ultimately be powered by the research community they serve. FairDM is focused on functionality that allows researchers to take ownership of their data and collaborate with others in a secure and transparent environment. By fostering a sense of community ownership, FairDM empowers researchers to share their data, insights, and expertise with the wider scientific community.

## Philosophy

**Simplicity** - FairDM strives to be simple, straight-forward and easy-to-use for both portal users and portal developers.

**Consistency** - FairDM promotes "convention over configuration" and emphasizes consistency over flexibility. Portal developers should not have to worry about implementation details, but rather focus on build a data schema that reflects the needs of their research community.

**Batteries Included** - FairDM provides a robust set of built-in functionalities that are common to all research data portals. All mission-critical external services are predefined and provided to portal developers ready-to-go.

**Isolation** - FairDM portals are designed to be self-hosted and self-contained, allowing researchers to maintain full control over their data and portal infrastructure.

**Integration** - FairDM should not try to reinvent the wheel. It should, where possible, integrate with existing, well-defined and widely accepted tools and services from the research data management ecosystem. Integrations should never compromise the [FairDM vision](#vision).

**Interoperability** - FairDM portals should be completely interoperable with other FairDM portals. FairDM should, through use of common export formats, strive to be interoperable with external systems.
