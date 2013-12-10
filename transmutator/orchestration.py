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

    def is_mutation(self, mutation):
        """Return ``True`` if ``mutation`` is path to an executable file."""
        return mutation.endswith('.py')

    def collect_mutations(self):
        """Return a list of all available mutations, whatever their status."""
        files = os.listdir(self.mutations_dir)
        files.sort()
        files = [os.path.join(self.mutations_dir, f)
                 for f in files
                 if self.is_mutation(f)]
        return files

    def register_mutation(self, mutation):
        """Register mutation as TODO or DONE."""
        basename = os.path.basename(mutation)
        if os.path.isfile(os.path.join(self.done_dir, basename)):
            pass
        else:
            shutil.copy2(mutation, os.path.join(self.todo_dir, basename))

    def start_mutation(self, mutation):
        """Mark mutation from TODO to DOING.:"""
        shutil.move(
            os.path.join(self.todo_dir, mutation),
            os.path.join(self.doing_dir, mutation),
        )

    def todo_mutations(self):
        mutations = os.listdir(self.todo_dir)
        mutations.sort()
        return mutations

    def run_mutation(self, mutation):
        session = LocalSession()
        sh = session.sh
        result = sh.run(os.path.join(self.doing_dir, mutation))
        print(result.stdout)

    def success_mutation(self, mutation):
        """Mark mutation as DONE.:"""
        shutil.move(
            os.path.join(self.doing_dir, mutation),
            os.path.join(self.done_dir, mutation),
        )

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
