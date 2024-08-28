# SettingsMenu.add_items(
#     SubMenu(
#         _("profile"),
#         weight=1,
#         children=[
#             MenuItem(_("Public Profile"), reverse("contributor-profile"), icon=icon("person")),
#             MenuItem(_("affiliations"), reverse("contributor-affiliations"), icon="fas fa-building-user"),
#             MenuItem(_("identifiers"), reverse("contributor-identifiers"), icon="fa fa-fingerprint"),
#         ],
#     )
# )


# AccountSubMenu = SettingsMenu.submenus["Account"]


# AccountSubMenu.children.append(
#     MenuItem(_("identifiers"), reverse("user:contributor-identifiers"), icon="fa fa-fingerprint"),
# )
