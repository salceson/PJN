# coding: utf-8
from collections import Counter
from math import fsum, sqrt

import networkx as nx
from networkx.drawing.nx_agraph import view_pygraphviz

__author__ = "Michał Ciołczyk"


class Graph(object):
    def __init__(self):
        self.matrix = Counter()
        self.vertices = set()

    def add_edge(self, from_vertex, to_vertex):
        self.vertices.add(from_vertex)
        self.vertices.add(to_vertex)
        self.matrix[(from_vertex, to_vertex)] += 1

    def draw(self, filename):
        graph = nx.DiGraph(name="Text graph")
        graph.add_nodes_from(self.vertices)
        for (from_vertex, to_vertex), weight in self.matrix.items():
            graph.add_edge(from_vertex, to_vertex, {"weight": weight})
        with open(filename, 'wb') as f:
            try:
                view_pygraphviz(graph, path=f, edgelabel="weight")
            except KeyError:  # This occurs because NxNetwork wants to open generated file
                pass

    def get_metric(self, other):
        vec1 = {k: self.matrix[k] for k in self.matrix}
        vec2 = {k: other.matrix[k] for k in other.matrix}
        keys = set(vec1.keys()) & set(vec2.keys())
        norm1 = sqrt(fsum([v * v for v in vec1.values()]))
        norm2 = sqrt(fsum([v * v for v in vec2.values()]))
        try:
            return 1. - fsum([vec1[key] * vec2[key] for key in keys]) / (norm1 * norm2)
        except ZeroDivisionError:
            return 1


def text_to_graph(text, k):
    g = Graph()
    # The below is working until the window is too small
    for n_gram in zip(*(text[i:] for i in range(k + 1))):
        for word in n_gram:
            g.add_edge(n_gram[0], word)
    # The below is working after the window is too small
    for i in range(k):
        i = len(text) - i - 1
        n_gram = text[i:]
        for word in n_gram:
            g.add_edge(n_gram[0], word)
    return g


if __name__ == "__main__":
    g = text_to_graph("test troll test troll troll".split(), 2)
    g.draw('out.png')
