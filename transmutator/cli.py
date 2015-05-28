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
    parser.parse_args(arguments)
    orchestrator = transmutator.Orchestrator()
    orchestrator.run_mutations()
    sys.exit(0)
