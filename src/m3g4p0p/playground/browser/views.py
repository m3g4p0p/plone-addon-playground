from plone.dexterity.browser.view import DefaultView
from plone import api
from ..interfaces import IEvent

class FooView(DefaultView):
    def all_events(self):
        return [event.getObject() for event in api.content.find(object_provides=IEvent)]

class BarView(DefaultView):
    def subject(self):
        return u'bar'
