# Roadmap

This document outlines the objectives and goals for the development of the Geoluminate framework. It is intended to provide a high-level overview of the project's direction and priorities, and is subject to change as the project evolves. The roadmap is divided into target versions of the application, which each have several milestones representing a set of tasks and deliverables.

## V1.0.0

The primary goal in reaching version 1.0.0 is to establish a solid foundation for the project, including core functionality, documentation, and outreach. This version will serve as the basis for future development and expansion of the framework. It is critical that the core functionality is well thought through in order to avoid major refactoring in future versions that might lead to database migration issues.

### M1. Project Setup

- ✅ Set up the project structure and directory layout.
- ✅ Initialize version control with Git and create a repository.
- ✅ Choose a package management tool (e.g., Poetry, pipenv) and set up the project dependencies.

### M2. Build Foundations

- ✅ Configure a basic continuous integration (CI) workflow for automated testing and deployment.
- ✅ Initialize basic documentation.
- ✅ Create and publish a Docker image for building the core application
- ✅ Define mission-critical services for deployment.
- ✅ Orchestrate the build process for both local and production environments

### M3. Core Functionality

- ✅ Define the core functionality and features of the project.
- ✅ Design and implement an adaptable core data model that will serve as the backbone of the project.
- ✅ Design and implement basics for listing and filtering the core data model.
- ✅ Design and implement basic detail views for the core data model.
- ✅ Create a basic (read only) RESTful API around the core data model.
- 🔲 Write unit tests to ensure the correctness of the core functionality.
- 🔲 Conduct thorough testing and debugging to identify and fix any issues.

### M4. User Interface

- ✅ Design and develop an extendable user-friendly interface for interacting with the project.
- 🔲 Gather feedback from relevant or potential stakeholders regarding useability.
- 🔲 Perform usability testing to gather feedback and make necessary improvements.

### M5. Documentation and Examples

- ✅ Publish documentation online, describing the aims and intentions of the framework.
- ✅ Provide an overview of current and future capabilities.
- ✅ Explore the possibility of generating API documentation from code comments or docstrings.

### M6 Outreach

- ✅ Create a demo application attached to the website to showcase the project's capabilities.
- ✅ Enable discussions on GitHub to facilitate community engagement and support.
- 🔲 Create a website for the project to highlight its capabilities and features.
- 🔲 Create a blog to share updates and announcements about the project.
- 🔲 Create a social media presence to engage with the community and share updates.
- 🔲 Create a mailing list to share updates and announcements about the project.
- ✅ Create a GitHub organization to host the project and its related repositories.
- ✅ Create a GitHub repository to host the project's documentation.

### M7. Performance Optimization

- 🔲 Identify potential performance bottlenecks in the project.
- 🔲 Profile and measure the performance of critical components.
- 🔲 Optimize algorithms, data structures, and resource utilization for improved efficiency.
- 🔲 Conduct benchmarking and performance testing to validate optimizations.



## V2.0.0

### M5. Extended Functionality

- 🔲 Develop full CRUD capabilities for all levels of the core data model.
- 🔲 Design and develop an extensible multi-table import process for existing datasets

### M6. Documentation and Examples

- 🔲 Create a comprehensive developer guide so that new developers can get started with the framework. 
- 🔲 Create a comprehensive user guide to help application users contribute to their chosen portals.


### M8: Testing and Quality Assurance

- 🔲 Develop a comprehensive testing strategy, including unit tests, integration tests, and system tests.
- 🔲 Implement automated testing to ensure code integrity and prevent regressions.
- 🔲 Adopt code review practices to maintain code quality and enforce best practices.
- ✅ Perform static code analysis and adhere to style guidelines (e.g., PEP 8) for consistent and readable code.