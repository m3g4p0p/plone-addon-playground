from Acquisition import aq_inner
from plone.app.layout.navigation.navtree import buildFolderTree, NavtreeStrategyBase
from plone.app.layout.navigation.root import getNavigationRoot
from Products.Five.browser import BrowserView
from zope.interface.interfaces import ComponentLookupError
from zope.component import getMultiAdapter
from ..interfaces import IEvent
from ..behaviors.megamenu import IMegaMenuContainer, IMegaMenuImages

def pp():
    import pprint
    return pprint.PrettyPrinter(indent=4)


class NodeUtil(object):
    __context = None

    def __init__(self, node):
        super(NodeUtil, self).__init__()
        self.node = node

    @property
    def context(self):
        if self.__context is None:
            # Lazy get and cache expensive database lookup
            self.__context = self.node['item'].getObject()

        return self.__context

    def view(self, request, name):
        try:
            view = getMultiAdapter(
                (aq_inner(self.context), request),
                name=name
            )

        except ComponentLookupError:
            raise RuntimeError('%s not found for %s' % (name, str(self.context)))

        return view()



class NavigationStrategy(NavtreeStrategyBase):
    """ Strategy for building a navigation tree """

    def __init__(self, root_path):
        super(NavigationStrategy, self).__init__()
        self.rootPath = root_path

    def nodeFilter(self, node):
        return not getattr(node['item'], 'exclude_from_nav', False)

    def decoratorFactory(self, node):
        node['util'] = NodeUtil(node)
        return node


class NavigationView(BrowserView):
    """ View for the navigation """

    def __populate_mega_menu(self, tree):
        for node in tree['children']:
            current_context = node['util'].context
            is_mega_menu = IMegaMenuContainer.providedBy(current_context) and current_context.is_mega_menu
            is_mega_item = not is_mega_menu and IMegaMenuImages.providedBy(current_context)

            node['is_mega_menu'] = is_mega_menu
            node['is_mega_item'] = is_mega_item

            if is_mega_menu:
                self.__populate_mega_menu(node)

            elif is_mega_item:
                adapted = IMegaMenuImages(current_context)
                node['navigation_image'] = adapted.navigation_image
                node['mega_item_view'] = node['util'].view(self.request, 'megaitemview')

    def pretty(self):
        return pp().pformat(self.navtree())

    def navtree(self):
        root_path = getNavigationRoot(self.context)
        strategy = NavigationStrategy(root_path)
        query = { 'path': { 'query': root_path, 'depth': 2 } }

        tree = buildFolderTree(
            self.context,
            query=query,
            strategy=strategy
        )

        self.__populate_mega_menu(tree)
        return tree['children']

class MegaItemView(BrowserView):
    """ Mega Menu Item """
