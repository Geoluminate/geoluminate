FROM python:3.9-slim-bullseye as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# ====================== BUILD STAGE ============================
FROM base as builder

ENV POETRY_VERSION=1.3.1

COPY pyproject.toml poetry.lock ./

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential && \
  # install poetry for dependencies   
  pip install "poetry==$POETRY_VERSION" && \
  # build requirements.txt file
  poetry export -o requirements.txt --with dev,docs && \
  # dependencies for building Python packages
  # # cleaning up unused files
  apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false  && \
  rm -rf /var/lib/apt/lists/*

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --wheel-dir /usr/src/app/wheels \
  -r requirements.txt 

FROM base as final

RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg2 dependencies
  # libpq-dev \
  # Translations dependencies
  gettext \
  # geodjango dependencies
  binutils libproj-dev gdal-bin \
  # spatialite dependencies
  libsqlite3-mod-spatialite && \
  # cleaning up unused files
  apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# copy python dependency wheels from python-build-stage
COPY --from=builder /usr/src/app/wheels /wheels/

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
	&& rm -rf /wheels/

# CMD ["./entrypoint"]