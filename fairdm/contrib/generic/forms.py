from crispy_forms.helper import FormHelper
from django import forms
from django.forms import BaseFormSet, BaseInlineFormSet
from django.utils.module_loading import import_string
from django_select2.forms import Select2MultipleWidget, Select2TagWidget
from extra_views import InlineFormSetFactory
from research_vocabs.forms import MultiConceptField, TaggableConceptFormMixin

from fairdm.core.models import Dataset
from fairdm.core.models.sample import SampleDescription
from fairdm.forms import PartialDateField
from fairdm.utils.utils import get_setting

# from .models import Date, Description


class TagWidget(Select2TagWidget):
    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        return ",".join(value) if value else None


class FormsetMixin:
    def __init__(self, *args, **kwargs):
        self.vocabulary = self.model.VOCABULARY
        kwargs["initial"] = self.get_initial(kwargs.pop("queryset"))
        super().__init__(*args, **kwargs)
        self.can_delete = False
        self.can_delete_extra = False
        self.helper = FormHelper()
        self.helper.form_method = "post"

    def get_initial(self, qs):
        existing_choices = qs.values_list("type", flat=True)
        missing_choices = [c for c in self.vocabulary.values if c not in existing_choices]
        initial = [{"type": choice} for choice in missing_choices]
        self.extra = len(missing_choices)
        return initial

    def __iter__(self):
        # Yield forms in the order defined in the vocabulary. Without this, forms are displayed first by those that
        # are already in the database, then by the order they were added to the formset (which can be confusing.).
        form_map = {form.initial.get("type", form.instance.type): form for form in self.forms}
        for type_value in self.vocabulary.values:
            if type_value in form_map:
                yield form_map[type_value]

    def _construct_form(self, i, **kwargs):
        # ensures that the vocabulary is passed to the form for rendering and labelling
        kwargs["vocab"] = self.vocabulary
        return super()._construct_form(i, **kwargs)

    def save(self, commit=True):
        self._deleted_form_indexes = []
        self.can_delete = True
        for i, form in enumerate(self.forms):
            # if the form has no date value, mark it for deletion. This is prettier and IMO more user-friendly than
            # the default formset behavior of providing flags for deletion.
            if not form.cleaned_data.get("value") and i not in self._deleted_form_indexes:
                self._deleted_form_indexes.append(i)

        return super().save(commit=commit)


class CoreFormset(FormsetMixin, BaseFormSet):
    pass


class CoreInlineFormset(FormsetMixin, BaseInlineFormSet):
    """A base formset for use with the generic models (Description, Date, Identifier) related to the core data models.

    The constructor to this formset requires a `content_object` to be passed in, which is either a Project, Dataset, Sample,
    or Measurement instance. It also requires a vocabulary to be passed in, which contains accepted choices for the given
    content_type.

    The final formset is rendered as individual forms for each choice in the vocabulary, in the order defined by the vocabulary.
    """

    def __init__(self, *args, instance=None, **kwargs):
        kwargs["queryset"] = self.model._default_manager.filter(**{self.fk.name: instance})
        super().__init__(*args, instance=instance, **kwargs)


class TypeVocabularyFormMixin(forms.ModelForm):
    """
    A mixin for Django ModelForms that integrates vocabulary-based concepts
    for a 'type' field and dynamically adjusts the 'value' field labels and help texts.

    Args:
        vocab (Vocabulary): A vocabulary object containing concepts
                            mapped to type values.
    """

    def __init__(self, *args, **kwargs):
        vocabulary = kwargs.pop("vocab", [])
        super().__init__(*args, **kwargs)
        self.fields["type"].widget = forms.HiddenInput()

        if type_value := self.initial.get("type") or self.instance.type:
            concept = vocabulary.get_concept(type_value)
            self.fields["value"].label = concept.label()
            self.fields["value"].help_text = concept.definition()


class DateForm(TypeVocabularyFormMixin):
    """
    A Django ModelForm for handling date-related input using a partial date field.

    Attributes:
        value (PartialDateField): A custom date input field that allows partial dates.
            - Required: False (optional field).
            - Label and help text: Dynamically set by TypeVocabularyFormMixin.

    Behavior:
        - The "type" field is inherited from TypeVocabularyFormMixin and is hidden.
        - The "value" field allows users to input partial dates (e.g., only a year or year-month).
        - The form dynamically sets the label and help text of "value" based on a vocabulary concept.
    """

    value = PartialDateField(required=False)

    class Meta:
        fields = ["value", "type"]


class KeywordForm(TaggableConceptFormMixin, forms.ModelForm):
    tags = forms.CharField(
        label="Free keywords",
        help_text="Additional keywords that are not available in the listed controlled vocabularies.",
        widget=TagWidget,
        required=False,
    )

    class Meta:
        model = Dataset
        fields = ["tags"]
        taggable_fields = []
        # The field name to add the controlled voacbulary keywords to
        taggable_field_name = "keywords"

    def __init__(self, *args, **kwargs):
        self.attach_vocabularies()
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = "keyword-form"

    def attach_vocabularies(self):
        vocabularies = get_setting("DATASET", "keyword_vocabularies")
        for vocab_str in vocabularies:
            vocab_class = import_string(vocab_str)
            self.Meta.taggable_fields.append(vocab_class.__name__)
            self.base_fields[vocab_class.__name__] = MultiConceptField(
                vocabulary=vocab_class, widget=Select2MultipleWidget, required=False
            )
        x = 8
        # self._meta.fields = fields + self._meta.fields


# Inlines: To be used with extra_views.UpdateWithInlinesView
class BaseInlineFactory(InlineFormSetFactory):
    factory_kwargs = {
        "can_delete": False,
        "can_delete_extra": False,
    }


class DescriptionForm(TypeVocabularyFormMixin):
    """
    A Django ModelForm that extends TypeVocabularyFormMixin to handle text-based descriptions.

    Attributes:
        value (CharField): A text area input for entering a description.
            - Required: False (optional field).
            - Label: False (label is dynamically set by the mixin).
            - Widget: A Textarea with Alpine.js-based auto-resizing functionality.

    Behavior:
        - The "type" field is inherited from TypeVocabularyFormMixin and is hidden.
        - The "value" field automatically resizes based on input using Alpine.js.
        - The form dynamically sets the label and help text of "value" based on a vocabulary concept.
    """

    value = forms.CharField(
        required=False,
        label=False,
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "x-data": "{}",
                "x-ref": "textarea",
                "x-init": "$nextTick(() => $refs.textarea.style.height = $refs.textarea.scrollHeight + 'px')",
                "x-on:input": "$refs.textarea.style.height = 'auto'; $refs.textarea.style.height = $refs.textarea.scrollHeight + 'px';",
                "style": "overflow: hidden; resize: none;",
                "class": "w-100 form-control",
            }
        ),
    )

    class Meta:
        model = SampleDescription
        fields = ["value", "type"]


class DescriptionInline(InlineFormSetFactory):
    form_class = DescriptionForm
    formset_class = CoreInlineFormset

    def __init__(self, parent_model, request, instance, view_kwargs=None, view=None):
        self.model = parent_model._meta.get_field("descriptions").related_model
        super().__init__(parent_model, request, instance, view_kwargs=None, view=None)

    def construct_formset(self):
        formset = super().construct_formset()
        formset.helper.form_id = "description-form-collection"
        return formset
