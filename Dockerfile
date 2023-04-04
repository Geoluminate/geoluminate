FROM python:3.9-slim-bullseye

ARG APP_DIR=/app

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg2 dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  # git
  # git-all \
  # geodjango dependencies
  binutils libproj-dev gdal-bin \
  # # cleaning up unused files
  # && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  # && rm -rf /var/lib/apt/lists/*