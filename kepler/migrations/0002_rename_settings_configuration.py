# Generated by Django 3.2.15 on 2022-09-27 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kepler', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Settings',
            new_name='Configuration',
        ),
    ]
