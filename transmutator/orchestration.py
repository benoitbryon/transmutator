import os
import shutil

from xal.session.local import LocalSession


class Orchestrator(object):
    def __init__(self, mutations_dir=None, working_dir=None):
        root_dir = os.path.abspath(os.getcwd())

        #: Directory where to load source mutations.
        self.mutations_dir = mutations_dir
        if mutations_dir is None:
            self.mutations_dir = os.path.join(root_dir, 'mutations')

        #: Directory where to store internal data.
        self.working_dir = working_dir
        if working_dir is None:
            self.working_dir = os.path.join(root_dir, 'var', 'transmutator')
        if not os.path.isdir(self.working_dir):
            os.makedirs(self.working_dir)

        #: Directory where mutations that are about to be run are stored.
        self.todo_dir = os.path.join(self.working_dir, 'todo')
        if not os.path.isdir(self.todo_dir):
            os.makedirs(self.todo_dir)

        #: Directory where mutations that are being run are stored.
        self.doing_dir = os.path.join(self.working_dir, 'doing')
        if not os.path.isdir(self.doing_dir):
            os.makedirs(self.doing_dir)

        #: Directory where mutations that have been run are stored.
        self.done_dir = os.path.join(self.working_dir, 'done')
        if not os.path.isdir(self.done_dir):
            os.makedirs(self.done_dir)

    def is_release(self, release):
        """Return ``True`` if ``release`` is a valid one.

        Checks are:

        * release is a directory, it exists;
        * release contains at least one mutation.

        """
        if os.path.isdir(os.path.join(self.mutations_dir, release)):
            if self.has_mutations(release):
                return True
        return False

    def is_mutation(self, mutation):
        """Return ``True`` if ``mutation`` is a valid one.

        Checks are:

        * mutation is a file, it exists;
        * mutation lives within directories of mutations;
        * mutation is executable

        """
        filename = self.mutation_sourcefile(mutation)
        if not filename.startswith(self.mutations_dir):
            return False
        if not os.path.isfile(filename):
            return False
        if not os.access(filename, os.X_OK):
            return False
        return True

    def is_done(self, mutation):
        """Return ``True`` if ``mutation`` has already been performed."""
        return os.path.isfile(os.path.join(self.done_dir, mutation))

    def is_new(self, mutation):
        """Return ``True`` if ``mutation`` has not been performed yet."""
        return not os.path.exists(os.path.join(self.done_dir, mutation))

    def is_recurrent(self, mutation):
        """Return ``True`` if ``mutation`` has to be performed on every run."""
        return mutation.startswith('recurrent/')

    def is_in_development(self, mutation):
        """Return ``True`` if ``mutation`` is in development.

        On forward, in-development mutations go backward and forward.

        """
        return self.release(mutation) == 'development'

    def current_release(self):
        """Return latest release for which mutations have been applied."""
        current_release = None
        releases = self.done_releases()
        try:
            current_release = releases.pop(-1)
            if current_release == 'development':
                current_release = releases.pop(-1)
        except IndexError:
            pass
        return current_release

    def latest_release(self, development=False):
        """Return name of latest release that has been applied."""
        done_releases = self.done_releases()
        try:
            while True:
                latest = done_releases.pop(-1)
                if development:
                    if latest == 'development':
                        return latest
                else:
                    if latest != 'development':
                        return latest
        except IndexError:
            return None

    def done_releases(self):
        """Return list of releases that have been applied."""
        releases = []
        noname_release = False
        development_release = False
        for name in os.listdir(self.done_dir):
            if os.path.isdir(os.path.join(self.done_dir, name)):
                if name == 'development':
                    development_release = True
                elif name == 'recurrent':
                    pass
                else:
                    releases.append(name)
            else:
                noname_release = True
        releases.sort()
        if noname_release:
            releases.insert(0, '')
        if development_release:
            releases.append('development')
        return releases

    def available_releases(self, development=False, recurrent=False):
        """Return ordered list of available releases."""
        releases = set()
        noname_release = False
        development_release = False
        for name in os.listdir(self.mutations_dir):
            if self.is_release(name):
                if name == 'development':
                    if development:
                        development_release = True
                elif name == 'recurrent' and not recurrent:
                    pass
                else:
                    releases.add(name)
            elif self.is_mutation(name):
                noname_release = True
        releases = list(releases)
        releases.sort()
        if noname_release:
            releases.insert(0, '')
        if development_release:
            releases.append('development')
        return releases

    def next_release(self):
        """Return name of next release to process."""
        current_release = self.current_release()
        for release in self.available_releases():
            if current_release < release:
                return release
        return None

    def latest_mutation(self, development=False):
        """Return name of latest mutation applied.

        Excludes "development" release.

        """
        done_mutations = self.done_mutations()
        try:
            while True:
                latest = done_mutations.pop(-1)
                if development:
                    if latest.startswith('development/'):
                        return latest
                else:
                    if not latest.startswith('development/'):
                        return latest
        except IndexError:
            return None

    def done_mutations(self):
        """Return ordered list of done mutations."""
        mutations = []
        for (dirpath, dirnames, filenames) in os.walk(self.done_dir):
            for filename in filenames:
                relative_dirname = dirpath[len(self.done_dir):]
                relative_dirname = relative_dirname.lstrip(os.path.sep)
                relative_filename = os.path.join(relative_dirname, filename)
                mutations.append(relative_filename)
        return sorted(mutations)

    def mutation_sourcefile(self, mutation):
        """Return absolute filename to mutation."""
        filename = os.path.join(self.mutations_dir, mutation)
        filename = os.path.normpath(filename)
        return filename

    def has_mutations(self, release=None):
        """Return True if release has at least one mutation."""
        for (dirpath, dirnames, filenames) in os.walk(self.mutations_dir):
            for filename in filenames:
                relative_dirname = dirpath[len(self.mutations_dir):]
                relative_dirname = relative_dirname.lstrip(os.path.sep)
                if release is None:
                    if relative_dirname in ['development', 'recurrent']:
                        continue
                elif relative_dirname != release:
                    continue
                relative_filename = os.path.join(relative_dirname, filename)
                if self.is_mutation(relative_filename):
                    return True
        return False

    def available_mutations(self, release=None):
        """Iterates over all available mutations."""
        mutations = []
        for (dirpath, dirnames, filenames) in os.walk(self.mutations_dir):
            for filename in filenames:
                relative_dirname = dirpath[len(self.mutations_dir):]
                relative_dirname = relative_dirname.lstrip(os.path.sep)
                if release is None:
                    if relative_dirname in ['development', 'recurrent']:
                        continue
                elif relative_dirname != release:
                    continue
                relative_filename = os.path.join(relative_dirname, filename)
                if self.is_mutation(relative_filename):
                    mutations.append(relative_filename)
        return sorted(mutations)

    def register_mutation(self, mutation):
        """Register mutation as TODO or DONE."""
        todo = self.is_new(mutation) or \
            self.is_in_development(mutation) or \
            self.is_recurrent(mutation)
        if todo:
            dest = os.path.join(self.todo_dir, mutation)
            if not os.path.isdir(os.path.dirname(dest)):
                os.makedirs(os.path.dirname(dest))
            shutil.copy2(os.path.join(self.mutations_dir, mutation), dest)

    def start_mutation(self, mutation):
        """Mark mutation from TODO to DOING.:"""
        todo = os.path.join(self.todo_dir, mutation)
        todo_dir = os.path.dirname(todo)
        doing = os.path.join(self.doing_dir, mutation)
        if not os.path.isdir(os.path.dirname(doing)):
            os.makedirs(os.path.dirname(doing))
        if self.is_recurrent(mutation):
            shutil.copy2(todo, doing)
        else:
            shutil.move(todo, doing)
        if todo_dir != self.todo_dir and not os.listdir(todo_dir):
            shutil.rmtree(todo_dir)

    def todo_releases(self):
        """Return ordered list of releases to process."""
        releases = []
        noname_release = False
        development_release = False
        for name in os.listdir(self.todo_dir):
            if os.path.isdir(os.path.join(self.todo_dir, name)):
                if name == 'development':
                    development_release = True
                elif name == 'recurrent':
                    pass
                else:
                    releases.append(name)
            else:
                noname_release = True
        releases.sort()
        if noname_release:
            releases.insert(0, '')
        if development_release:
            releases.append('development')
        return releases

    def todo_recurrent(self):
        """Return ordered list of recurrent mutations."""
        files = os.listdir(os.path.join(self.todo_dir, 'recurrent'))
        files.sort()
        return [os.path.join('recurrent', name) for name in files]

    def todo_mutations(self, release=None):
        files = []
        if release is None:
            releases = self.available_releases()
        else:
            releases = [release]
        for release in releases:
            mutations = self.available_mutations(release)
            mutations.extend(self.available_mutations('recurrent'))
            mutations = sorted(mutations, cmp=self.compare_mutations)
            files.extend(mutations)
        files = [mutation for mutation in files
                 if (not self.is_done(mutation)
                     or self.is_in_development(mutation))]
        return files

    def release(self, mutation):
        """Return release of mutation."""
        if not mutation or os.path.sep not in mutation:
            if mutation is None:
                return None
            else:
                return ''
        parts = mutation.split(os.path.sep, 1)
        return parts[0]

    def compare_mutations(self, left, right):
        left_release = self.release(left)
        right_release = self.release(right)
        release_result = self.compare_releases(left_release, right_release)
        if release_result:
            return release_result
        left_name = left if not left_release else left[len(left_release)+1:]
        right_name = right if not right_release else right[len(right_release)+1:]
        return cmp(left_name, right_name)

    def compare_releases(self, left, right):
        if left == right:
            return 0
        if left == 'recurrent' or right == 'recurrent':
            return 0
        if left == 'development':
            return 1
        if right == 'development':
            return -1
        return cmp(left, right)

    def forward_mutation(self, mutation):
        print('## FORWARD mutation "{name}"'.format(name=mutation))
        session = LocalSession()
        sh = session.sh
        result = sh.run(os.path.join(self.doing_dir, mutation))
        print(result.stdout)

    def backward_mutation(self, mutation):
        print('## BACKWARD mutation "{name}"'.format(name=mutation))
        session = LocalSession()
        sh = session.sh
        result = sh.run([
            os.path.join(self.doing_dir, mutation),
            '--backward'])
        print(result.stdout)

    def run_mutation(self, mutation):
        do_backward = (self.is_done(mutation)
                       and self.is_in_development(mutation))
        do_forward = True
        if do_backward:
            self.backward_mutation(mutation)
        if do_forward:
            self.forward_mutation(mutation)

    def success_mutation(self, mutation):
        """Mark mutation as DONE.:"""
        doing = os.path.join(self.doing_dir, mutation)
        doing_dir = os.path.dirname(doing)
        done = os.path.join(self.done_dir, mutation)
        if not os.path.isdir(os.path.dirname(done)):
            os.makedirs(os.path.dirname(done))
        if not self.is_recurrent(mutation):
            shutil.move(doing, done)
            if doing_dir != self.doing_dir and not os.listdir(doing_dir):
                shutil.rmtree(doing_dir)

    def error_mutation(self, mutation):
        """Register error and warn user."""
        print('ERROR with mutation "{name}"'.format(name=mutation))

    def run_mutations(self):
        for mutation in self.collect_mutations():
            self.register_mutation(mutation)
        for release in self.todo_releases():
            print('#### Processing release "{name}" ####'.format(name=release))
            for mutation in self.todo_mutations(release):
                self.start_mutation(mutation)
                try:
                    self.run_mutation(mutation)
                except:
                    self.error_mutation(mutation)
                else:
                    self.success_mutation(mutation)
        recurrent_dir = os.path.join(self.todo_dir, 'recurrent')
        if os.path.exists(recurrent_dir) and os.listdir(recurrent_dir):
            shutil.rmtree(recurrent_dir)
