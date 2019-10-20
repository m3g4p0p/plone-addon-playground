from Acquisition import aq_inner
from plone.app.layout.navigation.navtree import buildFolderTree, NavtreeStrategyBase
from plone.app.layout.navigation.root import getNavigationRoot
from Products.Five.browser import BrowserView
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
            self.__context = self.node['item'].getObject()

        return self.__context

    def view(self, name):
        try:
            view = self.context.unrestrictedTraverse('@@' + name)
        except AttributeError:
            raise RuntimeError('%s not found for %s' % (name, str(context)))

        return view()



class NavigationStrategy(NavtreeStrategyBase):
    ''' Strategy for building a navigation tree '''

    def __init__(self, context):
        super(NavigationStrategy, self).__init__()
        self.rootPath = getNavigationRoot(context)


    def set_object(self, node):
        node['obj'] = self.get_object(node)

    def is_mega_menu(self, node):
        item = self.get_object(node)

        return (
            IMegaMenuContainer.providedBy(item) and
            item.is_mega_menu
        )

    def nodeFilter(self, node):
        return not getattr(node['item'], 'exclude_from_nav', False)

    def decoratorFactory(self, node):
        node['util'] = NodeUtil(node)
        return node


class NavigationView(BrowserView):
    ''' View for the navigation '''

    def pretty(self):
        return pp().pformat(self.navtree())

    def __populate_mega_menu(self, nodes):
        for node in nodes:
            current_context = node['util'].context
            is_mega_menu = IMegaMenuContainer.providedBy(current_context) and current_context.is_mega_menu
            is_mega_menu_item = not is_mega_menu and IMegaMenuImages.providedBy(current_context)

            node['is_mega_menu'] = is_mega_menu
            node['is_mega_menu_item'] = is_mega_menu_item

            if is_mega_menu:
                self.__populate_mega_menu(node['children'])

            elif is_mega_menu_item:
                node['item_view'] = node['util'].view('megaitemview')

        return nodes

    def navtree(self):
        strategy = NavigationStrategy(self.context)
        path = getNavigationRoot(self.context)
        query = { 'path': { 'query': path, 'depth': 2 } }

        tree = buildFolderTree(
            self.context,
            query=query,
            strategy=strategy
        )

        return self.__populate_mega_menu(tree['children'])
