# -*- coding: utf-8 -*-
"""Shell scripts."""
import argparse
import sys

import transmutator


def transmute(arguments=sys.argv[1:], program=sys.argv[0]):
    """Run ``transmute`` shell command."""
    parser = argparse.ArgumentParser(
        prog=program,
        description="Collect and run mutations.\n"
                    "\n"
                    "Mutations are executable files that live in 'mutations'\n"
                    "folder, relative to current working directory.\n"
                    "\n"
                    "A 'var/transmutator' folder will be created to manage\n"
                    "index of mutations.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('--version',
                        action='version',
                        version=transmutator.__version__)
    parser.add_argument('--collect',
                        action='store_true',
                        default=False)
    parser.add_argument('--status',
                        action='store_true',
                        default=False)
    parsed_arguments = parser.parse_args(arguments)
    orchestrator = transmutator.Orchestrator()
    if parsed_arguments.status:
        mutation = orchestrator.latest_mutation()
        release = orchestrator.release(mutation)
        if release is '':
            release = '--- unamed release ---'
        print "RELEASE: {release}".format(release=release)
        print "MUTATION: {mutation}".format(mutation=mutation)
    elif parsed_arguments.collect:
        todo_mutations = []
        current_release = None
        for release in orchestrator.available_releases():
            mutations = orchestrator.todo_mutations(release)
            if mutations:
                print "RELEASE {release}".format(release=release)
            for mutation in mutations:
                print "--> FORWARD {mutation}".format(mutation=mutation)
        # Handle special "in-development" release.
        release = 'development'
        mutations = orchestrator.todo_mutations(release)
        if mutations:
            print "RELEASE {release}".format(release=release)
        for mutation in mutations:
            if orchestrator.is_done(mutation):
                print "<-- BACKWARD {mutation}".format(mutation=mutation)
            print "--> FORWARD {mutation}".format(mutation=mutation)

    sys.exit(0)
