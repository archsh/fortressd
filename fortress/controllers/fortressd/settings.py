# -*- coding: utf-8 -*-
"""{{target.capitalize()}} controller module"""

from tg import expose, flash, require, url, lurl
from tg import request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg import predicates
from fortress import model

from fortress.lib.base import BaseController


class SettingController(BaseController):
    # Uncomment this line if your controller requires an authenticated user
    allow_only = predicates.has_permission('administration', msg=l_('Only for administrators'))

    def _before(self, *args, **kw):
        tmpl_context.page_name = "Fortressd"

    @expose('fortress.templates.settings.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')


