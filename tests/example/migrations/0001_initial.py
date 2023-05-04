# Generated by Django 4.2 on 2023-05-04 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("geoluminate", "0003_geoluminatesite_alter_geoluminate_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="TestData",
            fields=[
                (
                    "geoluminate_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="geoluminate.geoluminate",
                    ),
                ),
                (
                    "some_field",
                    models.CharField(
                        blank=True, help_text="Some Field", max_length=255, null=True, verbose_name="Some Field"
                    ),
                ),
            ],
            options={
                "verbose_name": "Test Data",
                "verbose_name_plural": "Test Data",
                "permissions": [("geoluminate_database_admin", "Can access the geoluminate database admin")],
            },
            bases=("geoluminate.geoluminate",),
        ),
    ]