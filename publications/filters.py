from .models import Publication
import django_filters as df
from crispy_forms.helper import FormHelper
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.layout import Layout, Submit

class PublicationFilter(df.FilterSet):

    author = df.CharFilter(label='Author', lookup_expr='icontains')
    title = df.CharFilter(label='Title', lookup_expr='icontains')

    helper = FormHelper()
    helper.form_method = 'GET'
    helper.form_id = 'publicationFilterForm'
    helper.layout = Layout(
                FloatingField('author'),
                FloatingField('title'),
                # Submit('Search', 'submit')
    )

    class Meta:
        # model = Publication
        fields = ['author','title',]

      