Introduction
============

For the `Optimal Decision Diagrams for Classification <https://arxiv.org/abs/2205.14500>`_ paper we chose
as **benchmark** the **54 data sets** from the UCI Machine Learning Repository [1]_ used by Bertsimas and Dunn (2017) [2]_ for 
their seminal work on **optimal decision trees**.

Finding all data sets in a **standard format** proved to be a **challenge**. 
We did find all data sets in the **ARFF format**, though with **differing categorical encodings**, **data cleaning strategies** and other details.

For this reason, we created a **data pipeline** to preprocess all ARFF files into CSV with a **standard format** of **zero-based indexing**, **one-hot encoding** 
and **no rows with missing values**, following the original benchmark from Bertsimas and Dunn (2017) [2]_.

The pipeline expects ARFF files in the ``datasets/raw`` directory and a set of corresponding transformations in ``datasets/transformations.py``.
It outputs processed CSV files in the ``datasets/processed`` directory.

Configuration
-------------

Possible transformations are implemented in the :py:mod:`operations` module. For a description of each operation, please refer to the module's documentation.

To process a data set, an ARFF file must be placed in the ``datasets/raw`` directory. Then, a corresponding configuration must be created in the 
``dataset_transformations`` dictionary of the ``datasets/transformations.py`` file, using the **same name as the ARFF file**.

The configuration has the following structure. Note that any transformation may be omitted if unnecessary.

.. code:: python

  dataset_transformations = {
    ...
    'dataset-name': {
      'replace': { 'value-to-be-replaced': 'new-value', 'other-value-to-be-replaced': 'other-new-value' },
      'zero-index': range(5),
      'one-hot-encode': [10,11],
      'drop-columns': [0,1],
      'drop-rows': [87,166,192,266,287,302],
      'drop-rows-with-values': ['?']
    },
    ...
  }

Basic usage
-----------

Process all datasets in the ``datasets/raw`` directory.

.. code:: console

  $ python3 datasets/pipeline.py all

Process a single dataset.

.. code:: console

  $ python3 datasets/pipeline.py acute-inflammations-nephritis

Some options are available for debugging, printing and overwriting previously processed data sets. Please refer to the :py:mod:`pipeline` module 
documentation for more information.

.. [1] Dua, D. and Graff, C. (2019). UCI Machine Learning Repository [http://archive.ics.uci.edu/ml]. Irvine, CA: University of California, 
  School of Information and Computer Science.

.. [2] Bertsimas, Dimitris & Dunn, Jack. (2017). Optimal classification trees. Machine Learning. 106. 10.1007/s10994-017-5633-9.