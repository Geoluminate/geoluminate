from simple_menu import Menu, MenuItem
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

Menu.add_item('toolbar', MenuItem(_("Database"),
                                  reverse("database_table"),
                                  #   weight=10,
                                  icon="fa-database"))

Menu.add_item('toolbar', MenuItem(_("Map"),
                                  reverse("viewer"),
                                  #   weight=10,
                                  icon="fa-map-marked-alt"))

Menu.add_item('toolbar', MenuItem(_("API"),
                                  reverse("swagger-ui"),
                                  #   weight=10,
                                  icon="fa-project-diagram"))


Menu.add_item('toolbar', MenuItem(_("Glossary"),
                                  reverse("glossary"),
                                  #   weight=10,
                                  icon="fa-th-list"))


Menu.add_item('toolbar', MenuItem(_("Versions"),
                                  reverse("swagger-ui"),
                                  #   weight=10,
                                  icon="fa-code-branch"))

Menu.add_item('toolbar', MenuItem(_("Literature"),
                                  reverse("literature:list"),
                                  icon="fa-book",
                                  children=(
    MenuItem(_("Catalogue"), reverse("literature:list")),
    MenuItem(_("Authors"), reverse("literature:author_list")),
)
))
