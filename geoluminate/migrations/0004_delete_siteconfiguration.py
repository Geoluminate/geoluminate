# Generated by Django 4.2.11 on 2024-03-22 22:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("geoluminate", "0003_siteconfiguration"),
    ]

    operations = [
        migrations.DeleteModel(
            name="SiteConfiguration",
        ),
    ]