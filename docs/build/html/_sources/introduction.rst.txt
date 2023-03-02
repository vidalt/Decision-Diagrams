Introduction
============

This package is the implementation of the `Optimal Decision Diagrams for Classification <https://arxiv.org/abs/2205.14500>`_ paper.

Decision Diagrams
-----------------

A **decision diagram** is a generalization of decision trees, where the **model topology allows merges** (i.e. two nodes 
can share a common child). Just as trees, decision diagrams can be used as a classification or regression model for data mining
and machine learning projects. In this package, only classification is implemented.

.. image:: images/intro-diagram.png
  :width: 300
  :align: center
  :alt: Decision diagram example

Advantages
~~~~~~~~~~

The model has some **advantages** over classic trees, as their **width is not bound to grow exponentially
with their depth**, which allows training deep but narrow decision diagrams without quickly facing issues of **data fragmentation**.
Moreover, **additional degrees of freedom** in their topology design permit to **express a richer set of concepts** and to **achieve better
model compression** in memory-constrained computing environments.


Exact methods for Machine Learning
----------------------------------

Despite these advantages, decision diagrams have been **more rarely used than decision trees**, as
learning them remains **inherently complex**; a decision diagram topology cannot easily be optimized
by construction and local optimization algorithms based on impurity measures. However, **recent
enhancements in global optimization techniques** for decision tree training motivate us to reevaluate
this issue. 

Indeed, optimal decision tree training through mathematical programming is becoming
practical due to the **formidable progress of hardware and mixed-integer linear programming solvers**,
which collectively led to speed-ups as high as :math:`10^{11}` between 1991 and 2015 --- most of which due to
algorithmic improvements rather than hardware.


Optimal Decision Diagrams
-------------------------

This package is the **first mixed-integer linear program (MILP) to train decision diagrams for classification**. 
The model effectively represents the decision diagram topology and the flow of the samples
within it, employing a limited number of binary variables. We also provide **efficient
heuristic search strategies** to obtain good **primal solutions** quickly.
