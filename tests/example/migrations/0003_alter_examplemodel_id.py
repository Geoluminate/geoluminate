# Generated by Django 4.2.11 on 2024-03-13 06:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("example", "0002_examplemodel_delete_testdata"),
    ]

    operations = [
        migrations.AlterField(
            model_name="examplemodel",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]