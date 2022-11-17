from geoluminate.menus import Menu, Node
from django.urls import reverse, resolve
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, resolve, path, include
from django.views.generic import DetailView
from .models import Publication


class PubNode(Node):
    base_template_name = "literature/hx/"
    model = Publication

    def url_pattern(self):
        return path(f'{self.name}/',
                    DetailView.as_view(
                        template_name=f"{self.base_template_name}{self.name}.html",
                        model=self.model),
                    name=self.name)

# class OffCanvas(Node):


class PublicationMenu(Menu):

    def nodes(self):
        return [
            PubNode('about', icon='fa-book', object=self.object),
            PubNode('data', icon='fa-table', object=self.object),
            PubNode('map', icon='fa-map', object=self.object),
            PubNode('related', icon='fa-network-wired', object=self.object),
            PubNode('discussion', icon='fa-comments', object=self.object),
            PubNode('tools', icon='fa-wrench', object=self.object),
        ]
