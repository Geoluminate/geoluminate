FROM python:3.11-slim-bullseye as base


ARG BUILD_ENVIRONMENT=production

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR /app

RUN addgroup --system django \
    && adduser --system --ingroup django django

RUN apt-get update && apt-get install --no-install-recommends -y \
  # Translations dependencies
  gettext \
  # geodjango dependencies - https://docs.djangoproject.com/en/4.2/ref/contrib/gis/install/geolibs/
  binutils libproj-dev gdal-bin && \
  # cleaning up unused files
  apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*


# copy entrypoint and command scripts
COPY ./compose/geoluminate/bin/ /usr/local/bin/maintenance/

# fix line endings and make scripts executable, move scripts to /usr/local/bin
RUN sed -i 's/\r$//g' /usr/local/bin/maintenance/* && \
    chmod +x /usr/local/bin/maintenance/* && \
    mv /usr/local/bin/maintenance/* /usr/local/bin && \
    rmdir /usr/local/bin/maintenance

ENTRYPOINT ["entrypoint"]
