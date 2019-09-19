""""Tests around collection of mutations, a.k.a. ``transmute --collect``."""
import unittest

import xal

import transmutator
from transmutator.utils import temporary_directory


class OrchestratorTestCase(unittest.TestCase):
    """Tests around Orchestrator's collect utilities."""
    def setUp(self):
        self.session = xal.LocalSession()
        self.mutations_dir_context = temporary_directory()
        self.root_dir = self.session.path(
            self.mutations_dir_context.__enter__())
        self.mutations_dir = self.root_dir / self.session.path('mutations')
        self.mutations_dir.mkdir()
        working_dir = self.root_dir / self.session.path('var')
        working_dir.mkdir()
        self.orchestrator = transmutator.Orchestrator(
            mutations_dir=str(self.mutations_dir),
            working_dir=str(working_dir))

    def tearDown(self):
        self.mutations_dir_context.__exit__()

    def add_mutation(self, name):
        """Create a mutation in mutation source directory."""
        name = self.session.path(name)
        full_name = self.mutations_dir / name
        if not full_name.parent.exists():
            full_name.parent.mkdir()
        full_name.open('w').write(u'')
        full_name.chmod(0o775)
        return full_name

    def add_mutation_record(self, name, status):
        """Create a mutation in working directory, with given status."""
        name = self.session.path(name)
        status = self.session.path(status)
        working_dir = self.session.path(self.orchestrator.working_dir)
        full_name = working_dir / status / name
        if not full_name.parent.exists():
            full_name.parent.mkdir(parents=True)
        full_name.open('w').write(u'')
        full_name.chmod(0o775)
        return full_name

    def test_is_release(self):
        """Check results of :meth:`Orchestrator.is_release`."""
        # No mutation, no No-name release.
        self.assertFalse(self.orchestrator.is_release(''))
        # Adding a non-executable file: no release added.
        mutation = self.add_mutation('2.0/1-hello.sh')
        mutation.chmod(0o664)
        self.assertFalse(self.orchestrator.is_release(''))
        self.assertFalse(self.orchestrator.is_release('2.0'))
        self.assertFalse(self.orchestrator.is_release('2.0/1-hello.sh'))
        # With an executable: new release detected.
        mutation.chmod(0o775)
        self.assertFalse(self.orchestrator.is_release(''))
        self.assertTrue(self.orchestrator.is_release('2.0'))
        # No-name release matters.
        self.add_mutation('3-hello.sh')
        self.assertTrue(self.orchestrator.is_release(''))
        self.assertTrue(self.orchestrator.is_release('2.0'))
        self.assertFalse(self.orchestrator.is_release('3-hello.sh'))

    def test_is_mutation(self):
        """Check results of :meth:`Orchestrator.is_mutation`."""
        self.assertFalse(self.orchestrator.is_mutation('i-do-not-exist'))
        # Adding a valid mutation.
        mutation = self.add_mutation('1-hello.sh')
        self.assertTrue(self.orchestrator.is_mutation('1-hello.sh'))
        # Mutations are executables.
        mutation.chmod(0o664)
        self.assertFalse(self.orchestrator.is_release('1-hello.sh'))
        mutation.chmod(0o775)
        self.assertTrue(self.orchestrator.is_mutation('1-hello.sh'))
        # Mutations must live within authorized directories.
        mutation.rename(self.root_dir / self.session.path('1-hello.sh'))
        self.assertFalse(self.orchestrator.is_mutation(str(mutation)))

    def test_available_releases(self):
        """Check results of :meth:`Orchestrator.available_releases`."""
        # Initial situation: no release.
        self.assertEqual(
            self.orchestrator.available_releases(),
            [])
        # Adding a non-executable file: no release added.
        mutation = self.add_mutation('2.0/1-hello.sh')
        mutation.chmod(0o664)
        self.assertEqual(
            self.orchestrator.available_releases(),
            [])
        # With an executable: new release detected.
        mutation.chmod(0o775)
        self.assertEqual(
            self.orchestrator.available_releases(),
            ['2.0'])
        # Multiple files in a release don't change list of releases.
        self.add_mutation('2.0/2-hello.sh')
        self.assertEqual(
            self.orchestrator.available_releases(),
            ['2.0'])
        # No-name release matters.
        self.add_mutation('3-hello.sh')
        self.assertEqual(
            self.orchestrator.available_releases(),
            ['', '2.0'])
        # Releases are ordered.
        self.add_mutation('1.0/4-hello.sh')
        self.assertEqual(
            self.orchestrator.available_releases(),
            ['', '1.0', '2.0'])

    def test_latest_release(self):
        self.add_mutation_record('1-hello.sh', 'todo')
