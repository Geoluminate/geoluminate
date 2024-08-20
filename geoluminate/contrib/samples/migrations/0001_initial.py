# Generated by Django 5.0.7 on 2024-08-19 12:57

import django.db.models.deletion
import django_bleach.models
import geoluminate.contrib.core.models
import geoluminate.contrib.samples.choices
import geoluminate.db.fields
import meta.models
import research_vocabs.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("contributors", "0001_initial"),
        ("datasets", "0002_initial"),
        ("gis", "0001_initial"),
    ]

    operations = [
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
                    "roles",
                    models.JSONField(
                        blank=True,
                        default=list,
                        help_text="Assigned roles for this contributor.",
                        null=True,
                        verbose_name="roles",
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
            name="Sample",
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
                ("path", models.CharField(max_length=255, unique=True)),
                ("depth", models.PositiveIntegerField()),
                ("numchild", models.PositiveIntegerField(default=0)),
                ("name", models.CharField(max_length=255, verbose_name="name")),
                (
                    "status",
                    research_vocabs.fields.ConceptField(
                        default="unknown",
                        max_length=8,
                        verbose_name="status",
                        vocabulary=geoluminate.contrib.samples.choices.SampleStatus,
                    ),
                ),
                (
                    "options",
                    models.JSONField(
                        blank=True,
                        help_text="Item options.",
                        null=True,
                        verbose_name="options",
                    ),
                ),
                (
                    "contributors",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The contributors to this sample.",
                        through="samples.Contribution",
                        to="contributors.contributor",
                        verbose_name="contributors",
                    ),
                ),
                (
                    "dataset",
                    models.ForeignKey(
                        help_text="The dataset for which this sample was collected.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="samples",
                        to="datasets.dataset",
                        verbose_name="dataset",
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        blank=True,
                        help_text="The location of the sample.",
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="samples",
                        to="gis.location",
                        verbose_name="location",
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
                "verbose_name": "Sample",
                "verbose_name_plural": "Samples",
                "ordering": ["created"],
                "default_related_name": "samples",
            },
            bases=(meta.models.ModelMeta, models.Model),
        ),
        migrations.AddField(
            model_name="contribution",
            name="object",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contributions",
                to="samples.sample",
                verbose_name="sample",
            ),
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
                        max_length=11,
                        verbose_name="type",
                        vocabulary=geoluminate.contrib.samples.choices.SampleDescriptions,
                    ),
                ),
                (
                    "object",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="samples.sample"
                    ),
                ),
            ],
            options={
                "verbose_name": "description",
                "verbose_name_plural": "descriptions",
                "abstract": False,
                "default_related_name": "descriptions",
                "unique_together": {("object", "type")},
            },
            bases=(meta.models.ModelMeta, models.Model),
        ),
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
                        max_length=16,
                        verbose_name="type",
                        vocabulary=geoluminate.contrib.samples.choices.SampleDates,
                    ),
                ),
                (
                    "object",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="samples.sample"
                    ),
                ),
            ],
            options={
                "verbose_name": "date",
                "verbose_name_plural": "dates",
                "abstract": False,
                "default_related_name": "dates",
                "unique_together": {("object", "type")},
            },
            bases=(meta.models.ModelMeta, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name="contribution",
            unique_together={("object", "contributor")},
        ),
    ]
