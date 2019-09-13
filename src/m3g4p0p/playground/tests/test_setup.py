# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from m3g4p0p.playground.testing import M3G4P0P_PLAYGROUND_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that m3g4p0p.playground is properly installed."""

    layer = M3G4P0P_PLAYGROUND_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if m3g4p0p.playground is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'm3g4p0p.playground'))

    def test_browserlayer(self):
        """Test that IM3G4P0PPlaygroundLayer is registered."""
        from m3g4p0p.playground.interfaces import (
            IM3G4P0PPlaygroundLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IM3G4P0PPlaygroundLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = M3G4P0P_PLAYGROUND_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['m3g4p0p.playground'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if m3g4p0p.playground is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'm3g4p0p.playground'))

    def test_browserlayer_removed(self):
        """Test that IM3G4P0PPlaygroundLayer is removed."""
        from m3g4p0p.playground.interfaces import \
            IM3G4P0PPlaygroundLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IM3G4P0PPlaygroundLayer,
            utils.registered_layers())
