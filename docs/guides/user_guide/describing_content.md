# Describing your dataset

There are a number of description types available within the Geoluminate framework that you can use to describe your 
dataset. These description types are based on the [Datacite](https://schema.datacite.org/) standards to ensure you can 
easily publish you datasets when the time is right. To help you get started, we have provided a number of examples:


## Overview of Description Types

1. **Abstract:**
The "Abstract" description type provides a brief summary of the dataset's content, purpose, and key findings. Limited to a specific character count (e.g., 2000 characters), the abstract offers a concise overview, making it easier for potential users and researchers to understand the dataset's relevance without having to go through the entire dataset.

2. **Methods:**
The "Methods" description type outlines the methodologies and experimental procedures used to generate the dataset. Researchers can grasp the data collection process and the steps taken to obtain the results.

3. **Series Information:**
For datasets belonging to a larger series or collection, the "Series Information" description type offers details about the overall series, aiding in grouping and organizing related datasets.

4. **Table of Contents:**
The "Table of Contents" description type presents a hierarchical or structured outline of the dataset's contents, allowing users to quickly navigate and comprehend the dataset's organization.

5. **Technical Info:**
The "Technical Info" description type contains relevant technical details, specifications, and formats associated with the dataset. Users can understand the data structure and compatibility with various software or tools.

6. **Other:**
The "Other" description type is a general category for any additional or supplementary information not covered by the previous types. It provides flexibility for dataset creators to include relevant details.

Including these various description types in the DataCite metadata schema enhances the completeness and usability of datasets, improving their discoverability and encouraging meaningful data reuse within the research community.


## Example Descriptions

The following example descriptions showcase how each description type adds specific context and information, making datasets more informative and valuable for researchers, funding agencies, and other stakeholders.

**Abstract:**

Investigating the impact of climate change on marine biodiversity in the Pacific Ocean. This dataset contains species distribution data for various marine organisms, collected through extensive field surveys and satellite remote sensing. The findings reveal significant shifts in species habitats, providing valuable insights for conservation efforts and sustainable resource management.

**Methods:**

To generate the dataset, we employed a combination of underwater surveys using SCUBA diving and satellite remote sensing data. The surveys covered 25 sites across the Pacific Ocean, and data on species occurrences were recorded for each site. Additionally, we used remote sensing data to monitor sea surface temperature and chlorophyll levels, enabling us to analyze the correlation between environmental variables and species distribution.

**Series Information:**

This dataset is part of the "Pacific Marine Biodiversity Study," a multi-year research initiative aimed at understanding the ecological impacts of climate change on marine ecosystems across the Pacific Ocean. Each dataset within the series focuses on different taxonomic groups, contributing to a comprehensive understanding of the region's biodiversity.

**Table of Contents:**

1. Species Distribution Data
  - Site 1: Lat: -12.345, Long: 123.456
  - Site 2: Lat: -10.987, Long: 145.789
  - ...
2. Environmental Variables
  - Sea Surface Temperature
  - Chlorophyll Levels
  - ...

**Technical Info:**

File Format: CSV
Data Resolution: 0.1-degree grid
Coordinate Reference System: WGS84
Satellite Data Source: Sentinel-2

**Other:**

The dataset includes a detailed species list with taxonomic classifications, field data collection protocols, and information on potential sources of data bias. It also provides supplementary visualizations, such as species distribution maps and environmental trend plots, to aid in data interpretation.

