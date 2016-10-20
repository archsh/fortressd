# -*- coding: utf-8 -*-

#  Quickstarted Options:
#
#  sqlalchemy: True
#  auth:       sqlalchemy
#  mako:       False
#
#

# This is just a work-around for a Python2.7 issue causing
# interpreter crash at exit when trying to log an info message.
try:
    import logging
    import multiprocessing
except:
    pass

import sys
py_version = sys.version_info[:2]

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

testpkgs = [
    'WebTest >= 1.2.3',
    'nose',
    'coverage',
    'gearbox'
]

install_requires = [
    "TurboGears2 >= 2.3.9",
    "Beaker >= 1.8.0",
    "Kajiki >= 0.3.5",
    "zope.sqlalchemy >= 0.4",
    "sqlalchemy",
    "alembic",
    "repoze.who",
    "tw2.forms",
    "tgext.admin >= 0.6.1",
    "WebHelpers2"
]

if py_version != (3, 2):
    # Babel not available on 3.2
    install_requires.append("Babel")
if py_version == (3, 2):
    # jinja2 2.7 is incompatible with Python 3.2
    install_requires.append('jinja2 < 2.7')
else:
    install_requires.append('jinja2')
setup(
    name='fortressd',
    version='0.1',
    description='',
    author='Mingcai SHEN',
    author_email='archsh@gmail.com',
    url='https://github.com/archsh/fortressd',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=install_requires,
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=testpkgs,
    package_data={'fortress': [
        'i18n/*/LC_MESSAGES/*.mo',
        'templates/*/*',
        'public/*/*'
    ]},
    message_extractors={'fortress': [
        ('**.py', 'python', None),
        ('templates/**.jinja', 'jinja2', {'silent': 'true', 'extensions': 'jinja2.ext.autoescape,jinja2.ext.with_'}),
        ('public/**', 'ignore', None)
    ]},
    entry_points={
        'paste.app_factory': [
            'main = fortress.config.middleware:make_app'
        ],
        'gearbox.plugins': [
            'turbogears-devtools = tg.devtools'
        ]
    },
    zip_safe=False
)
