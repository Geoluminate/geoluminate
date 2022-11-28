from django.http import JsonResponse
from django_select2.views import AutoResponseView
from django.utils.module_loading import import_string
from django.conf import settings
from django.views.generic import DetailView, TemplateView
from geoluminate.utils import DATABASE
from .filters import MapFilter
from meta.views import Meta
from geoluminate.core.mixins import FieldSetMixin
from datatables.views import DatatablesReadOnlyView
from database.models import HeatFlow
from django.apps import apps
import datatables
# from django.contrib.admindocs import views
from django.apps import apps
from django.conf import settings
# from django.contrib.admindocs.utils import parse_docstring
from django.db import models
from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from django.forms import ModelChoiceField


@datatables.register
class DatabaseTableView(DatatablesReadOnlyView):
    model = HeatFlow
    read_only = True
    search_fields = ('name', )
    ordering_fields = ['-geographic', ]
    exclude_fields = [
        'geom',
        'expl',
        'intervals',
        'references',
        'q_acq',
        'q_comment',
        'continent',
        'last_modified',
        'conductivity_logs',
        'temperature_logs',
        'site_ptr',
        'date_added',
        '__str__',
    ]
    include_str = False
    invisible_fields = ['id', ]
    datatables = dict(
        scrollY='100vh',
        deferRender=True,
        scroller=True,
    )


class GlossaryView(TemplateView):
    template_name = 'geoluminate/glossary.html'
    exclude_fields = ['site_ptr', 'date_added', 'historic_id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            models=[self.get_model_context(x)
                    for x in getattr(settings, "GEOLUMINATE_GLOSSARY")],
            exclude=self.exclude_fields,
        )
        return context

    def get_model_context(self, model_name, **kwargs):
        model = apps.get_model(model_name)
        opts = model._meta

        title, body, metadata = utils.parse_docstring(model.__doc__)
        title = title and utils.parse_rst(
            title, 'model', _('model:') + model_name)
        body = body and utils.parse_rst(
            body, 'model', _('model:') + model_name)

        # Gather fields/field descriptions.
        fields = []
        for field in opts.fields:
            if isinstance(field, models.ForeignKey):
                data_type = field.remote_field.model.__name__
            else:
                data_type = views.get_readable_field_data_type(field)
            verbose = field.verbose_name
            choices = None
            if field.choices:
                choices = [x[0] for x in field.get_choices()]
            if data_type == 'Choice':
                choices = field.get_choices_queryset()

            fields.append({
                'name': field.name,
                'data_type': data_type,
                'verbose': verbose or '',
                'help_text': field.help_text,
                'choices': choices or None,
            })

        # Gather many-to-many fields.
        for field in opts.many_to_many:
            choices = None
            if field.choices:
                choices = [x[0] for x in field.get_choices()]
            if data_type == 'Choice':
                choices = field.get_choices_queryset()
            fields.append({
                'name': field.name,
                'data_type': field.remote_field.model.__name__,
                'verbose': field.verbose_name,
                'help_text': field.help_text,
                'choices': choices or None,
            })

        # Gather related objects
        # for rel in opts.related_objects:
        #     verbose = _("related `%(app_label)s.%(object_name)s` objects") % {
        #         'app_label': rel.related_model._meta.app_label,
        #         'object_name': rel.related_model._meta.object_name,
        #     }
        #     accessor = rel.get_accessor_name()
        #     fields.append({
        #         'name': accessor,
        #         # 'data_type': field.remote_field.model.__name__,
        #         'data_type': None,
        #         'verbose': None,
        #         # 'help_text': field.help_text,
        #         'choices': None,
        #     })
        #     # accessor = rel.get_accessor_name()

        return super().get_context_data(**{
            **kwargs,
            'name': opts.verbose_name,
            'summary': title,
            'description': body,
            'fields': fields,
        })


class WorldMap(TemplateView):
    template_name = 'mapping/application.html'
    # template_name = 'kepler/application.html'
    filter = MapFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(dict(
            filter=self.filter(),
            download_form=self.download_form(),
            # settings=MapSettingsForm(),
        ))

        context['meta'] = Meta(
            title='World Map | World Heat Flow Database',
            description='Interactive search and download of all data within the World Heat Flow Database database. The fastest wasy to find published and unpublished thermal data related to studies of the Earth.',
            keywords=[
                'heat flow',
                'thermal gradient',
                'thermal conductivity',
                'temperature',
                'heat production',
                'World Heat Flow Database',
                'data',
                'access']
        )
        return context


class SiteView(FieldSetMixin, DetailView):
    template_name = "main/site_details.html"
    model = DATABASE
    fieldset = [
        # (None,
        #     {'fields': [
        #         'name',
        #         ('lat','lng'),
        #         'elevation',
        #         ]}),
        ("Heat Flow",
            {'fields': [
                'q',
                'q_unc',
                'method',
                'env',
                'expl',
                'wat_temp',
                'q_comment',
            ]}),
        ('Geographic',
            {'fields': [
                'country',
                'political',
                'continent',
                'ocean',
                'province',
                'plate',
            ]}),
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta'] = self.get_object().as_meta(self.request)
        context['fieldset'] = self.get_fieldset()
        return context

    def get_queryset(self):
        return (super().get_queryset()
                .prefetch_related('references'))


class ModelFieldSelect2View(AutoResponseView):
    """This is a subclass of the `django_select2.views.AutoResponseView`
    that will return distinct values of a model field using the values
    themselves as both the `id` and the `text` fields in the JSONResponse.

    E.g.
        'results': [
                {'text': "foo", 'id': "foo"}
        ],
    """

    def get(self, request, *args, **kwargs):
        self.widget = self.get_widget_or_404()
        self.term = kwargs.get("term", request.GET.get("term", ""))
        field = self.widget.search_fields[0].split('__')[0]
        self.object_list = (
            self.get_queryset()
            .values_list(field, flat=True)
            .order_by(field)
            .distinct())
        context = self.get_context_data()
        return JsonResponse(
            {
                "results": [
                    {"text": obj, "id": obj}
                    for obj in context["object_list"]
                ],
                "more": context["page_obj"].has_next(),
            },
            encoder=import_string(settings.SELECT2_JSON_ENCODER)
        )
