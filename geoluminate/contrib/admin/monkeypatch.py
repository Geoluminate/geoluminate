import logging
from typing import Dict, List

from django.apps import apps
from django.contrib.auth.models import AbstractUser
from jazzmin.utils import (
    get_admin_url,
    get_app_admin_urls,
    get_custom_url,
    get_model_meta,
    get_view_permissions,
)

logger = logging.getLogger(__name__)


def make_menu(
    user: AbstractUser,
    links: List[Dict],
    options: Dict,
    allow_appmenus: bool = True,
    admin_site: str = "admin",
) -> List[Dict]:
    """
    Make a menu from a list of user supplied links
    """
    if not user:
        return []

    model_permissions = get_view_permissions(user)

    menu = []
    for link in links:
        perm_matches = []
        for perm in link.get("permissions", []):
            perm_matches.append(user.has_perm(perm))

        if not all(perm_matches):
            continue

        # Url links
        if "url" in link:
            menu.append(
                {
                    "name": link.get("name", "unspecified"),
                    "url": get_custom_url(link["url"], admin_site=admin_site),
                    "children": None,
                    "new_window": link.get("new_window", False),
                    "icon": link.get("icon", options["default_icon_children"]),
                }
            )

        # Model links
        if "model" in link:
            if link["model"].lower() not in model_permissions:
                continue

            _meta = get_model_meta(link["model"])

            name = _meta.verbose_name_plural.title() if _meta else link["model"]
            menu.append(
                {
                    "name": name,
                    "url": get_admin_url(link["model"], admin_site=admin_site),
                    "children": [],
                    "new_window": link.get("new_window", False),
                    "icon": options["icons"].get(link["model"], options["default_icon_children"]),
                }
            )

        # App links
        elif "app" in link and allow_appmenus:
            children = [
                {
                    "name": child.get("verbose_name", child["name"]),
                    "url": child["url"],
                    "children": None,
                }
                for child in get_app_admin_urls(link["app"], admin_site=admin_site)
                if child["model"] in model_permissions
            ]
            if len(children) == 0:
                continue

            menu.append(
                {
                    "name": getattr(apps.app_configs[link["app"]], "verbose_name", link["app"]).title(),
                    "url": "#",
                    "children": children,
                    "icon": options["icons"].get(link["app"], options["default_icon_children"]),
                }
            )

        elif "children" in link:
            children = []
            for child in link.get("children", []):
                if "model" in child:
                    if child["model"].lower() not in model_permissions:
                        continue

                    _meta = get_model_meta(child["model"])

                    name = _meta.verbose_name_plural.title() if _meta else child["model"]
                    children.append(
                        {
                            "name": name,
                            "url": get_admin_url(child["model"], admin_site=admin_site),
                            "new_window": child.get("new_window", False),
                            "icon": options["icons"].get(child["model"], options["default_icon_children"]),
                        }
                    )
                else:
                    children.append(
                        {
                            "name": child.get("verbose_name", child["name"]),
                            "url": child["url"],
                            "children": None,
                        }
                    )

            # children = [
            #     {
            #         "name": child.get("verbose_name", child["name"]),
            #         "url": child["url"],
            #         "children": None,
            #     }
            #     for child in link.get("children", [])
            # ]
            if len(children) == 0:
                continue

            menu.append(
                {
                    "name": link["name"].title(),
                    "url": "#",
                    "children": children,
                    "icon": link.get("icon", options["default_icon_children"]),
                }
            )

    return menu
