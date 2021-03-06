from __future__ import unicode_literals

import logging
from warnings import warn

from django.utils.translation import ugettext_lazy as _
from djblets.configforms.mixins import DynamicConfigPageMixin
from djblets.configforms.pages import ConfigPage
from djblets.configforms.registry import ConfigPageRegistry
from djblets.registries.errors import ItemLookupError
from djblets.registries.mixins import ExceptionFreeGetterMixin

from reviewboard.accounts.forms.pages import (AccountSettingsForm,
                                              AvatarSettingsForm,
                                              APITokensForm,
                                              ChangePasswordForm,
                                              ProfileForm,
                                              GroupsForm)


class AccountPageRegistry(ExceptionFreeGetterMixin, ConfigPageRegistry):
    """A registry for managing account pages."""

    lookup_attrs = ('page_id',)

    def get_defaults(self):
        """Return the default page classes.

        Returns:
            type: The page classes, as subclasses of :py:class:`AccountPage`.
        """
        return (GroupsPage, AccountSettingsPage, AuthenticationPage,
                ProfilePage, APITokensPage)

    def unregister(self, page_class):
        """Unregister the page class.

        Args:
            page_class (type):
                The page class to unregister.

        Raises:
            ItemLookupError:
                This exception is raised if the specified page class cannot
                be found.
        """
        try:
            super(AccountPageRegistry, self).unregister(page_class)
        except ItemLookupError as e:
            logging.error(e)
            raise e


class AccountPage(DynamicConfigPageMixin, ConfigPage):
    """Base class for a page of forms in the My Account page.

    Each AccountPage is represented in the My Account page by an entry
    in the navigation sidebar. When the user has navigated to that page,
    any forms shown on the page will be displayed.

    Extensions can provide custom pages in order to offer per-user
    customization.
    """

    registry = AccountPageRegistry()


class AccountSettingsPage(AccountPage):
    """A page containing the primary settings the user can customize."""

    page_id = 'settings'
    page_title = _('Settings')
    form_classes = [AccountSettingsForm]


class APITokensPage(AccountPage):
    """A page containing settings for API tokens."""

    page_id = 'api-tokens'
    page_title = _('API Tokens')
    form_classes = [APITokensForm]


class AuthenticationPage(AccountPage):
    """A page containing authentication-related forms.

    By default, this just shows the Change Password form, but extensions
    can provide additional forms for display.
    """

    page_id = 'authentication'
    page_title = _('Authentication')
    form_classes = [ChangePasswordForm]


class ProfilePage(AccountPage):
    """A page containing settings for the user's profile."""

    page_id = 'profile'
    page_title = _('Profile')
    form_classes = [ProfileForm, AvatarSettingsForm]


class GroupsPage(AccountPage):
    """A page containing a filterable list of groups to join."""

    page_id = 'groups'
    page_title = _('Groups')
    form_classes = [GroupsForm]


def register_account_page_class(cls):
    """Register a custom account page class.

    A page ID is considered unique and can only be registered once.

    Args:
        cls (type):
            The page class to register, as a subclass of
            :py:class:`AccountPage`.

    Raises:
        djblets.registries.errors.AlreadyRegisteredError:
            Raised if the page or any of its forms have already been
            registered.

        djblets.registries.errors.RegistrationError:
            Raised if the page shares an attribute with an already
            registered page or if any of its forms share an attribute
            with an already registered form.
    """
    warn('register_account_page_class is deprecated in Review Board 3.0 and '
         'will be removed; use AccountPage.registry.register instead.',
         DeprecationWarning)
    AccountPage.registry.register(cls)


def unregister_account_page_class(page_cls):
    """Unregister a previously registered account page class.

    Args:
        page_cls (type):
            The page class to unregister, as a subclass of
            :py:class:`AccountPage`.
    """
    warn('unregister_account_page_class is deprecated in Review Board 3.0 and '
         'will be removed; use AccountPage.registry.unregister instead.',
         DeprecationWarning)
    AccountPage.registry.unregister(page_cls)


def get_page_class(page_id):
    """Return the account page class with the specified ID.

    Args:
        page_id (unicode):
            The page's unique identifier.

    Returns:
        type:
        The :py:class:`AccountPage` subclass, or ``None`` if it could not be
        found.
    """
    warn('get_page_class is deprecated in Review Board 3.0 and will be '
         'removed; use AccountPage.registry.get instead.',
         DeprecationWarning)
    return AccountPage.registry.get('page_id', page_id)


def get_page_classes():
    """Yield all registered page classes.

    Yields:
        type: Each registered page class, as a subclass of
        :py:class:`AccountPage`.
    """
    warn('get_page_classes is deprecated in Review Board 3.0 and will be '
         'removed; iterate through AccountPage.registry instead.',
         DeprecationWarning)
    return iter(AccountPage.registry)
