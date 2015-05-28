#!/usr/bin/env python
"""This mutation shows how ``transmutator`` can be used as a Python library."""
import transmutator


class HelloWorldMutation(transmutator.AtomicMutation):
    """`transmutator` provides base classes to implement mutations."""
    def forward(self):
        """Forward: say hello using Python."""
        print("Hello Python world!")

    def backward(self):
        """Backward: say goodbye using Python."""
        print("Goodbye Python world!")


if __name__ == '__main__':  # Python mutations are scripts, just like sh ones.
    mutation = HelloWorldMutation()  # Mutations may be initialized with conf.
    mutation()  # Mutation instances are callables.
