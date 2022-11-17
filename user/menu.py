from geoluminate.menus import Menu, Node
from django.utils.translation import gettext_lazy as _


class UserAccountMenu(Menu):

    def nodes(self):
        return [
            Node('account', "user:settings", icon='fa-user'),
        ]
