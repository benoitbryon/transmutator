############
Transmutator
############

Transmutator is a general purpose migration framework. 
It focuses on automating actions you perform to upgrade (or downgrade) a
product.

.. warning::

   This project is experimental. At this stage, it just describes concepts.
   Perhaps the concepts are implemented by some existing tools.

A typical migration for a web service could include:

* ask admin for confirmation
* enable maintenance page
* stop frontends
* backup data
* update configuration
* provision machines (upgrade software)
* migrate databases
* restart frontends
* run smoketests
* disable maintenance page.


****
Demo
****

Check https://transmutator.readthedocs.org/en/latest/demo.html


**********
Ressources
**********

* Documentation: https://transmutator.readthedocs.org
* PyPI: https://pypi.python.org/pypi/transmutator
* Code repository: https://github.com/benoitbryon/transmutator
* Bugtracker: https://github.com/benoitbryon/transmutator/issues
* Roadmap: https://waffle.io/benoitbryon/transmutator
* Continuous integration: https://travis-ci.org/benoitbryon/transmutator
