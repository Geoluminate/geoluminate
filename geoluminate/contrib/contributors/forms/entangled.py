from django import forms


class MultiTagForm(forms.Form):
    pass
    # interests = ControlledMultipleTagField(
    #     choices=[
    #         (i, _(i))
    #         for i in [
    #             "GIS",
    #             "Remote Sensing",
    #             "Geospatial Data Science",
    #             "Geospatial Data Engineering",
    #         ]
    #     ],
    #     widget=SelectizeMultiple(),
    # )

    # status = ControlledMultipleTagField(
    #     choices=[
    #         (i, _(i))
    #         for i in [
    #             "Open to collaboration",
    #             "Looking for collaborators",
    #             "Busy",
    #             "Looking for work",
    #         ]
    #     ],
    #     widget=SelectizeMultiple(),
    # )


# class ContributorPermissions(EntangledModelForm):
#     """A form that can be used to set permissions for a contributor on a project."""

#     edit = forms.BooleanField(
#         label=_("Can Edit"),
#         help_text=_("Can edit this project."),
#         required=False,
#     )

#     class Meta:
#         model = Contribution
#         entangled_fields = {
#             "permissions": [
#                 "edit",
#             ]
#         }


# class ProfileOptions(EntangledModelForm):
#     can_contact = forms.BooleanField(
#         label=_("Can Contact"),
#         help_text=_("Allow other users to contact you through this site."),
#         required=False,
#     )

#     class Meta:
#         model = Contributor
#         entangled_fields = {"options": ["can_contact"]}
