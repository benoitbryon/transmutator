# -*- coding: utf-8 -*-
"""General purpose migration (upgrade, downgrade) framework."""
import pkg_resources


#: Module version, as defined in :pep:`396`.
__version__ = pkg_resources.get_distribution(__package__).version


# API shortcuts.
from transmutator.api import *  # NoQA
