# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl
from tg import request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg import predicates
# from fortress import model
# from fortress.controllers.secure import SecureController
# from fortress.model import DBSession
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig
# from tgext.admin.controller import AdminController
from fortress.lib.base import BaseController
from fortress.controllers.error import ErrorController
from fortress.controllers.fortressd import (AuthorizationController,
                                            InfrastructureController,
                                            HistoryController,
                                            UserController,
                                            ProfileController,
                                            RequestController,
                                            TerminalController, )
import logging
log = logging.getLogger(__name__)
__all__ = ['RootController']


class FortressAdminConfig(TGAdminConfig):
    allow_only = predicates.in_group('administrators')


class RootController(BaseController):
    """
    The root controller for the fortressd application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    # secc = SecureController()
    # admin = AdminController(model, DBSession, config_type=FortressAdminConfig)

    error = ErrorController()
    profile = ProfileController()
    request = RequestController()
    history = HistoryController()
    terminal = TerminalController()

    def _before(self, *args, **kw):
        tmpl_context.project_name = _("FORTRESSD")

    @expose('fortress.templates.index')
    def index(self):
        """Handle the front-page."""
        # log.debug("Default Root Index .................")
        return dict(page='index')

    @expose('fortress.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('fortress.templates.management.index')
    @require(predicates.has_permission('administration', msg=l_('Only for administrators')))
    def management(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(page='management', environment=request.environ)


    @expose('fortress.templates.settings.index')
    @require(predicates.has_permission('administration', msg=l_('Only for administrators')))
    def settings(self, **kw):
        """
        This method showcases how you can use the same controller
        for a data page and a display page.
        """
        return dict(page='settings', params=kw)

    @expose('fortress.templates.index')
    @require(predicates.has_permission('administration', msg=l_('Only for administrators')))
    def admin_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='administrator stuff')

    @expose('fortress.templates.index')
    @require(predicates.is_user('operate', msg=l_('Only for the operators')))
    def operator_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='operator stuff')

    @expose('fortress.templates.login')
    def login(self, came_from=lurl('/'), failure=None, login=''):
        """Start the user login."""
        if failure is not None:
            if failure == 'user-not-found':
                flash(_('User not found'), 'error')
            elif failure == 'invalid-password':
                flash(_('Invalid Password'), 'error')

        login_counter = request.environ.get('repoze.who.logins', 0)
        if failure is None and login_counter > 0:
            flash(_('Wrong credentials'), 'warning')

        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from, login=login)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ.get('repoze.who.logins', 0) + 1
            redirect('/login',
                     params=dict(came_from=came_from, __logins=login_counter))
        # userid = request.identity['repoze.who.userid']
        user = request.identity['user']
        log.debug(">>> request.identity: %s", request.identity.items())
        flash(_('Welcome back, %s!') % user.display_name)

        # Do not use tg.redirect with tg.url as it will add the mountpoint
        # of the application twice.
        return HTTPFound(location=came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        return HTTPFound(location=came_from)
