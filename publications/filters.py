from .models import Publication
import django_filters as df
from crispy_forms.helper import FormHelper
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.layout import Layout
from core.utils import get_choices

class PublicationFilter(df.FilterSet):
    DOI = df.CharFilter(label='DOI', lookup_expr='exact')
    author = df.CharFilter(label='Author', lookup_expr='icontains')
    title = df.CharFilter(label='Title', lookup_expr='icontains')
    type = df.ChoiceFilter(
        choices=get_choices(Publication, 'type'),
        label='Type', lookup_expr='exact')
    container_title = df.ChoiceFilter(
        choices=get_choices(Publication, 'container_title'),
        label='Container', lookup_expr='exact')
    language = df.ChoiceFilter(
        choices=get_choices(Publication, 'language'),
        label='Language', lookup_expr='exact')
    # keywords = df.ModelMultipleChoiceFilter(queryset=,label='Keywords')

    class Meta:
        model = Publication
        fields = ['author','title',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        self.helper.form_id = 'publicationFilterForm'
        self.helper.layout = Layout(
                    FloatingField('DOI'),
                    FloatingField('author'),
                    FloatingField('title'),
                    FloatingField('type'),
                    FloatingField('container_title'),
                    FloatingField('language'),
        )