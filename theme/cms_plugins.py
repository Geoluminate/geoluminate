from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from .models import Section, Heading, Image, Feature, PageHeading

@plugin_pool.register_plugin
class SectionPlugin(CMSPluginBase):
    module = 'GeoLuminate'
    model = Section
    render_template = "section.html"
    cache = False
    name = _('Section')
    allow_children = True


@plugin_pool.register_plugin
class ContentPlugin(CMSPluginBase):
    module = 'GeoLuminate'
    render_template = "content.html"
    cache = False
    name = _('Content')
    allow_children = True


@plugin_pool.register_plugin
class HeadingPlugin(CMSPluginBase):
    module = 'GeoLuminate'
    model = Heading
    render_template = "heading.html"
    cache = False
    name = _('Heading')
    require_parent = True


@plugin_pool.register_plugin
class ImagePlugin(CMSPluginBase):
    module = 'GeoLuminate'
    model = Image
    render_template = "image.html"
    cache = False
    name = _('Image')


@plugin_pool.register_plugin
class FeaturePlugin(CMSPluginBase):
    module = 'GeoLuminate'
    model = Feature
    render_template = "feature.html"
    cache = False
    name = _('Feature')


@plugin_pool.register_plugin
class FeatureContainerPlugin(CMSPluginBase):
    module = 'GeoLuminate'
    render_template = "feature_container.html"
    cache = False
    name = _('Feature Container')
    allow_children = True


@plugin_pool.register_plugin
class PageHeadingPlugin(CMSPluginBase):
    module = 'GeoLuminate'
    model = PageHeading
    render_template = "page_heading.html"
    cache = False
    name = _('Page Heading')
    allow_children = True