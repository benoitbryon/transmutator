import os
import shutil

from xal.session.local import LocalSession


class Orchestrator(object):
    def __init__(self):
        root_dir = os.path.abspath(os.getcwd())
        self.mutations_dir = os.path.join(root_dir, 'mutations')
        self.working_dir = os.path.join(root_dir, 'var', 'transmutator')
        if not os.path.isdir(self.working_dir):
            os.makedirs(self.working_dir)
        self.todo_dir = os.path.join(self.working_dir, 'todo')
        if not os.path.isdir(self.todo_dir):
            os.makedirs(self.todo_dir)
        self.doing_dir = os.path.join(self.working_dir, 'doing')
        if not os.path.isdir(self.doing_dir):
            os.makedirs(self.doing_dir)
        self.done_dir = os.path.join(self.working_dir, 'done')
        if not os.path.isdir(self.done_dir):
            os.makedirs(self.done_dir)

    def mutation_sourcefile(self, mutation):
        """Return absolute filename to mutation."""
        return os.path.join(self.mutations_dir, mutation)

    def is_mutation(self, mutation):
        """Return ``True`` if ``mutation`` is path to an executable file."""
        return os.access(self.mutation_sourcefile(mutation), os.X_OK)

    def is_done(self, mutation):
        """Return ``True`` if ``mutation`` has already been performed."""
        return os.path.isfile(os.path.join(self.done_dir, mutation))

    def is_new(self, mutation):
        """Return ``True`` if ``mutation`` has not been performed yet."""
        return not os.path.exists(os.path.join(self.done_dir, mutation))

    def is_recurrent(self, mutation):
        """Return ``True`` if ``mutation`` has to be performed on every run.

        On forward, recurrent mutations are not skipped, they go forward.

        """
        return mutation.startswith('recurrent/')

    def is_in_development(self, mutation):
        """Return ``True`` if ``mutation`` is in development.

        On forward, in-development mutations go backward and forward.

        """
        return mutation.startswith('development')

    def collect_mutations(self):
        """Return a list of all available mutations, whatever their status."""
        for (dirpath, dirnames, filenames) in os.walk(self.mutations_dir):
            for filename in filenames:
                relative_dirname = dirpath[len(self.mutations_dir):]
                relative_dirname = relative_dirname.lstrip(os.path.sep)
                relative_filename = os.path.join(relative_dirname, filename)
                yield relative_filename

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
        shutil.move(todo, doing)
        if todo_dir != self.todo_dir and not os.listdir(todo_dir):
            shutil.rmtree(todo_dir)

    def todo_mutations(self):
        files = []
        for (dirpath, dirnames, filenames) in os.walk(self.todo_dir):
            for filename in filenames:
                relative_dirname = dirpath[len(self.todo_dir):]
                relative_dirname = relative_dirname.lstrip(os.path.sep)
                relative_filename = os.path.join(relative_dirname, filename)
                files.append((filename, relative_filename))
        files.sort()
        files = [relative_filename for f, relative_filename in files]
        return files

    def forward_mutation(self, mutation):
        print('FORWARD mutation "{name}"'.format(name=mutation))
        session = LocalSession()
        sh = session.sh
        result = sh.run(os.path.join(self.doing_dir, mutation))
        print(result.stdout)

    def backward_mutation(self, mutation):
        print('BACKWARD mutation "{name}"'.format(name=mutation))
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
        shutil.move(doing, done)
        if doing_dir != self.doing_dir and not os.listdir(doing_dir):
            shutil.rmtree(doing_dir)

    def error_mutation(self, mutation):
        """Register error and warn user."""
        print('ERROR with mutation "{name}"'.format(name=mutation))

    def run_mutations(self):
        for mutation in self.collect_mutations():
            self.register_mutation(mutation)
        for mutation in self.todo_mutations():
            self.start_mutation(mutation)
            try:
                self.run_mutation(mutation)
            except:
                self.error_mutation(mutation)
            else:
                self.success_mutation(mutation)
