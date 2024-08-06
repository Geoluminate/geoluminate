from django import forms
from django.utils.translation import gettext_lazy as _
from entangled.forms import EntangledModelForm, EntangledModelFormMixin

# AutoNumberInput,
# ButtonGroup,
# IconGroup,
# TagTypeFormField,
from .models import Configuration


class DatabaseConfigForm(EntangledModelFormMixin):
    name = forms.CharField(
        label=_("Database Name"),
        required=False,
    )
    short_name = forms.CharField(
        label=_("Database Short Name"),
        required=False,
    )

    class Meta:
        model = Configuration
        entangled_fields = {
            "database": [
                "name",
                "short_name",
                # "license",
            ]
        }


class AuthorityConfigForm(EntangledModelFormMixin):
    name = forms.CharField(
        label=_("Authority Name"),
        required=False,
    )
    short_name = forms.CharField(
        label=_("Authority Short Name"),
        required=False,
    )
    url = forms.URLField(
        label=_("Authority URL"),
        required=False,
    )
    contact = forms.EmailField(
        label=_("Contact Email"),
        required=False,
    )

    class Meta:
        model = Configuration
        entangled_fields = {
            "authority": [
                "name",
                "short_name",
                "url",
                "contact",
            ]
        }


class SiteConfigForm(EntangledModelForm):
    name = forms.CharField(
        label=_("Database Name"),
        required=False,
    )
    short_name = forms.CharField(
        label=_("Database Short Name"),
        required=False,
    )

    class Meta:
        model = Configuration
        entangled_fields = {
            "database": [
                "name",
                "short_name",
            ]
        }
        untangled_fields = (
            "logo",
            "icon",
            # "theme",
        )

    # theme = AttributesFormField(
    #     label=_("Bootstrap 5 Variables"),
    #     help_text=_(
    #         "Key-value pairs of Bootstrap 5 theme variables used to customize the appearance of the site. Omit the leading $ symbol E.g. primary = blue"
    #     ),
    #     required=False,
    # )
