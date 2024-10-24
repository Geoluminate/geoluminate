# Deployment to a production server

## Understanding the production.yml file

This file contains all services necessary to run the application in a single server production environment. It
includes the following services:

  - Django application:
      - The main application that serves the web pages and API endpoints. It is built from the Dockerfile located
        at ./compose/production/django.
  - PostgreSQL database:
      - The database that stores all the data for the application.
  - Redis:
      - The in-memory data structure store that is used as both a message broker for Celery workers and a cache for
        the Django application.
  - Celery workers:
      - The background workers that process asynchronous tasks such as sending emails, processing uploaded files, and
        other long-running tasks.
  - Celery beat:
      - The scheduler that sends tasks to the Celery workers at specified intervals.
  - Flower:
      - The web-based monitoring tool for Celery workers and tasks. It is available at tasks.${DJANGO_DOMAIN}.
  - Minio:
      - The object storage server that is used to store media files such as images and documents. It is available at
        media.${DJANGO_DOMAIN}. The dashboard is available at minio.${DJANGO_DOMAIN}.
      - NOTE: this service can be commented or deleted if you are using an external S3 based service such as AWS S3.
  - Traefik:
      - The reverse proxy and load balancer that routes incoming requests to the appropriate services. It also
        automatically requests and renews SSL certificates from Let's Encrypt.


## Deployment configuration

### What are environment variables?

### Where can I declare environment variables?

From highest to lowest precedence:

- production.yml (not recommended)
- stack.env (or Portainer environment variables)
- deploy/config/*.env
- system environment variables


### Which environment variables take precedence?