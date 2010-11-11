from datetime import datetime
from pytz import timezone, UTC

from svarga import template
from svarga.core.env import env

from svargaext.babel import Babel


default_date_formats = ImmutableDict({
    'time':             'medium',
    'date':             'medium',
    'datetime':         'medium',
    'time.short':       None,
    'time.medium':      None,
    'time.full':        None,
    'time.long':        None,
    'date.short':       None,
    'date.medium':      None,
    'date.full':        None,
    'date.long':        None,
    'datetime.short':   None,
    'datetime.medium':  None,
    'datetime.full':    None,
    'datetime.long':    None,
})


def _get_format(key, format):
    """A small helper for the datetime formatting functions.  Looks up
    format defaults for different kinds.
    """
    babel = env.babel_instance
    if format is None:
        format = babel.date_formats[key]
    if format in ('short', 'medium', 'full', 'long'):
        rv = babel.date_formats['%s.%s' % (key, format)]
        if rv is not None:
            format = rv
    return format


def get_timezone():
    """Returns the timezone that should be used for this request as
    `pytz.timezone` object.  This returns `None` if used outside of
    a request.
    """
    tzinfo = getattr(env, 'babel_tzinfo', None)
    if tzinfo is None:
        rv = Babel.timezone_selector()
        if rv is None:
            tzinfo = Babel.default_timezone()
        else:
            if isinstance(rv, basestring):
                tzinfo = timezone(rv)
            else:
                tzinfo = rv
        env.babel_tzinfo = tzinfo
    return tzinfo


def to_user_timezone(datetime):
    """Convert a datetime object to the user's timezone.  This automatically
    happens on all date formatting unless rebasing is disabled.  If you need
    to convert a :class:`datetime.datetime` object at any time to the user's
    timezone (as returned by :func:`get_timezone` this function can be used).
    """
    if datetime.tzinfo is None:
        datetime = datetime.replace(tzinfo=UTC)
    tzinfo = get_timezone()
    return tzinfo.normalize(datetime.astimezone(tzinfo))


def to_utc(datetime):
    """Convert a datetime object to UTC and drop tzinfo.  This is the
    opposite operation to :func:`to_user_timezone`.
    """
    if datetime.tzinfo is None:
        datetime = get_timezone().localize(datetime)
    return datetime.astimezone(UTC).replace(tzinfo=None)


@template.filter
def format_datetime(datetime=None, format=None, rebase=True):
    """Return a date formatted according to the given pattern.  If no
    :class:`~datetime.datetime` object is passed, the current time is
    assumed.  By default rebasing happens which causes the object to
    be converted to the users's timezone (as returned by
    :func:`to_user_timezone`).  This function formats both date and
    time.

    The format parameter can either be ``'short'``, ``'medium'``,
    ``'long'`` or ``'full'`` (in which cause the language's default for
    that setting is used, or the default from the :attr:`Babel.date_formats`
    mapping is used) or a format string as documented by Babel.
    """
    format = _get_format('datetime', format)
    return _date_format(dates.format_datetime, datetime, format, rebase)


@template.filter
def format_date(date=None, format=None, rebase=True):
    """Return a date formatted according to the given pattern.  If no
    :class:`~datetime.datetime` or :class:`~datetime.date` object is passed,
    the current time is assumed.  By default rebasing happens which causes
    the object to be converted to the users's timezone (as returned by
    :func:`to_user_timezone`).  This function only formats the date part
    of a :class:`~datetime.datetime` object.

    The format parameter can either be ``'short'``, ``'medium'``,
    ``'long'`` or ``'full'`` (in which cause the language's default for
    that setting is used, or the default from the :attr:`Babel.date_formats`
    mapping is used) or a format string as documented by Babel.
    """
    if rebase and isinstance(date, datetime):
        date = to_user_timezone(date)
    format = _get_format('date', format)
    return _date_format(dates.format_date, date, format, rebase)


@template.filter
def format_time(time=None, format=None, rebase=True):
    """Return a time formatted according to the given pattern.  If no
    :class:`~datetime.datetime` object is passed, the current time is
    assumed.  By default rebasing happens which causes the object to
    be converted to the users's timezone (as returned by
    :func:`to_user_timezone`).  This function formats both date and
    time.

    The format parameter can either be ``'short'``, ``'medium'``,
    ``'long'`` or ``'full'`` (in which cause the language's default for
    that setting is used, or the default from the :attr:`Babel.date_formats`
    mapping is used) or a format string as documented by Babel.
    """
    format = _get_format('time', format)
    return _date_format(dates.format_time, time, format, rebase)


@template.filter
def format_timedelta(datetime_or_timedelta, granularity='second'):
    """Format the elapsed time from the given date to now or the given
    timedelta.  This currently requires an unreleased development
    version of Babel.
    """
    if isinstance(datetime_or_timedelta, datetime):
        datetime_or_timedelta = datetime.utcnow() - datetime_or_timedelta
    return dates.format_timedelta(datetime_or_timedelta, granularity,
                                  locale=get_locale())


def _date_format(formatter, obj, format, rebase, **extra):
    """Internal helper that formats the date."""
    locale = get_locale()
    extra = {}
    if formatter is not dates.format_date and rebase:
        extra['tzinfo'] = get_timezone()
    return formatter(obj, format, locale=locale, **extra)


