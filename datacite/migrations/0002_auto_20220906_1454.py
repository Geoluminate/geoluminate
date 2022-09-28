# Generated by Django 3.2.15 on 2022-09-06 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datacite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publisher', models.CharField(help_text='Name of the publisher. This value will be sent with all forms submitted to Datacite via this application.', max_length=256, verbose_name='Publisher')),
                ('resourceTypeGeneral', models.CharField(max_length=256)),
                ('show_lang_fields', models.BooleanField(default=True)),
                ('schema', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datacite.schema')),
                ('subjects', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='datacite.subject')),
            ],
            options={
                'verbose_name': 'Configuration',
                'verbose_name_plural': 'Configuration',
            },
        ),
        migrations.DeleteModel(
            name='DataCiteOptions',
        ),
    ]
