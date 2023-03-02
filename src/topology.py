__author__ = "Thiago Serra"

class Topology:
    """
    Collection of structures that define a decision diagram topology.

    Instantiation of this class is intended for internal modules only.

    Parameters
    ----------
    nonterminal_width_list : list of int
        List defining the number of internal layers and their respective width 
        (i.e. node count). The list must start with a `1`, representing the root.
    data : Dataset
        Dataset instance.
    long_arcs : bool, default True
        If true, every internal node will be assigned a *long arc* to all leaves.
    verbose : bool, default False
        Flag to turn on verbose logging.
    
    Attributes
    ----------
    layer_widths : list of int
        Lists layers' widths, including the terminal layer.
    long_arcs : bool
        Indicates if topology has long arcs.
    root_node : int
        Index of root node.
    layers : int
        Total number of layers in the topology.
    nodes : list of int
        List of node indexes.
    internal_nodes : list of int
        List of internal node indexes.
    nodes_per_layer : dict of int: list of int
        For each layer, lists all of its nodes indexes.
    layer_of_node : dict of int: int
        Layer index of each node.
    has_internal_nodes : bool
        Indicates whether topology has any internal nodes (other than the root).
    node_class : dict of int: int
        Dictionary where the keys are leaf node indexes and the values are each node's
        respective class index.
    class_node : dict of int: int
        Dictionary where the keys are classes and values are each class's corresponding leaf node.
    arcs : list of tuple
        List of possible arcs in the topology. Arcs are tuples `(s,u,v)` where `s` is a side (`+` or `-`),
        `u` is the parent node and `v` is the child node.
    arcs_departing_node : dict of int: list of tuple
        For each node, lists all arcs departing it (see `arcs` attribute description).
    pos_arcs_departing_node : dict of int: list of tuple
        For each node, lists all positive arcs departing it (see `arcs` attribute description).
    neg_arcs_departing_node : dict of int: list of tuple
        For each node, lists all negative arcs departing it (see `arcs` attribute description).
    arcs_arriving_at_node : dict of int: list of tuple
        For each node, lists all arcs arriving at it (see `arcs` attribute description).
    """
    
    def __init__(self, nonterminal_width_list, data, long_arcs = True, verbose = False):
        assert nonterminal_width_list[0] == 1, "nonterminal_width_list must start with a `1`"

        self.layer_widths = nonterminal_width_list + [ len(data.classes) ]
        self.long_arcs = long_arcs
        self.root_node = 0

        self.layers = len(self.layer_widths)

        self.nodes = []
        self.internal_nodes = []
        self.nodes_per_layer = {}
        self.layer_of_node = {}
        next_node_number = self.root_node
        for l in range(self.layers):
            self.nodes_per_layer[l] = []
            for k in range(self.layer_widths[l]):
                self.nodes.append(next_node_number)
                if 0 < l < self.layers-1:
                    self.internal_nodes.append(next_node_number)
                self.nodes_per_layer[l].append(next_node_number)
                self.layer_of_node[next_node_number] = l
                next_node_number += 1
        if len(self.internal_nodes)==0:
            self.has_internal_nodes = False
        else:
            self.has_internal_nodes = True
        
        self.node_class = {}
        self.class_node = {}
        for i in range(len(data.classes)):
            self.node_class[self.nodes_per_layer[self.layers-1][i]] = data.classes[i]
            self.class_node[data.classes[i]] = self.nodes_per_layer[self.layers-1][i]
        self.nonterminal_nodes = [v for l in range(self.layers-1) for v in self.nodes_per_layer[l]]
        self.terminal_nodes = [v for v in self.nodes_per_layer[self.layers-1]]
        
        self.arcs = []
        self.arcs_departing_node = {}
        self.pos_arcs_departing_node = {}
        self.neg_arcs_departing_node = {}
        self.arcs_arriving_at_node = {}
        for v in range(next_node_number):
            self.arcs_departing_node[v] = []
            self.pos_arcs_departing_node[v] = []
            self.neg_arcs_departing_node[v] = []
            self.arcs_arriving_at_node[v] = []
    
        for l in range(self.layers-1):
            for u in self.nodes_per_layer[l]:
                for v in self.nodes_per_layer[l+1]:
                    for s in ['+','-']:
                        new_arc = (s,u,v)
                        self.arcs.append(new_arc)
                        self.arcs_departing_node[u].append(new_arc)
                        if s == '+':
                            self.pos_arcs_departing_node[u].append(new_arc)
                        else:
                            self.neg_arcs_departing_node[u].append(new_arc)
                        self.arcs_arriving_at_node[v].append(new_arc)
                        
        if long_arcs:
            for l in range(self.layers-2): # Adds arcs from all other layers to the last one
                for u in self.nodes_per_layer[l]:
                    for t in self.terminal_nodes:
                        for s in ['+','-']:
                            new_arc = (s,u,t)
                            self.arcs.append(new_arc)
                            self.arcs_departing_node[u].append(new_arc)
                            if s == '+':
                                self.pos_arcs_departing_node[u].append(new_arc)
                            else:
                                self.neg_arcs_departing_node[u].append(new_arc)
                            self.arcs_arriving_at_node[t].append(new_arc)

        if verbose:
            print("Topology:", self.layer_widths)
        
    def __str__(self):
        return self.layer_widths.__str__()