# from django import forms
# from django.utils.translation import gettext_lazy as _
# from entangled.forms import EntangledModelForm, EntangledModelFormMixin

# # AutoNumberInput,
# # ButtonGroup,
# # IconGroup,
# # TagTypeFormField,
# from .models import Configuration


# class DatabaseConfigForm(EntangledModelFormMixin):
#     db_name = forms.CharField(max_length=255, label="Name")
#     db_short_name = forms.CharField(max_length=100, label="Short Name")
#     db_description = forms.CharField(
#         label=_("Description"),
#         required=True,
#         widget=forms.Textarea,
#     )

#     class Meta:
#         model = Configuration
#         # entangled_fields = {
#         #     "database": ["db_name", "db_short_name", "db_description"],
#         # }
#         retangled_fields = {
#             "db_name": "name",
#             "db_short_name": "short_name",
#         }


# class AuthorityConfigForm(EntangledModelFormMixin):
#     name = forms.CharField(
#         label=_("Authority Name"),
#         required=False,
#     )
#     short_name = forms.CharField(
#         label=_("Authority Short Name"),
#         required=False,
#     )
#     url = forms.URLField(
#         label=_("Authority URL"),
#         required=False,
#     )
#     contact = forms.EmailField(
#         label=_("Contact Email"),
#         required=False,
#     )

#     class Meta:
#         model = Configuration
#         entangled_fields = {
#             "authority": [
#                 "name",
#                 "short_name",
#                 "url",
#                 "contact",
#             ]
#         }


# class ConfigurationForm(DatabaseConfigForm, EntangledModelForm):
#     class Meta:
#         model = Configuration
#         untangled_fields = (
#             "logo",
#             "icon",
#             "theme",
#         )
#         # entangled_fields = {
#         #     "database": ["db_name", "db_short_name"],
#         #     "authority": ["auth_name", "auth_url", "auth_contact", "auth_description"],
#         # }
#         retangled_fields = {
#             "db_name": "name",
#             "db_short_name": "short_name",
#             "db_description": "description",
#             "auth_name": "name",
#             "auth_url": "url",
#             "auth_description": "description",
#             "auth_contact": "contact",
#         }

#     # Fields for the `authority` JSON field
#     auth_name = forms.CharField(max_length=255, label="Name")
#     auth_url = forms.URLField(label="Website")
#     auth_description = forms.CharField(
#         label="Description",
#         widget=forms.Textarea,
#     )
#     auth_contact = forms.EmailField(label="Contact Email")
