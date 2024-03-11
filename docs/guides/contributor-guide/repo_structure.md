# Repository Structure

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
