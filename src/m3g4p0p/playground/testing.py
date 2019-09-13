# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import m3g4p0p.playground


class M3G4P0PPlaygroundLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=m3g4p0p.playground)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'm3g4p0p.playground:default')


M3G4P0P_PLAYGROUND_FIXTURE = M3G4P0PPlaygroundLayer()


M3G4P0P_PLAYGROUND_INTEGRATION_TESTING = IntegrationTesting(
    bases=(M3G4P0P_PLAYGROUND_FIXTURE,),
    name='M3G4P0PPlaygroundLayer:IntegrationTesting',
)


M3G4P0P_PLAYGROUND_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(M3G4P0P_PLAYGROUND_FIXTURE,),
    name='M3G4P0PPlaygroundLayer:FunctionalTesting',
)


M3G4P0P_PLAYGROUND_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        M3G4P0P_PLAYGROUND_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='M3G4P0PPlaygroundLayer:AcceptanceTesting',
)
