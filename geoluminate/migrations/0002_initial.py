# Generated by Django 4.2.11 on 2024-03-11 15:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import licensing.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('geoluminate', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('licensing', '0001_initial'),
        ('literature', '0002_alter_literature_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='approved_by',
            field=models.ForeignKey(blank=True, help_text='The user who approved this dataset.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_%(class)ss', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dataset',
            name='license',
            field=licensing.fields.LicenseField(blank=True, help_text='the license under which this content is published', null=True, on_delete=django.db.models.deletion.PROTECT, to='licensing.license', verbose_name='license'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='project',
            field=models.ForeignKey(blank=True, help_text='The project that this dataset belongs to.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='datasets', to='geoluminate.project', verbose_name='project'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='reference',
            field=models.OneToOneField(blank=True, help_text='The data publication to which this dataset belongs. If the dataset has not been formally published, leave this field blank.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='literature.literature'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='related_literature',
            field=models.ManyToManyField(blank=True, help_text='Any literature that is related to this dataset.', related_name='related_datasets', related_query_name='related_dataset', to='literature.literature'),
        ),
    ]