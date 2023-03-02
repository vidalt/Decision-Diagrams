Experiments
===========

The experiments on the `Optimal Decision Diagrams for Classification <https://arxiv.org/abs/2205.14500>`_ paper are based
on the output of the ``run_experiments.py`` script.

Running
-------

To run the experiments for a specific data set and seed, execute the following commands from the project root, 
within the virtual environment created during :ref:`installation <section-installation>`:

.. code:: console

  $ mkdir results
  $ python run_experiments.py [name] [seed]

where ``[name]`` is the data set name and ``[seed]`` is an integer.

The resulting CSV files will be available in the ``results`` directory.

All available datasets can be found in the ``datasets/processed`` directory. Refer to the :doc:`Data pipeline <data/introduction>` section 
for more information.


Results
-------

The experiment results are output to file ``[dataset]_[seed]_ddTrainingSolutions.csv``.

Columns
~~~~~~~

.. list-table::
    :header-rows: 1
    :widths: 10, 20

    * - Name
      - Meaning
    * - seed
      - Seed integer used for this run
    * - dataset
      - Dataset name
    * - split
      - Whether univariate or multivariate split type
    * - symBreak
      - Whether symmetry breaking constraints are active
    * - forceTree
      - Whether topology is forced to conform to a tree
    * - numSamples
      - Number of samples in the dataset
    * - numFeatures
      - Number of features in the dataset
    * - numClasses
      - Number of classes in the dataset
    * - topology
      - Topology skeleton used for this run
    * - alpha
      - Regularization parameter used for this run
    * - optimal
      - If the MIP solution is optimal
    * - accuracyStep1
      - Accuracy achieved in the first step
    * - accuracyStep2
      - Accuracy achieved in the second step
    * - objVal
      - MIP objective function value
    * - gap
      - MIP gap
    * - accValid
      - Accuracy achieved in the validation set
    * - accTest
      - Accuracy achieved in the test set
    * - durationStep1
      - Time duration of the first step
    * - durationStep2
      - Time duration of the second step
    * - bestSolutionTime
      - Time when the best solution was obtained
    * - internalNodes1
      - Number of internal nodes used in the first step solution
    * - internalNodes2
      - Number of internal nodes used in the second step solution
    * - leafNodes
      - Number of leaf nodes in the final solution
    * - upperBound1
      - MIP upper bound found in the first step
    * - upperBound2
      - MIP upper bound found in the second step
    * - lowerBound
      - MIP lower bound found in the third step
    * - fragmentationPerNode
      - % of training samples that reach each node