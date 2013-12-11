# -*- coding: utf-8 -*-
"""Tests around :py:mod:`transmutator.cli`."""
from StringIO import StringIO
import sys
import unittest

import transmutator
from transmutator import cli


class sys_output(object):
    def __init__(self):
        self.stdout_backup = None
        self.stderr_backup = None
        self.stdout = StringIO()
        self.stderr = StringIO()

    def __enter__(self):
        self.stdout_backup = sys.stdout
        self.stderr_backup = sys.stderr
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is None:
            sys.stdout = self.stdout_backup
            sys.stderr = self.stderr_backup
            self.stdout = self.stdout.getvalue()
            self.stderr = self.stderr.getvalue()


class TransmuteTestCase(unittest.TestCase):
    """Tests around :py:func:`transmutator.cli.transmute`."""
    def transmute(self, args=[]):
        """Run transmute with args and assert it raises SystemExit."""
        with self.assertRaises(SystemExit) as context:
            cli.transmute(args, 'transmute')
        return context.exception.code

    def test_version(self):
        """`transmute --version` displays package's version."""
        with sys_output() as output:
            self.assertEqual(self.transmute(['--version']), 0)
        self.assertEqual(output.stdout, '')
        self.assertEqual(output.stderr,
                         transmutator.__version__ + '\n')
