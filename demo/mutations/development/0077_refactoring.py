#!/usr/bin/env python
import transmutator


class RefactoringMutation(transmutator.AtomicMutation):
    def forward(self):
        print("Apply some refactoring forward! Add column FOO.")

    def backward(self):
        print("Rollback some refactoring! Remove column FOO.")


if __name__ == '__main__':
    mutation = RefactoringMutation()
    mutation()
