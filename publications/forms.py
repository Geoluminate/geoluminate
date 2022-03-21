from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Div, Row, Column, Field, HTML
from .models import Publication
from crispy_bootstrap5.bootstrap5 import FloatingField
from django.forms.models import formset_factory
from django.utils.translation import gettext_lazy as _
from .fields import ListConcatField, CrossRefAuthorField, DatePartsField
from django.forms import Textarea

class UploadForm(forms.Form):
    file = forms.FileField(label='Select a .bib file', required=True)

class PublicationForm(forms.ModelForm):

    class Meta:
        # model = Publication
        fields = '__all__'
        field_classes = {
            'title': ListConcatField,
            'container_title': ListConcatField,
            'author': CrossRefAuthorField,
            'published': DatePartsField,
        }


class PublicationForm2(forms.ModelForm):

    class Meta:
        model = Publication
        fields = ['title',]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = 'GET'
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
                Field('author',placeholder='Author', css_class='mb-2'),
                Field('title', placeholder='Title', css_class='mb-2'),
            ButtonHolder(
                Submit('submit', 'search', css_class='button mt-2')
            )
        )


class CrossRefForm(forms.ModelForm):

    class Meta:
        model = Publication
        fields = ['DOI']
        widgets = {
            'DOI': Textarea(attrs={'cols': 80, 'rows': 20}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_id = 'createPublicationForm'
        self.helper.form_action = ''
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
                HTML(f"<p>{_('Enter a DOI to retrieve a published research article.')}</p>"),
                FloatingField('DOI', placeholder='DOI'),
                Submit('submit','Create')
            )


class DOIForm(forms.ModelForm):

    class Meta:
        model = Publication
        fields = ['DOI']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_id = 'createPublicationForm'
        self.helper.form_action = ''
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
                HTML(f"<p>{_('Enter a DOI to retrieve a published research article.')}</p>"),
                FloatingField('DOI', placeholder='DOI'),
                Field('bibtex',type='hidden'),
            )
            

