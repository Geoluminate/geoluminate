# Generated by Django 5.0.6 on 2024-07-22 09:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("datasets", "0001_initial"),
        ("literature", "0001_initial"),
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="dataset",
            name="project",
            field=models.ForeignKey(
                blank=True,
                help_text="The project that this dataset belongs to.",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="datasets",
                to="projects.project",
                verbose_name="project",
            ),
        ),
        migrations.AddField(
            model_name="dataset",
            name="reference",
            field=models.OneToOneField(
                blank=True,
                help_text="The data publication to which this dataset belongs. If the dataset has not been formally published, leave this field blank.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="literature.literatureitem",
            ),
        ),
        migrations.AddField(
            model_name="dataset",
            name="related_literature",
            field=models.ManyToManyField(
                blank=True,
                help_text="Any literature that is related to this dataset.",
                related_name="related_datasets",
                related_query_name="related_dataset",
                to="literature.literatureitem",
            ),
        ),
        migrations.AddField(
            model_name="contribution",
            name="object",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contributions",
                to="datasets.dataset",
                verbose_name="dataset",
            ),
        ),
        migrations.AddField(
            model_name="date",
            name="object",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="datasets.dataset"
            ),
        ),
        migrations.AddField(
            model_name="description",
            name="object",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="datasets.dataset"
            ),
        ),
        migrations.AddField(
            model_name="identifier",
            name="object",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="datasets.dataset"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="contribution",
            unique_together={("object", "contributor")},
        ),
        migrations.AlterUniqueTogether(
            name="date",
            unique_together={("object", "type")},
        ),
        migrations.AlterUniqueTogether(
            name="description",
            unique_together={("object", "type")},
        ),
        migrations.AlterUniqueTogether(
            name="identifier",
            unique_together={("scheme", "identifier")},
        ),
    ]
