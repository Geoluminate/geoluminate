from formset.collection import FormCollection
from formset.fields import Activator
from formset.renderers import ButtonVariant
from formset.renderers.bootstrap import FormRenderer
from formset.widgets import Button

from ..models import Identifier
from .forms import ContributorForm, IdentifierForm

DEFAULT_SUBMIT_BUTTON = Activator(
    label="Submit",
    widget=Button(
        action="disable -> spinner -> submit -> okay(3000) !~ scrollToError ",
        button_variant=ButtonVariant.PRIMARY,
        icon_path="formset/icons/send.svg",
    ),
)

DEFAULT_RENDERER = FormRenderer(
    form_css_classes="row",
    field_css_classes={
        "*": "mb-3 col-9",
    },
)


class ProfileEditForm(FormCollection):
    contributor = ContributorForm()

    submit = DEFAULT_SUBMIT_BUTTON
    default_renderer = DEFAULT_RENDERER


class ProfileIdentifierForm(FormCollection):
    min_siblings = 0
    identifiers = IdentifierForm(
        scheme_choices=[c for c in Identifier.PERS_ID_TYPES.choices if c[0] != Identifier.PERS_ID_TYPES.ORCID]
    )
    default_renderer = DEFAULT_RENDERER
    related_field = "object"

    def retrieve_instance(self, data):
        if data := data.get("identifiers"):
            try:
                return self.instance.identifiers.get(scheme=data.get("scheme") or "")
            except (AttributeError, Identifier.DoesNotExist, ValueError):
                return Identifier(**data)

    # def construct_instance(self, instance=None):
    #     """
    #     Construct the main instance and all its related objects from the nested dictionary. This
    #     method may only be called after the current form collection has been validated, usually by
    #     calling `is_valid`.

    #     Forms and Collections which do not correspond to the model given by the starting instance,
    #     are responsible themselves to override this method in order to store the corresponding data
    #     inside their related models.
    #     """
    #     assert self.is_valid(), f"Can not construct instance with invalid collection {self.__class__} object"
    #     for valid_holders in self.valid_holders:
    #         # first, handle holders which are forms
    #         for name, holder in valid_holders.items():
    #             if not isinstance(holder, BaseModelForm):
    #                 continue
    #             if holder.marked_for_removal:
    #                 holder.instance.delete()
    #                 continue
    #             construct_instance(holder, holder.instance)
    #             holder.instance.save()
    #             holder.instance.contributor_set.add(instance)
    #             try:
    #                 holder.save()
    #             except (IntegrityError, ValueError) as error:
    #                 # some errors are caught only after attempting to save
    #                 holder._update_errors(error)

    #         # next, handle holders which are sub-collections
    #         for name, holder in valid_holders.items():
    #             if callable(getattr(holder, "construct_instance", None)):
    #                 holder.construct_instance(holder.instance)


class UserIdentifierForm(FormCollection):
    identifiers = ProfileIdentifierForm()
    submit = DEFAULT_SUBMIT_BUTTON
    default_renderer = FormRenderer(
        form_css_classes="row mb-2",
        label_css_classes="visually-hidden",
        field_css_classes={
            "scheme": "col-3",
            "identifier": "col-6",
        },
    )
