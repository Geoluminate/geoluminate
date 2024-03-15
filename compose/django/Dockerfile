FROM geoluminate/geoluminate:latest as base

# ====================== BUILD STAGE ============================
FROM base as build-stage

ENV POETRY_VERSION=1.3.1

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg2 dependencies
  libpq-dev \
  # dependencies for building Python packages
  build-essential && \
  # install git
  apt-get install -y git && \
  # install poetry for dependencies
  pip install "poetry==$POETRY_VERSION" && \
  # cleaning up unused files
  apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false  && \
  rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

# Create Python Dependency and Sub-Dependency Wheels.
RUN poetry export --without-hashes -o requirements.txt --with dev && \
  pip wheel --wheel-dir /usr/src/app/wheels \
  -r requirements.txt

# # ====================== RUN STAGE ============================
FROM base as run-stage

# update system and install apt packages
RUN apt-get update && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    rm -rf /var/lib/apt/lists/*

# copy wheels from build-stage
COPY --from=build-stage /usr/src/app/wheels /wheels/

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
	&& rm -rf /wheels/
