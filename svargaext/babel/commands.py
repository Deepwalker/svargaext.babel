import os.path as op
import subprocess

from svarga.core.dispatch import command
from svarga.core.env import env
from svarga.utils.imports import import_module

from svargaext.babel import Babel


@command(usage='[-n APPNAME]')
def update_i18n(name=('n', '', 'app name')):
    'Update locale files for APP'
    print name, bool(name)
    apps = [name] if name else Babel.i18n_apps
    for app_name in apps:
        update_app_i18n(app_name)


@command(usage='[-n APPNAME]')
def compile_i18n(name=('n', '', 'app name')):
    'Compile locale files for APP'
    apps = [name] if name else Babel.i18n_apps
    for app_name in apps:
        compile_app_i18n(app_name)


def update_app_i18n(name):
    print 'Update locales for', name
    module = import_module(name)
    base_path = op.normpath( op.dirname( module.__file__) )
    i18n_path = op.join( base_path, 'i18n')
    tmp_pot = op.join('/tmp/', name)

    subprocess.call(['pybabel', 'extract', '-o', tmp_pot,
                '-k', 'lazy_gettext', '-k', '_', base_path])
    for l in Babel.locales:
        if op.isdir(op.join(i18n_path, l)):
            operation = 'update'
        else:
            operation = 'init'
        subprocess.call(['pybabel', operation, '-d', i18n_path, '-i', tmp_pot, '-l', l])


def compile_app_i18n(name):
    print 'Compile locales for', name
    module = import_module(name)
    base_path = op.normpath( op.dirname( module.__file__) )
    i18n_path = op.join( base_path, 'i18n')
    for l in Babel.locales:
        subprocess.call(['pybabel', 'compile', '-d', i18n_path, '-l', l])

