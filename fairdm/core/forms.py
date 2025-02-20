from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from polymorphic_treebeard.forms import movepolynodeform_factory

from fairdm.contrib.contributors.models import Contribution, Person
from fairdm.forms import ImageCroppingWidget

from .models import Dataset, Project, Sample


class BaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.user = None
        if self.request:
            self.user = self.request.user

        super().__init__(*args, **kwargs)


class ProjectForm(BaseForm):
    image = forms.ImageField(
        widget=ImageCroppingWidget(
            width=1200,
            height=int(1200 * 9 / 16),
            empty_text=_("Select cover image"),
            config={
                "enableOrientation": True,
            },
            result={
                "format": "jpeg",
            },
        ),
        required=False,
        label=False,
    )
    name = forms.CharField(label=_("Project name"), help_text=_("Give your new project a name"))
    status = forms.ChoiceField(
        label=_("Current status"),
        choices=Project.STATUS_CHOICES.choices,
        help_text=_("In which stage of it's lifecycle is this project?"),
    )

    class Meta:
        model = Project
        fields = [
            "image",
            "name",
            "status",
        ]


class SelectizeWidget(forms.SelectMultiple):
    def __init__(self, *args, **kwargs):
        # You can pass any additional arguments here like the 'drag_drop' option, etc.
        self.selectize_options = kwargs.pop("selectize_options", {})
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        # First, render the standard SelectMultiple widget
        output = super().render(name, value, attrs, renderer)

        # Add the Selectize initialization script to the output
        selectize_script = f"""
        <script type="text/javascript">
            $(document).ready(function() {{
                $('#{attrs["id"]}').selectize({{
                    {self._generate_selectize_options()}
                }});
            }});
        </script>
        """

        return mark_safe(output + selectize_script)

    def _generate_selectize_options(self):
        # Convert the selectize_options dictionary into JavaScript-friendly format
        options = ["'plugins': ['remove_button', 'drag_drop']"]
        # for key, value in self.selectize_options.items():
        #     if isinstance(value, str):
        #         options.append(f"'{key}': '{value}'")
        #     else:
        #         options.append(f"'{key}': {value}")
        return ", ".join(options)


class CreatorsFormField(forms.ModelMultipleChoiceField):
    widget = SelectizeWidget

    def clean(self, value):
        value = super().clean(value)
        removed = [c for c in self.initial if c not in value]

        for c in removed:
            c.roles.remove("Creator")
            c.save()

        for i, c in enumerate(value):
            if c not in self.initial:
                c.add_roles(["Creator"])
            # set order using django-ordered-model api
            c.to(i)
            c.save()

        return value

    def _check_values(self, value):
        """
        Given a list of possible PK values, return a QuerySet of the
        corresponding objects. Raise a ValidationError if a given value is
        invalid (not a valid PK, not in the queryset, etc.)
        """
        key = self.to_field_name or "pk"
        qs = super()._check_values(value)
        result = []
        for pk in value:
            result.append(qs.get(**{key: pk}))
        return result


class DatasetForm(BaseForm):
    """Generic form used by DataestCRUDView for creating and updating regular fields on a Dataset."""

    # image = forms.ImageField(
    #     widget=ImageCroppingWidget(
    #         width=1200,
    #         height=int(1200 * 9 / 16),
    #         config={
    #             "enableOrientation": True,
    #         },
    #         result={
    #             "format": "jpeg",
    #         },
    #     ),
    #     required=False,
    #     label=False,
    # )

    contributors = CreatorsFormField(
        label=_("Creators"),
        queryset=Contribution.objects.all(),
        required=False,
        help_text=_("The following contributors will be credited when publishing the dataset."),
    )

    class Meta:
        model = Dataset
        fields = ["image", "project", "name", "license", "visibility"]

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            content_type = ContentType.objects.get_for_model(Person)
            self.fields["contributors"].queryset = self.instance.contributors.filter(
                contributor__polymorphic_ctype=content_type.id
            )
            self.fields["contributors"].initial = [
                c for c in self.fields["contributors"].queryset if "Creator" in c.roles
            ]
        self.request = request
        if self.request:
            self.fields["project"].queryset = self.request.user.projects.all()
        # self.fields["project"].widget = forms.HiddenInput()
        # self.fields["visibility"].initial = Dataset.VISIBILITY_PRIVATE

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance


SampleFormMixin = movepolynodeform_factory(
    Sample, exclude=["created", "modified", "keywords", "options", "path", "numchild"]
)


class SampleForm(forms.ModelForm):
    # _position = forms.ChoiceField(required=True, label=_("Position"), widget=forms.HiddenInput)
    # _ref_node_id = forms.ChoiceField(
    #     label=_("Child of"),
    #     help_text=_("The sample from which this sample was derived, if any."),
    #     required=False,
    # )

    class Meta:
        model = Sample
        exclude = ["created", "modified", "keywords", "depth", "options", "path", "numchild", "tags"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        # if self.request:
        # self.fields["dataset"].queryset = self.request.user.datasets.all()
        # self.fields["dataset"].initial = self.request.GET.get("dataset")

        self.helper = FormHelper()
        self.helper.form_tag = False
        # self.helper.layout = convert_to_crispy_layout(fieldsets)

    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     if commit:
    #         instance.save()
    #     return instance
