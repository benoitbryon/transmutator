# -*- coding: utf-8 -*-
"""Python packaging."""
import os
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))

NAME = 'transmutator'
DESCRIPTION = """General purpose migration (upgrade, downgrade) framework."""
README = open(os.path.join(here, 'README')).read()
VERSION = open(os.path.join(here, 'VERSION')).read().strip()
PACKAGES = [NAME]
REQUIREMENTS = ['setuptools']
ENTRY_POINTS = {
    'console_scripts': [
        'transmute = %s.cli:transmute' % NAME,
    ]
}
CLASSIFIERS = ['License :: OSI Approved :: BSD License',
               'Development Status :: 1 - Planning',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7']


if __name__ == '__main__':  # Don't run setup() when we import this module.
    setup(name=NAME,
          version=VERSION,
          description=DESCRIPTION,
          long_description=README,
          classifiers=CLASSIFIERS,
          keywords='migration evolution mutation upgrade downgrade release',
          author='Benoît Bryon',
          author_email='benoit@marmelune.net',
          url='https://github.com/benoitbryon/%s' % NAME,
          packages=PACKAGES,
          include_package_data=True,
          zip_safe=False,
          install_requires=REQUIREMENTS,
          entry_points=ENTRY_POINTS)
