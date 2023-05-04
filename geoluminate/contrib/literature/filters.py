import django_filters as df
from crispy_bootstrap5.bootstrap5 import Field
from crispy_forms.helper import FormHelper
from django_select2.forms import ModelSelect2MultipleWidget

# from geoluminate.utils.generic import get_choices, choices_from_qs
from literature.models import Author, Literature

from geoluminate.utils.select2.filters import Select2MultipleChoiceFilter


class Small(Field):
    def __init__(self, *args, **kwargs):
        kwargs.update(css_class="form-control form-control-sm")
        super().__init__(*args, **kwargs)


class PublicationFilter(df.FilterSet):
    DOI = df.CharFilter(label="DOI", lookup_expr="exact")
    author = df.ModelMultipleChoiceFilter(
        label="Author/s",
        queryset=Author.objects.all(),
        widget=ModelSelect2MultipleWidget(
            model=Author,
            search_fields=[
                "family__icontains",
                "ORCID__icontains",
            ],
        ),
    )
    title = df.CharFilter(label="Title", lookup_expr="icontains")

    container_title = Select2MultipleChoiceFilter(Literature, "container_title", select2_lookup_expr="istartswith")
    type = Select2MultipleChoiceFilter(Literature, "type")
    # subject = df.ModelMultipleChoiceFilter(
    #     label="Subject/s",
    #     queryset=Subject.objects.all(),
    #     widget=ModelSelect2MultipleWidget(
    #         model=Subject,
    #         search_fields=[
    #             "name__icontains",
    #         ],
    #     ),
    # )

    # language = df.ChoiceFilter(
    #     choices=get_choices(Literature, 'language'),
    #     label='Language', lookup_expr='exact')

    class Meta:
        model = Literature
        fields = [
            # 'DOI',
            "type",
            "title",
            "author",
            "container_title",
            "language",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.filters['type'].choices = choices_from_qs(self.qs, 'type')
        form = self.form
        form.helper = FormHelper()
        form.helper.form_tag = False
        form.helper.include_media = False
        form.helper.form_method = "GET"
        form.helper.form_id = "publicationFilterForm"
        # form.helper.layout = Layout(
        #     Field('DOI'),
        #     Field('author'),
        #     Field('title'),
        #     Field('type'),
        #     Field('container_title'),
        #     Field('language'),
        # )
