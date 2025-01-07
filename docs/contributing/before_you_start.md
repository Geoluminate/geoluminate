# Before you start

This guide is mainly for experienced Django developers that may wish to contribute to the development of the core FairDM framework. If you are looking for information on how to develop a FairDM-powered web application for your research community, please see the [Developer Guide](#developer-guide).

## Code of Conduct

As contributors and maintainers of this project, we pledge to follow the guidelines outlined in this code of conduct to foster an open and welcoming environment for everyone. We aim to ensure a harassment-free experience for all participants, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:

- Using welcoming and inclusive language
- Being respectful of different viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

- The use of sexualized language or imagery and unwelcome sexual attention or advances
- Trolling, insulting or derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information, such as physical or electronic addresses, without explicit permission
- Other conduct which could reasonably be considered inappropriate in a professional setting

### Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, wiki edits, issues, and other contributions that are not aligned with this code of conduct, or to temporarily or permanently ban any contributor for other behaviors that they deem inappropriate, threatening, offensive, or harmful.

### Scope

This code of conduct applies within all project spaces, including the repository and any other platform used to discuss and contribute to the project. It also applies when an individual is representing the project or its community in public spaces. Examples of representing a project or community include using an official project email address, posting via an official social media account, or acting as an appointed representative at an online or offline event.

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team at [EMAIL ADDRESS]. The project team will review and investigate all complaints and will respond in a way that it deems appropriate to the circumstances. The project team is obligated to maintain confidentiality with regard to the reporter of an incident. Further details of specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the code of conduct in good faith may face temporary or permanent repercussions as determined by other members of the project's leadership.

### Attribution

This Contributor Code of Conduct is adapted from the [Contributor Covenant](https://www.contributor-covenant.org), version 2.0, available at [https://www.contributor-covenant.org/version/2/0/code_of_conduct.html](https://www.contributor-covenant.org/version/2/0/code_of_conduct.html).

## Design Philosophy

1. Python > HTML > CSS > JavaScript

2. Fat Models, Thin Views

3. Reusability

4. Testing

5. Mobile Second

6. Accessibility

7. Internationalisation

8. Documentation

10. Security

11. Tutorials

## Repository Structure

    geoluminate/                  # Project directory
    │
    ├── api/                       # Management script for running commands
    ├── conf/                      # Project package directory
    │   ├── backends/            # Django settings for the project
    │   ├── settings/            # Django settings for the project
    │   ├── local.py                # URL declarations for the project
    │   └── production.py                # WSGI config for deployment
    ├── contrib/                  # Application directory
    │   ├── admin/               # Admin configurations
    │   ├── contributors/                # Application configurations
    │   ├── core/              # Database models
    │   ├── datasets/               # Test cases
    │   ├── organizations/                # URL declarations for the app
    │   └── projects/               # View functions
    │   └── reviews/               # View functions
    │   └── samples/               # View functions
    │   └── users/               # View functions
    │
    └── templates/                  # Directory for HTML templates
        └── app_name/              # Directory for app-specific templates
            └── base.html          # Base template file