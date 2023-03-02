# Optimal Decision Diagrams

## Description

This repository implements the code for the paper [Optimal Decision Diagrams for Classification](https://arxiv.org/abs/2205.14500), presented and published at AAAI 2023.

## Requirements

This project requires Python3 and the [Gurobi solver](https://www.gurobi.com/), which has a [free academic license](https://www.gurobi.com/academia/academic-program-and-licenses/) available.

## Documentation

Full documentation is available in `docs/build/html/index.html`, including information about the paper experiments.

## Getting started

### Installation

First, clone the repository.

```
$ git clone https://https://github.com/pedrosbmartins/optimal-decision-graphs.git
```

Then, create and activate a python environment (for instance, using [virtualenv](https://virtualenv.pypa.io/en/latest/)).

```
$ virtualenv -p python3 env
$ source env/bin/activate
```

Finally, install required packages.

```
$ pip install -r requirements.txt
$ python -m pip install -i https://pypi.gurobi.com gurobipy
```

### Basic usage

> Note: make sure the `src` directory is present in your `sys.path`.

```
from dataset import Dataset
from topology import Topology
from heuristic import Heuristic
from optimizer import Optimizer
from visualizer import Visualizer

dataset = "datasets/processed/[dataset name].csv"
skeleton = [1,2,4,4,4]
alpha = 0.1

data = Dataset(dataset, train_validation_test_split=[0.5, 0.25, 0.25])
topology = Topology(skeleton, data)

heuristic = Heuristic(data, topology, alpha=alpha)
print('Heuristic', heuristic.solution.training_accuracy(), heuristic.solution.test_accuracy())

optimized = Optimizer(data, topology, alpha=alpha, initial_solution=heuristic.solution)
print('Optimized', optimized.solution.training_accuracy(), optimized.solution.test_accuracy())

optimized_viz = Visualizer(data, optimized.solution)
optimized_viz.view()
```

## Issues

If you encounter any issues, please open an issue ticket.
