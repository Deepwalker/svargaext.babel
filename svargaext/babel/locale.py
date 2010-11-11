# Code derived from flaskext.babel

import os
import sys
from babel import dates, support, Locale
from werkzeug import ImmutableDict

from svarga.core.env import env
from svargaext.babel.lazy import LazyString


class Babel(object):
    """Central controller class that can be used to configure how
    Svarga-Babel behaves."""

    i18n_dirs = []
    i18n_apps = []

    loaded_translations = {}

    @classmethod
    def add_dir(cls, app, path):
        cls.i18n_apps.append(app)
        cls.i18n_dirs.append(path)

    @classmethod
    def default_locale(cls):
        """The default locale from the configuration as instance of a
        `babel.Locale` object.
        """
        return Locale.parse(env.settings.BABEL_DEFAULT_LOCALE)

    @classmethod
    def locale_selector(cls):
        locale = env.request.cookies.get('svarga_locale')
        if locale:
            return locale

        accept = env.request.accept_languages.values()
        locale = [l for l in accept if l in Babel.locales]
        return locale[0] if locale else None


def load_translations(locales):
    # Try return from cache
    if locales in Babel.loaded_translations:
        return Babel.loaded_translations[locales]

    translations_list = []
    for dir in Babel.i18n_dirs:
        # Try to load '.mo' from dir
        translation = support.Translations.load(dir, locales)
        if isinstance(translation, support.Translations):
            translations_list.append(translation)

    if translations_list:
        translations = translations_list[0]
        # Add translations to first one
        for t in translations_list[1:]:
            translations.add(t)
    else:
        translations = None
    # Cache it
    Babel.loaded_translations[locales] = translations
    # And return
    return translations


def get_translations():
    """Returns the correct gettext translations that should be used for
    ths request.  This will never fail and return a dummy translation
    object if used outside of the request or if a translation cannot be
    found.
    """
    locales = get_locale()
    if not locales:
        return None

    translations = getattr(env, 'translations', None)

    if (not translations) and Babel.i18n_dirs:
        translations = env.translations = load_translations(locales)

    return translations


def get_locale():
    """Returns the locale that should be used for this request as
    `babel.Locale` object.  This returns `None` if used outside of
    a request.
    """
    try:
        locale = getattr(env, 'babel_locale', None)
    except RuntimeError:
        return None

    if locale is None:
        rv = Babel.locale_selector()
        if rv is None:
            locale = Babel.default_locale()
        else:
            locale = Locale.parse(rv)
        env.babel_locale = locale
    return locale


def gettext(string, **variables):
    """Translates a string with the current locale and passes in the
    given keyword arguments as mapping to a string formatting string::

        gettext(u'Hello World!')
        gettext(u'Hello %(name)s!', name='World')
    """
    t = get_translations()
    if t is None:
        return string % variables
    return t.ugettext(string) % variables


def ngettext(singular, plural, num, **variables):
    """Translates a string with the current locale and passes in the
    given keyword arguments as mapping to a string formatting string.
    The `num` parameter is used to dispatch between singular and various
    plural forms of the message.  It is available in the format string
    as ``%(num)d`` or ``%(num)s``.  The source language should be
    English or a similar language which only has one plural form.

    ::

        ngettext(u'%(num)d Apple', u'%(num)d Apples', num=len(apples))
    """
    variables.setdefault('num', num)
    t = get_translations()
    if t is None:
        return (singular if num == 1 else plural) % variables
    return t.ungettext(singular, plural, num) % variables


def lazy_gettext(string, **variables):
    """Like :func:`gettext` but the string returned is lazy which means
    it will be translated when it is used as an actual string.
    """
    return LazyString(gettext, string, **variables)
