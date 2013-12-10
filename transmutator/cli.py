# -*- coding: utf-8 -*-
"""Shell scripts."""
import argparse
import sys

import transmutator


def transmute(arguments=sys.argv[1:], program=sys.argv[0]):
    """Run ``transmute`` shell command."""
    parser = argparse.ArgumentParser(prog=program,
                                     description="Run and manage migrations.")
    parser.add_argument('--version',
                        action='version',
                        version=transmutator.__version__)
    parser.parse_args(arguments)
    orchestrator = transmutator.Orchestrator()
    orchestrator.run_mutations()
    sys.exit(0)
