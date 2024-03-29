# Generated by Django 4.2.11 on 2024-03-27 13:20

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Configuration",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        default="", max_length=255, verbose_name="Site Name"
                    ),
                ),
                (
                    "logo",
                    models.ImageField(
                        blank=True, null=True, upload_to="", verbose_name="Logo"
                    ),
                ),
                (
                    "icon",
                    models.ImageField(
                        blank=True, null=True, upload_to="", verbose_name="Icon"
                    ),
                ),
                ("database", models.JSONField(default=dict, verbose_name="database")),
                ("authority", models.JSONField(default=dict, verbose_name="authority")),
                ("theme", models.JSONField(default=dict, verbose_name="theme")),
            ],
            options={
                "verbose_name": "Site Configuration",
            },
        ),
    ]
