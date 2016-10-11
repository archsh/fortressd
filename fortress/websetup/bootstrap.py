# -*- coding: utf-8 -*-
"""Setup the fortressd application"""
from __future__ import print_function, unicode_literals
import transaction
from fortress import model


def bootstrap(command, conf, vars):
    """Place any commands to setup fortress here"""

    # <websetup.bootstrap.before.auth
    from sqlalchemy.exc import IntegrityError
    try:
        u = model.User()
        u.user_name = 'admin'
        u.display_name = 'Administrator'
        u.email_address = 'admin@example.com'
        u.password = 'adminpass'

        model.DBSession.add(u)

        g = model.Group()
        g.group_name = 'administrators'
        g.display_name = 'Administrators Group'

        g.users.append(u)

        model.DBSession.add(g)

        p = model.Permission()
        p.permission_name = 'administration'
        p.description = 'This permission gives an administrative right'
        p.groups.append(g)

        model.DBSession.add(p)

        u1 = model.User()
        u1.user_name = 'operator'
        u1.display_name = 'Example Operator'
        u1.email_address = 'operator@example.com'
        u1.password = 'operaterpass'

        model.DBSession.add(u1)
        model.DBSession.flush()
        transaction.commit()
    except IntegrityError:
        print('Warning, there was a problem adding your auth data, '
              'it may have already been added:')
        import traceback
        print(traceback.format_exc())
        transaction.abort()
        print('Continuing with bootstrapping...')

    # <websetup.bootstrap.after.auth>
