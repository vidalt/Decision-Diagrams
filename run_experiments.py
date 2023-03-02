"""
Experiments script for the original paper.
"""

__author__ = "Alexandre Florio, Maximilian Schiffer, Thiago Serra, and Thibaut Vidal"

import sys
sys.path.append('./src')

import csv
import numpy as np
from timeit import default_timer as timer

from dataset import Dataset
from topology import Topology
from heuristic import Heuristic
from optimizer import Optimizer

def solve_heuristic(data, topology, alpha):
    best_heur_sol = Heuristic(data, topology, verbose=False, randomize_splits=True,
            feature_subset_ratio=1.0)
    best_obj_value = best_heur_sol.solution.objective_value(alpha, len(topology.internal_nodes))
    start = timer()
    elapsed = 0
    run = 0
    while elapsed < 60:
        run += 1
        rnd = np.random.uniform(low=0.5, high=1.0)
        heur_sol = Heuristic(data, topology, verbose=False, randomize_splits=True,
                feature_subset_ratio=rnd, alpha=alpha)
        obj_value = heur_sol.solution.objective_value(alpha,
                top_internal_nodes=len(topology.internal_nodes))
        #print("heuristic: run:", run, " obj. value:", obj_value)
        if obj_value < best_obj_value:
            best_obj_value = obj_value
            best_heur_sol = heur_sol
        elapsed = timer() - start
        #print("elapsed:", elapsed)
    print("heuristic: best obj. value:", best_obj_value)
    return best_heur_sol

def run_single_experiment(train_data, topologies, alphaset, uni_split, dd_train_writer, ss, dn,
        split, sym_break, force_tree):
    data = train_data
    for t in topologies:
        print("topology (train):" + str(t))
        ddAccuracyBin = []
        ddNumInternalNodesBin = []
        for alpha in alphaset:
            topology = Topology(t, data, long_arcs=True, verbose=True)
            startStep1 = timer()
            heuristic = solve_heuristic(data, topology, alpha)
            durationStep1 = timer() - startStep1
            accuracyStep1 = heuristic.solution.training_accuracy()
            internalNodes1 = heuristic.solution.count_internal_nodes()
            upperBound1 = heuristic.solution.objective_value(alpha, len(topology.internal_nodes))
            start = timer()
            optimized = Optimizer(data, topology, alpha=alpha, initial_solution=heuristic.solution, 
                univariate_split=uni_split, sym_break=sym_break, force_tree=force_tree)
            durationStep2 = timer() - start
            current_solution = optimized.solution
            optimized.topology = t
            internalNodes2 = current_solution.count_internal_nodes()
            upperBound2 = current_solution.objective_value(alpha, len(topology.internal_nodes))
            lowerBound = current_solution.obj_lb
            leafNodes = current_solution.count_class_nodes()
            dd_train_writer.writerow([str(ss), dn, split, sym_break, force_tree, str(data.n),
                    str(data.p),str(len(data.classes)),str(t),str(alpha),current_solution.optimal,
                    str(accuracyStep1),str(current_solution.training_accuracy()),
                    str(current_solution.obj_val),str(current_solution.mip_gap),
                    str(current_solution.validation_accuracy()),
                    str(current_solution.test_accuracy()),str(durationStep1),str(durationStep2),
                    str(current_solution.best_solution_time),str(internalNodes1),
                    str(internalNodes2),str(leafNodes),str(upperBound1),str(upperBound2),
                    str(lowerBound),str(optimized.solution.fragmentation_per_node())])
            ddAccuracyBin.append(current_solution.validation_accuracy())
            ddNumInternalNodesBin.append(internalNodes2)

def run_all_experiments(dn, ss):
    # topologies for ODDs
    topologies = [ [1,2,4,8], [1,2,4,4,4], [1,2,3,3,3,3], [1,2,2,2,2,2,2,2] ]
    alphaset = [0.01, 0.1, 0.2, 0.5, 1]

    ddTrainingFileName = "results/{}_{}_ddTrainingSolutions.csv".format(dn, ss)

    with open(ddTrainingFileName, "w") as ddTrainingFile:
        dd_train_writer = csv.writer(ddTrainingFile, delimiter=";")

        csv_header = ("seed","dataset","split","symBreak","forceTree","numSamples","numFeatures",
                "numClasses","topology","alpha","optimal","accuracyStep1","accuracyStep2","objVal",
                "gap","accValid","accTest","durationStep1","durationStep2","bestSolutionTime",
                "internalNodes1","internalNodes2","leafNodes","upperBound1","upperBound2",
                "lowerBound","fragmentationPerNode")
        dd_train_writer.writerow(csv_header)

        print("dataset:", dn)

        train_data = Dataset("./datasets/processed/"+dn+".csv",
                train_validation_test_split=[0.5, 0.25, 0.25], verbose=True, seed=ss)

        # experiments for ODDs
        for split in ["multi", "uni"]:
            print("split:", split)
            uni_split = split == "uni"
            for sym_break in (True,):
                print("sym_break:", sym_break)
                run_single_experiment(train_data, topologies, alphaset, uni_split, dd_train_writer,
                        ss, dn, split, sym_break, False)

        # experiments for ODTs
        print("tree topology")
        topologies = [ [1,2,4,8] ]
        for split in ["multi", "uni"]:
            print("split:", split)
            uni_split = split == "uni"
            for sym_break in (True,):
                print("sym_break:", sym_break)
                run_single_experiment(train_data, topologies, alphaset, uni_split, dd_train_writer,
                        ss, dn, split, sym_break, True)

run_all_experiments(sys.argv[1], sys.argv[2])

