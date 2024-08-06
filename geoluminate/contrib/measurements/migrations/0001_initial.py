# Generated by Django 5.0.6 on 2024-07-22 09:07

import django.contrib.postgres.fields
import django.db.models.deletion
import django_bleach.models
import geoluminate.contrib.core.models
import geoluminate.contrib.measurements.choices
import geoluminate.db.fields
import meta.models
import polymorphic.showfields
import research_vocabs.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("contributors", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Date",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="When this record was created.",
                        verbose_name="Created",
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="When this record was last modified.",
                        verbose_name="Modified",
                    ),
                ),
                ("date", geoluminate.db.fields.PartialDateField(verbose_name="date")),
                (
                    "type",
                    research_vocabs.fields.ConceptField(
                        verbose_name="type",
                        vocabulary=geoluminate.contrib.measurements.choices.MeasurementDates,
                    ),
                ),
            ],
            options={
                "verbose_name": "date",
                "verbose_name_plural": "dates",
                "abstract": False,
                "default_related_name": "dates",
            },
            bases=(meta.models.ModelMeta, models.Model),
        ),
        migrations.CreateModel(
            name="Description",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="When this record was created.",
                        verbose_name="Created",
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="When this record was last modified.",
                        verbose_name="Modified",
                    ),
                ),
                ("text", django_bleach.models.BleachField()),
                (
                    "type",
                    research_vocabs.fields.ConceptField(
                        verbose_name="type",
                        vocabulary=geoluminate.contrib.measurements.choices.MeasurementDescriptions,
                    ),
                ),
            ],
            options={
                "verbose_name": "description",
                "verbose_name_plural": "descriptions",
                "abstract": False,
                "default_related_name": "descriptions",
            },
            bases=(meta.models.ModelMeta, models.Model),
        ),
        migrations.CreateModel(
            name="Contribution",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="When this record was created.",
                        verbose_name="Created",
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="When this record was last modified.",
                        verbose_name="Modified",
                    ),
                ),
                (
                    "store",
                    models.JSONField(
                        default=dict,
                        help_text="A JSON representation of the contributor profile at the time of publication",
                        verbose_name="contributor",
                    ),
                ),
                (
                    "permissions",
                    models.JSONField(
                        default=geoluminate.contrib.core.models.contributor_permissions_default,
                        help_text="A JSON representation of the contributor's permissions at the time of publication",
                        verbose_name="permissions",
                    ),
                ),
                (
                    "roles",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=research_vocabs.fields.ConceptField(
                            verbose_name="type",
                            vocabulary=geoluminate.contrib.measurements.choices.MeasurementRoles,
                        ),
                        help_text="Assigned roles for this contributor.",
                        size=None,
                        verbose_name="roles",
                    ),
                ),
                (
                    "contributor",
                    models.ForeignKey(
                        help_text="The person or organisation that contributed to the project or dataset.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(app_label)s_%(class)ss",
                        related_query_name="%(app_label)s_%(class)s",
                        to="contributors.contributor",
                        verbose_name="contributor",
                    ),
                ),
            ],
            options={
                "verbose_name": "contributor",
                "verbose_name_plural": "contributors",
                "abstract": False,
            },
            bases=(meta.models.ModelMeta, models.Model),
        ),
        migrations.CreateModel(
            name="Measurement",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="When this record was created.",
                        verbose_name="Created",
                    ),
                ),
                (
                    "modified",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="When this record was last modified.",
                        verbose_name="Modified",
                    ),
                ),
                (
                    "contributors",
                    models.ManyToManyField(
                        help_text="The contributors to this measurement.",
                        through="measurements.Contribution",
                        to="contributors.contributor",
                        verbose_name="contributors",
                    ),
                ),
                (
                    "polymorphic_ctype",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="polymorphic_%(app_label)s.%(class)s_set+",
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "verbose_name": "measurement",
                "verbose_name_plural": "measurements",
                "ordering": ["-modified"],
                "default_related_name": "measurements",
            },
            bases=(
                meta.models.ModelMeta,
                polymorphic.showfields.ShowFieldType,
                models.Model,
            ),
        ),
    ]