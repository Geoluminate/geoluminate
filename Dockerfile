FROM python:3.11-slim-bullseye

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.3.1

WORKDIR /app

RUN addgroup --system geoluminate \
    && adduser --system --ingroup geoluminate geoluminate

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # the python wheels for pycairo will not build without these and therefore package installation will fail. Pycairo is required through the following dependency tree django-cms > django-filer > easy-thumbnails[svg] > reportlab > pycairo
  libcairo2 libcairo2-dev \
  # Translations dependencies
  gettext \
  # geodjango dependencies
  binutils libproj-dev gdal-bin 
  # # cleaning up unused files
  # apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  # && rm -rf /var/lib/apt/lists/*

COPY --chown=geoluminate:geoluminate ./bin /scripts

# clean file endings and make all scripts executable
RUN find /scripts/ -type f -iname "*" -exec sed -i 's/\r$//g' {} \; -exec chmod +x {} \;


ENTRYPOINT ["/scripts/entrypoint"]
