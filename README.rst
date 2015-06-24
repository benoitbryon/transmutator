############
transmutator
############

`Transmutator` is a **general purpose migration framework**.
It focuses on automating actions to upgrade (or downgrade) a product.

General purpose
  Perhaps you heard about tools such as `Django migrations`_. They are
  migrations restricted to the scope of `Django` models and related database.
  `Transmutator` is not limited to a language, framework or database scope:
  it runs executables, whatever the language, for the purpose you want.

Migration
  Given a product in a given state (call it state 1.0), a "migration" brings
  the product to another state (call it state 2.0).
  In the semantic field of workflows, we would have called it a "transition".
  In the semantic field of end-user software, we would have called it an
  "upgrade" or "downgrade".

Framework
  `transmutator`'s primary purpose is to run migrations. But it also provides
  a basic toolkit to ease the development of migration scripts.

****
Demo
****

Check https://transmutator.readthedocs.org/en/latest/demo.html


******************
Development status
******************

**Today**, `transmutator` is experimental. First goal is to have a simple tool
that runs migration scripts in a predictable, repeatable and easy way. Let's
focus on a basic but consistent set of features.

**Later**, `transmutator` (or related projects) may deal with queues,
interactions, workflows, parallelization, monitoring, web UI...

Help is welcome to implement a nice tool today, and to make it better tomorrow!


**********
Ressources
**********

* Documentation: https://transmutator.readthedocs.org
* PyPI: https://pypi.python.org/pypi/transmutator
* Code repository: https://github.com/benoitbryon/transmutator
* Bugtracker: https://github.com/benoitbryon/transmutator/issues
* Roadmap: https://waffle.io/benoitbryon/transmutator
* Continuous integration: https://travis-ci.org/benoitbryon/transmutator

.. _`Django migrations`:
   https://docs.djangoproject.com/en/1.8/topics/migrations/
