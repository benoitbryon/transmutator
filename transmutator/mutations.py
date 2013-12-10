import argparse
import sys


class AtomicMutation(object):
    """Base class for mutations that focus on one thing."""
    def __init__(self, action="forward"):
        self.action = action

    def __call__(self, arguments=sys.argv[1:], program=sys.argv[0]):
        parser = argparse.ArgumentParser(prog=program,
                                         description=self.__class__.__doc__)
        self.arguments = parser.parse_args(arguments)
        action = getattr(self, self.action)
        try:
            action()
        except:
            raise
        sys.exit(0)

    def forward(self):
        """Upgrade."""
        raise NotImplementedError()

    def backward(self):
        """Downgrade."""
        raise NotImplementedError()

    def forward_smoketest(self):
        """Quickly assert that forward expectations are met."""

    def forward_diagnostic(self):
        """Check forward expectations and produce detailed diagnostic."""
