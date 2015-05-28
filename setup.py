#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Python packaging."""
import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    """Test command that runs tox."""
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox  # import here, cause outside the eggs aren't loaded.
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)


#: Absolute path to directory containing setup.py file.
here = os.path.abspath(os.path.dirname(__file__))
#: Boolean, ``True`` if environment is running Python version 2.
IS_PYTHON2 = sys.version_info[0] == 2

# Data for use in setup.
NAME = 'transmutator'
DESCRIPTION = "General purpose migration framework (upgrades, downgrades)."
README = open(os.path.join(here, 'README.rst')).read()
VERSION = open(os.path.join(here, 'VERSION')).read().strip()
AUTHOR = u'Benoît Bryon'
EMAIL = 'benoit@marmelune.net'
LICENSE = 'BSD'
URL = 'https://{name}.readthedocs.org/'.format(name=NAME)
CLASSIFIERS = [
    'License :: OSI Approved :: BSD License',
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 2.7',
]
KEYWORDS = [
    'migration',
    'evolution',
    'upgrade',
    'downgrade',
    'shell',
    'deployment',
]
PACKAGES = [NAME.replace('-', '_')]
REQUIREMENTS = [
    'setuptools',
    'xal',
]
ENTRY_POINTS = {
    'console_scripts': [
        'transmute = {name}.cli:transmute'.format(name=PACKAGES[0]),
    ]
}
SETUP_REQUIREMENTS = ['setuptools']
TEST_REQUIREMENTS = ['tox']
CMDCLASS = {'test': Tox}
EXTRA_REQUIREMENTS = {
    'test': TEST_REQUIREMENTS,
}


if __name__ == '__main__':  # Do not run setup() when we import this module.
    setup(
        name=NAME,
        version=VERSION,
        description=DESCRIPTION,
        long_description=README,
        classifiers=CLASSIFIERS,
        keywords=' '.join(KEYWORDS),
        author=AUTHOR,
        author_email=EMAIL,
        url=URL,
        license=LICENSE,
        packages=PACKAGES,
        include_package_data=True,
        zip_safe=False,
        install_requires=REQUIREMENTS,
        entry_points=ENTRY_POINTS,
        tests_require=TEST_REQUIREMENTS,
        cmdclass=CMDCLASS,
        setup_requires=SETUP_REQUIREMENTS,
        extras_require=EXTRA_REQUIREMENTS,
    )
