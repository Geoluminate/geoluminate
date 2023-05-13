FROM python:3.11-slim-bullseye

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.3.1

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  # the python wheels for pycairo will not build without these and therefore package installation will fail. Pycairo is required through the following dependency tree django-cms > django-filer > easy-thumbnails[svg] > reportlab > pycairo
  libcairo2 libcairo2-dev \
  # geodjango dependencies
  binutils libproj-dev gdal-bin && \
  # upgrade pip to the latest version
  pip install --upgrade pip && \
  # install poetry for dependencies
  pip install "poetry==$POETRY_VERSION" && \
  # cleaning up unused files 
  apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*