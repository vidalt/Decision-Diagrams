__author__ = "Pedro Martins and Thibaut Vidal"

import numpy as np
from graphviz import Digraph

class Visualizer:
    """
    Graphical representation of decision diagrams.

    Parameters
    ----------
    data : Dataset
        Dataset instance used to build the decision diagram.
    solution : Solution
        Solution instance to visualize.
    feature_names : list of str, default None
        Optional list of feature names. Used to display univariate splits.
    samples_per_node : dict of int: list, default None
        Optional dictionary listing samples for each node. If not provided, will be
        calculated from `solution`. Used to display sample count per node.
    """
    
    def __init__(self, data, solution, feature_names=None, samples_per_node=None):
        self.solution = solution
        self.topology = solution.topology
        self.data = data
        self.feature_names = feature_names
        self.fragmentation_per_node = self.solution.fragmentation_per_node()
        self.samples_per_node = samples_per_node
        self.colors = self._color_brew(len(data.classes))
        self._calculate_samples_and_class_distribution()

    def view(self, filled=True, fragmentation_only=False):
        """
        Generate the decision diagram as a Graphviz Digraph.
        
        By default, each node displays its index, split decision (*note:* this currently 
        only works for univariate splits), sample count and class distribution.

        Parameters
        ----------
        filled : bool, default True
            If `filled` is True, nodes are colored according to its predominant class, else
            nodes have white background.
        fragmentation_only : bool, default False
            If `fragmentation_only` is True, each node displays only the proportion of samples
            that reaches it, and is colored by this same metric.
        
        Returns
        -------
        diagram
            A Graphviz Digraph representing the decision diagram.
        """
        graph = Digraph()
        graph.attr(bgcolor='transparent')
        graph.attr('node', shape='box', ordering='out')
        edges = []
        filled = filled or fragmentation_only
        for l in range(self.topology.layers):
            for v in self.topology.nodes_per_layer[l]:
                if not v in self.solution.used_nodes:
                    continue
                if l < self.topology.layers-1:
                    if v in self.solution.node_positive_arc:
                        pos_arc, pos_label = self._nonterminal_node_positive_arc(v)
                        edges.append([str(v), pos_arc, pos_label])
                    if v in self.solution.node_negative_arc:
                        neg_arc, neg_label = self._nonterminal_node_negative_arc(v)
                        edges.append([str(v), neg_arc, neg_label])
                    content = self._nonterminal_node_content(v, fragmentation_only)
                    bgcolor = self._nonterminal_node_bgcolor(v, fragmentation_only)
                    graph.node(str(v), content, style='filled', fillcolor=bgcolor, color='#bbbbbb')
                elif l == self.topology.layers-1:
                    class_color = self.colors[list(self.data.classes).index(int(self.solution.node_class[v]))]
                    content = self._terminal_node_content(v, fragmentation_only)
                    color = self._rgba_to_hex(class_color) if filled else "#ffffff"
                    if fragmentation_only:
                        alpha = int(self.fragmentation_per_node[v] * 125)
                        color = self._rgba_to_hex([0,0,255] + [alpha])
                    graph.node(str(v), content, style='filled', fillcolor=color)
        for edge in edges:
            [node, child_node, label] = edge
            graph.edge(node, child_node, label, arrowsize='.5', color="#bbbbbb")
        return graph

    def _nonterminal_node_bgcolor(self, node, fragmentation_only):
        if fragmentation_only:
            return self._fragmentation_node_color(node)
        return '#f8f8f8'

    def _fragmentation_node_color(self, node):
        alpha = int(self.fragmentation_per_node[node] * 125)
        return self._rgba_to_hex([0,0,255,alpha])

    def _nonterminal_node_content(self, node, fragmentation_only):
        if fragmentation_only:
            return self._fragmentation_label(node)
        color = self._nonterminal_node_color(node, self.colors.copy())
        return f"""<
            <table border="0">
                <tr><td colspan="3" bgcolor="{color}"></td></tr>
                <tr><td colspan="1" bgcolor="{color}">{node}</td><td colspan="2">{self._split_label(node)}</td></tr>
                <tr><td colspan="1">{len(self.samples_per_node[node])}</td><td colspan="2">{str(self.class_distrib_per_node[node])}</td></tr>
            </table>
        >"""

    def _nonterminal_node_color(self, node, colors):
        class_distrib = self.class_distrib_per_node[node]
        argmax = np.argwhere(class_distrib == np.amax(class_distrib)).flatten()
        if len(argmax) > 1:
            return "#ffffffff"
        class_color = colors[argmax[0]]
        max_sample_count = class_distrib[argmax[0]]
        sample_count_sum = np.sum(class_distrib)
        if sample_count_sum == max_sample_count:
            return self._rgba_to_hex(class_color)
        alpha = int(0.5 * 255 * (max_sample_count / sample_count_sum))
        return self._rgba_to_hex(class_color[:3] + [alpha])

    def _split_label(self, node):
        if node not in self.solution.node_hyperplane:
            return '--'
        feature_index = np.argmax(self.solution.node_hyperplane[node])
        if self.feature_names is None:
            feature = '<FONT POINT-SIZE="10">X<sub>{}</sub></FONT> '.format(feature_index)
        else:
            feature = self.feature_names[feature_index]
        return '{} ≥ {:0.1f}'.format(feature, self.solution.node_intercept[node])

    def _nonterminal_node_positive_arc(self, node):
        pos_arc = self.solution.node_positive_arc[node]
        pos_label = 'True' if node == self.topology.root_node else None
        return str(pos_arc), pos_label

    def _nonterminal_node_negative_arc(self, node):
        neg_arc = self.solution.node_negative_arc[node]
        neg_label = 'False' if node == self.topology.root_node else None
        return str(neg_arc), neg_label
    
    def _terminal_node_content(self, node, fragmentation_only):
        if fragmentation_only:
            return self._fragmentation_label(node)
        return f"""<
            <table border="0">
                <tr><td colspan="1" bgcolor="#00000033">{node}</td><td colspan="2">{f'class {str(self.solution.node_class[node])}'}</td></tr>
                <tr><td colspan="1">{len(self.samples_per_node[node])}</td><td colspan="2">{str(self.class_distrib_per_node[node])}</td></tr>
            </table>
        >"""

    def _fragmentation_label(self, node):
        return "{:0.1f}%".format(self.fragmentation_per_node[node]*100)

    def _calculate_samples_and_class_distribution(self):
        n = self.data.train_n
        Y = self.data.train_Y
        classes = self.data.classes

        if self.samples_per_node is not None:
            self.class_distrib_per_node = {}
            for v in self.topology.nodes:
                self.class_distrib_per_node[v] = [len([i for i in self.samples_per_node[v] if Y[i] == k]) for k in classes]
        else:
            self.samples_per_node = {}
            self.samples_per_node[self.topology.root_node] = [i for i in range(n)]

            self.class_distrib_per_node = {}
            self.class_distrib_per_node[self.topology.root_node] = [len([i for i in range(n) if Y[i] == k]) for k in classes]

            for l in range(1, self.topology.layers):
                for v in self.topology.nodes_per_layer[l]:
                    self.samples_per_node[v] = []
                    self.class_distrib_per_node[v] = [0 for i in classes]
                    
            for l in range(self.topology.layers-1):
                for v in self.topology.nodes_per_layer[l]:
                    if v not in self.solution.used_nodes: continue
                    for i in self.samples_per_node[v]:
                        if v not in self.solution.node_hyperplane: continue
                        lhs  = sum([x*y for x,y in zip(self.solution.node_hyperplane[v],self.data.train_X[i])])
                        if lhs >= self.solution.node_intercept[v]:
                            if v not in self.solution.node_positive_arc: continue
                            u = self.solution.node_positive_arc[v]
                        else:
                            if v not in self.solution.node_negative_arc: continue
                            u = self.solution.node_negative_arc[v]
                        self.samples_per_node[u].append(i)
                        self.class_distrib_per_node[u][list(classes).index(int(Y[i]))] += 1

    def _color_brew(self, n):
        """From sklearn.tree.
        Generate n colors with equally spaced hues.
        Parameters
        ----------
        n : int
            The number of colors required.
        Returns
        -------
        color_list : list, length n
            List of n tuples of form (R, G, B) being the components of each color.
        """
        color_list = []

        # Initialize saturation & value; calculate chroma & value shift
        s, v = 0.75, 0.9
        c = s * v
        m = v - c

        for h in np.arange(25, 385, 360. / n).astype(int):
            # Calculate some intermediate values
            h_bar = h / 60.
            x = c * (1 - abs((h_bar % 2) - 1))
            # Initialize RGB with same hue & chroma as our color
            rgb = [(c, x, 0),
                (x, c, 0),
                (0, c, x),
                (0, x, c),
                (x, 0, c),
                (c, 0, x),
                (c, x, 0)]
            r, g, b = rgb[int(h_bar)]
            # Shift the initial RGB values to match value and store
            rgba = [(int(255 * (r + m))),
                (int(255 * (g + m))),
                (int(255 * (b + m))),
                255]
            color_list.append(rgba)

        return color_list

    def _rgba_to_hex(self, rgba):
        return '#{:02x}{:02x}{:02x}{:02x}'.format(*rgba)
