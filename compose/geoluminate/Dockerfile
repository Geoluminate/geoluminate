
FROM python:3.11-slim-bullseye as base

ARG DJANGO_ENV=production
ENV DJANGO_ENV=${DJANGO_ENV}
ENV DJANGO_SETTINGS_MODULE=config.settings.${DJANGO_ENV}
ENV PATH="/venv/bin:${PATH}"

RUN addgroup --system django \
    && adduser --system --ingroup django django

RUN apt-get update && apt-get install --no-install-recommends -y \
  # https://github.com/vishnubob/wait-for-it
  wait-for-it \
  # Translations dependencies
  gettext && \
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

USER django

WORKDIR /app

ENTRYPOINT ["entrypoint"]
