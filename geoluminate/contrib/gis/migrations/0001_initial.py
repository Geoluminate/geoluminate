# Generated by Django 4.2.1 on 2023-06-07 18:42

from django.db import migrations


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("project", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Site",
            fields=[],
            options={
                "verbose_name": "Site",
                "verbose_name_plural": "Sites",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("project.sample",),
        ),
    ]