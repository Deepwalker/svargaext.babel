# -*- coding: utf-8 -*-
"""
    svargaext.babel
    ~~~~~~~~~~~~~~

    Implements i18n/l10n support for Svarga applications based on Babel.
    Derived from flaskext.babel from Armin Ronacher.

    :copyright: (c) 2010 by Mihail Krivushin
    :license: BSD, see LICENSE for more details.
"""

__version__ = '0.1'
__author__ = 'Happy Contributor'
__email__ = 'me@example.com'


import os.path as op
from svarga.utils.imports import import_module
from svargaext.babel.locale import Babel, gettext, ngettext, lazy_gettext


def init(settings, env_class):
    settings.default('BABEL_DEFAULT_LOCALE', 'en')
    Babel.locales = settings.default('BABEL_LOCALES', ('en',) )

    # TODO
    if False:
        env_class.jinja.add_extension('jinja2.ext.i18n')
        env_class.jinja.install_gettext_callables(
            lambda x: get_translations().ugettext(x),
            lambda s, p, n: get_translations().ungettext(s, p, n),
            newstyle=True
        )

    settings.add_apps_init(AppsConfig)


class AppsConfig(object):

    def __init__(self, apps, env_class):
        for app, config in apps.iteritems():
            p = op.normpath( op.join( op.dirname( config.module.__file__), 'i18n'))
            if op.isdir(p):
                Babel.add_dir(app, p)


def refresh():
    'Clean translations attr from env'
    for key in 'babel_locale', 'babel_translations':
        if hasattr(Babel, key):
            delattr(Babel, key)


