from menus.base import Modifier
from menus.menu_pool import menu_pool
from cms.models import Page


class AddIconModifier(Modifier):
    """Adds the new page Icon to the corresponding menu node so that
    icons can be rendered alongside their label in the menu template."""

    def modify(self, request, nodes, namespace, root_id, post_cut, breadcrumb):
        # only do something when the menu has already been cut
        if post_cut:
            # only consider nodes that refer to cms pages
            # and put them in a dict for efficient access
            page_nodes = {n.id: n for n in nodes if n.attr["is_page"]}
            # retrieve the attributes of interest from the relevant pages
            pages = Page.objects.select_related('icon').filter(
                id__in=page_nodes.keys()).values(
                'id', 'icon__icon')
            # loop over all relevant pages
            for page in pages:
                # take the node referring to the page
                node = page_nodes[page['id']]
                # put the icon attribute on the node
                node.attr["icon"] = page['icon__icon']

        return nodes


menu_pool.register_modifier(AddIconModifier)
