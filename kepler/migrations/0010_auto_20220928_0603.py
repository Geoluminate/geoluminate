# Generated by Django 3.2.15 on 2022-09-27 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kepler', '0009_rename_fallback_lang_configuration_lang'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='configuration',
            name='default_config',
        ),
        migrations.AddField(
            model_name='configuration',
            name='mapState',
            field=models.JSONField(default=dict, help_text='Configuration object for the map state', verbose_name='map state configuration'),
        ),
        migrations.AddField(
            model_name='configuration',
            name='mapStyle',
            field=models.JSONField(default=dict, help_text='Configuration object for the map style', verbose_name='map style configuration'),
        ),
        migrations.AddField(
            model_name='configuration',
            name='visState',
            field=models.JSONField(default=dict, help_text='Configuration object for the visual state', verbose_name='map style configuration'),
        ),
    ]