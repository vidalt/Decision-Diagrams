"""
Heuristic script for manual model evaluation and validation.
"""

__author__ = "Pedro Martins"

import sys
sys.path.append('./src')

import csv
import os

from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

from dataset import Dataset
from heuristic import Heuristic
from topology import Topology

def arg_parser():
    parser = ArgumentParser()
    parser.add_argument('dataset', nargs='?', help='Data set name to run heuristic. Must match the filename (without extension)\
        of a *.arff* file in the ``datasets/raw`` directory. Use ``all`` or omit to check all datasets.')
    parser.add_argument('-t', '--topologies', nargs='+', type=topology_format, default='1-2-4-4-4', help='List of topology skeletons.')
    parser.add_argument('-a', '--alphas', nargs='+', type=float, default=[0.0], help='List of alpha hyperparameters.')
    parser.add_argument('-s', '--seeds', nargs='+', type=int, default=[1], help='List of seeds.')
    return parser

def run():
    args = arg_parser().parse_args()

    check_all = args.dataset == 'all' or args.dataset == None
    datasets = list_dataset_names() if check_all else [args.dataset]

    Path("output/heuristic").mkdir(parents=True, exist_ok=True)
    filename = f'output/heuristic/{"all" if check_all else args.dataset}_{timestamp()}.csv'
    with open(filename, 'w') as check_file:
        header = ['dataset', 'seed', 'topology', 'alpha', 'training_accuracy', 'test_accuracy', 'objective_value']
        writer = csv.DictWriter(check_file, fieldnames=header)
        writer.writeheader()
        for dataset in datasets:
            for seed in args.seeds:
                for topology in args.topologies:
                    for alpha in args.alphas:
                        row = solve(dataset, seed, topology, alpha)
                        writer.writerow(row)

def topology_format(string):
    return [int(n) for n in string.split('-')]

def list_dataset_names():
    return sorted([os.path.splitext(dataset)[0] for dataset in os.listdir('datasets/processed')])

def timestamp():
    return int(round(datetime.now().timestamp()))

def solve(dataset, seed, topology_desc, alpha):
    print(dataset, seed, topology_desc, alpha)
    data = Dataset(f'datasets/processed/{dataset}.csv', train_validation_test_split=[0.5, 0.25, 0.25], seed=seed, verbose=False)
    topology = Topology(topology_desc, data, long_arcs=True, verbose=False)
    heuristic = Heuristic(data, topology, verbose=False, alpha=alpha)
    solution = heuristic.solution
    return {
        'dataset': dataset,
        'seed': seed,
        'topology': topology_desc,
        'alpha': alpha,
        'training_accuracy': solution.training_accuracy(),
        'test_accuracy': solution.test_accuracy(),
        'objective_value': solution.objective_value(alpha, len(topology.internal_nodes))
    }

if __name__ == '__main__':
    run()