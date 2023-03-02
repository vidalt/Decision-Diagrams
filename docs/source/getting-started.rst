Getting started
===============

Requirements
------------

This package requires Python 3+. The :py:mod:`optimizer` requires the **Gurobi** solver and the **gurobipy** package to be installed.

.. list-table::
    :header-rows: 1
    :widths: 10, 10

    * - Dependency
      - Versions
    * - Python
      - 3+
    * - Gurobi
      - 9.0+
    * - gurobipy
      - Compatible with your Gurobi version

Gurobi
~~~~~~

`Gurobi <https://www.gurobi.com/>`_ is a solver for mathematical optimization, including mixed-integer linear programming (MILP). 
It has a `free academic license <https://www.gurobi.com/academia/academic-program-and-licenses/>`_.

.. _section-installation:

Installation
------------

First, clone the repository.

.. code:: console

  $ git clone https://https://github.com/pedrosbmartins/optimal-decision-graphs.git

Then, create and activate a python environment (for instance, using `virtualenv <https://virtualenv.pypa.io/en/latest/>`_).

.. code:: console

  $ virtualenv -p python3 env
  $ source env/bin/activate

Finally, install required packages.

.. code:: console

  $ pip install -r requirements.txt
  $ python -m pip install -i https://pypi.gurobi.com gurobipy


Basic usage
-----------

Import components.

.. code:: python

  from dataset import Dataset
  from topology import Topology
  from heuristic import Heuristic
  from optimizer import Optimizer
  from visualizer import Visualizer

Setup desired dataset, topology skeleton and alpha hyperparameter.

.. code:: python

  dataset = "path/to/dataset.csv"
  skeleton = [1,2,4,4,4]
  alpha = 0.1

  data = Dataset(dataset, train_validation_test_split=[0.5, 0.25, 0.25])
  topology = Topology(skeleton, data)

Run heuristic to generate a first solution.

.. code:: python

  heuristic = Heuristic(data, topology, alpha=alpha)
  print('Heuristic', heuristic.solution.training_accuracy(), heuristic.solution.test_accuracy())

Run optimizer using the heuristic as initial solution, then generate a Graphviz visualization.

.. code:: python

  optimized = Optimizer(data, topology, alpha=alpha, initial_solution=heuristic.solution)
  print('Optimized', optimized.solution.training_accuracy(), optimized.solution.test_accuracy())

  optimized_viz = Visualizer(data, optimized.solution)
  optimized_viz.view()


Issues
------

If you encounter any issues, please open a ticket on `GitHub <https://https://github.com/pedrosbmartins/optimal-decision-graphs>`_.