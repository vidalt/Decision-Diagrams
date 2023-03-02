"""
Module for configuring automated tests.
"""

__author__ = "Pedro Martins"

import pytest

from src.dataset import Dataset
from src.topology import Topology
from src.heuristic import Heuristic

def pytest_addoption(parser):
    parser.addoption("--seed", action="store", default=1, help="set testing seed")

@pytest.fixture(scope="module")
def seed(request):
    return request.config.getoption("--seed")

@pytest.fixture(scope="module")
def diagram_heuristic_outputs(seed):
    return [solve_heuristic(seed, dataset, diagram_topology, alpha) for dataset in datasets for alpha in alphas]

@pytest.fixture(scope="module")
def tree_heuristic_outputs(seed):
    return [solve_heuristic(seed, dataset, tree_topology, alpha) for dataset in datasets for alpha in alphas]

def solve_heuristic(seed, dataset, topology, alpha):
    data = Dataset(f"datasets/processed/{dataset}.csv", train_validation_test_split=[0.5, 0.25, 0.25], seed=seed)
    topology = Topology(tree_topology, data, long_arcs=True)
    heuristic = Heuristic(data, topology, verbose=False, alpha=alpha)
    return (heuristic, topology)

diagram_topology = [1,2,4,4,4]
tree_topology = [1,2,4,8]
alphas = [0.0, 0.5, 1.0]

datasets = [
    "acute-inflammations-nephritis",
    "acute-inflammations-urinary",
    "balance-scale",
    "banknote-authentication",
    "blood-transfusion-service",
    "breast-cancer-diagnostic",
    "breast-cancer-prognostic",
    "breast-cancer-wisconsin",
    "car-evaluation",
    "chess-kr-vs-kp",
    "climate-simulation-crashes",
    "congressional-voting",
    "connectionist-mines-vs-rocks",
    "connectionist-vowel",
    "contraceptive-method-choice",
    "credit-approval",
    "cylinder-bands",
    "dermatology",
    "echocardiogram",
    "fertility-diagnosis",
    "habermans-survival",
    "hayes-roth",
    "heart-disease-cleveland",
    "hepatitis",
    "image-segmentation",
    "indian-liver-patient",
    "ionosphere",
    "iris",
    "mammographic-mass",
    "monks1",
    "monks2",
    "monks3",
    "optical-recognition",
    "ozone-eighthr",
    "ozone-onehr",
    "parkinsons",
    "pima-indians-diabetes",
    "planning-relax",
    "qsar-biodegradation",
    "seeds",
    "seismic-bumps",
    "soybean-small",
    "spambase",
    "spectf-heart",
    "spect-heart",
    "statlog-german-credit",
    "statlog-landsat-satellite",
    "teaching-assistant-evaluation",
    "thoracic-surgery",
    "thyroid-ann",
    "thyroid-new",
    "tic-tac-toe",
    "wall-following-robot-2",
    "wine"
]
