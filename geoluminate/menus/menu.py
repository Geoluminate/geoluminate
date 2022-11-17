import re
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse, resolve
from django.utils.translation import gettext_lazy as _


class Menu:

    def __init__(self, object=None, **kwargs):
        self.object = object

    def nodes(self, request):
        """
        should return a list of NavigationNode instances
        """
        raise NotImplementedError

    def get_url_patterns(self):
        return [p.url_pattern() for p in self.nodes() if p.url_pattern()]

    def __iter__(self):
        return self.nodes().__iter__()

    def __next__(self):
        return self.nodes().__next__()


class Node(Menu):
    """
    MenuItem represents an item in a menu, possibly one that has a sub-menu (children).
    """

    def __init__(self, title, url=None, check=None,
                 visible=True, slug=None, exact_url=False, **kwargs):
        """
        MenuItem constructor

        title       either a string or a callable to be used for the title
        url         the url of the item
        check       a callable to determine if this item is visible
        slug        used to generate id's in the HTML, auto generated from
                    the title if left as None
        exact_url   normally we check if the url matches the request prefix
                    this requires an exact match if set

        All other keyword arguments passed into the MenuItem constructor are
        assigned to the MenuItem object as attributes so that they may be used
        in your templates. This allows you to attach arbitrary data and use it
        in which ever way suits your menus the best.
        """

        # self.url = url
        self.title = _(title.capitalize())
        self.name = title
        self.visible = visible
        self.check_func = check
        self.slug = slug
        self.exact_url = exact_url
        self.selected = False
        self.parent = None

        # merge our kwargs into our self
        for k in kwargs:
            setattr(self, k, kwargs[k])

    def url(self):
        return reverse(
            f"{self.object._meta.app_label}:{self.name}",
            kwargs={
                'pk': self.object.pk})

    def check(self, request):
        """
        Evaluate if we should be visible for this request
        """
        if callable(self.check_func):
            self.visible = self.check_func(request)

    def process(self, request):
        """
        process determines if this item should visible, if its selected, etc...
        """
        # if we're not visible we return since we don't need to do anymore
        # processing
        self.check(request)
        if not self.visible:
            return

        # evaluate our title
        if callable(self.title):
            self.title = self.title(request)

        # if no title is set turn it into a slug
        if self.slug is None:
            # in python3 we don't need to convert to unicode, in python2 slugify
            # requires a unicode string
            self.slug = slugify(self.title)

        # evaluate children
        if callable(self.children):
            children = list(self.children(request))
        else:
            children = list(self.children)

        for child in children:
            child.parent = self
            child.process(request)

        self.children = [
            child
            for child in children
            if child.visible
        ]
        self.children.sort(key=lambda child: child.weight)

        # if we have no children and MENU_HIDE_EMPTY then we are not visible
        # and should return
        hide_empty = getattr(settings, 'MENU_HIDE_EMPTY', False)
        if hide_empty and len(self.children) == 0:
            self.visible = False
            return

        # find out if one of our children is selected, and mark it as such
        curitem = None
        for item in self.children:
            item.selected = False

            if item.match_url(request):
                if curitem is None or len(curitem.url) < len(item.url):
                    curitem = item

        if curitem is not None:
            curitem.selected = True

    def match_url(self, request):
        """
        match url determines if this is selected
        """
        matched = False
        if self.exact_url:
            if re.match(f"{self.url}$", request.path):
                matched = True
        elif re.match("%s" % self.url, request.path):
            matched = True
        return matched

    def nodes(self):
        return []

    def url_pattern(self):
        return None
