"""Command that copies the base Geoluminate file structure
into the users current working directory. Should be used
in place of ``django-admin startproject``
"""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Starting celery worker with autoreload...")
