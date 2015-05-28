######################
Let's try transmutator
######################

``demo/mutations`` folder in `code repository`_ contains sample mutations to
illustrate usage of `transmutator`.

.. code:: sh

   # Deploy development environment...
   # Inside a virtualenv if you like ;)
   git clone git@github.com:benoitbryon/transmutator.git
   cd transmutator
   make develop

   # Let's run demo mutations.
   cd demo/
   transmute  # Collect and run stuff in "mutations/" folder.

   # Just try to run the mutations again.
   transmute  # Run new, recurrent or in-development mutations.


.. rubric:: Notes & references

.. target-notes::

.. _`code repository`: https://github.com/benoitbryon/transmutator/
