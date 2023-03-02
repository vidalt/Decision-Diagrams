"""
Automated tests for the Heuristic class.
"""

__author__ = "Pedro Martins"

import pytest

@pytest.mark.integration
def test_tree_sample_count_consistency(tree_heuristic_outputs):
    for heuristic,topology in tree_heuristic_outputs:
        samples_per_layer = [sum([len(heuristic.node_samples[v]) for v in topology.nodes_per_layer[l]]) for l in range(topology.layers)]
        assert samples_per_layer[0] == samples_per_layer[-1]

@pytest.mark.integration
def test_diagram_sample_count_consistency(diagram_heuristic_outputs):
    for heuristic,topology in diagram_heuristic_outputs:
        samples_per_layer = [sum([len(heuristic.node_samples[v]) for v in topology.nodes_per_layer[l]]) for l in range(topology.layers)]
        assert samples_per_layer[0] == samples_per_layer[-1]
