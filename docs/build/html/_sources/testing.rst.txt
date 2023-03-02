Testing
=======


Heuristic
---------

The heuristic implementation has a set of tests to ensure changes do not introduce bugs. There are two types of tests,
automated tests for model verification and manual model evaluation and validation.


Automated tests
~~~~~~~~~~~~~~~

Tests for the heuristic are implemented in ``tests/test_heuristic.py``.

To run this tests, first install ``pytest`` within the virtual environment created during :ref:`installation <section-installation>`.

.. code:: console

  $ source env/bin/activate
  $ pip install pytest

Then run the tests from the project root:

.. code:: console

  $ pytest --seed=1

where ``seed`` is an integer.

.. warning::

  The automated tests runs for *all* data sets, two topology skeletons and three alpha hyperparameters. For this reason, they can be slow.
  For writing new tests, it is recommended to temporarily setup fewer data sets and configurations in the ``tests/conftest.py`` file.


Manual evaluation and validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``run_heuristic.py`` script allows the heuristic to be run for any combination of data set, seed, topology and alpha hyperparameter.
It reports training accuracy, test accuracy and objective value.

For model evaluation and validation, we have a **GitHub Action** setup that is triggered whenever the ``src/heuristic.py`` file is modified. 
It runs the script for *all* data set and a number of seed, topology and alpha configurations. Results are saved to the ``output/heuristic``
directory.

These outputs can be evaluated for overall impacts of each commit on accuracy, generalization and objective value.

run_heuristic.py script
~~~~~~~~~~~~~~~~~~~~~~~

.. argparse::
  :module: run_heuristic
  :func: arg_parser
  :prog: run_heuristic
