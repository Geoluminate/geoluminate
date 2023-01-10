# pull official base image
FROM python:3.9
LABEL org.opencontainers.image.authors="Geoluminate"


# set work directory
WORKDIR /usr/src/app

# set environment variables

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
#  Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1
#  Pip will not cache package installs
ENV PIP_NO_CACHE_DIR=1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project from current dir to workdir in container
COPY ../ .

