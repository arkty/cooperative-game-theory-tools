import networkx as nx
import numpy as np
from fractions import Fraction


def choquet_value_frac(g, v, r: Fraction):
    # Copy graph, because we will make changes in it's structure
    g = g.copy()

    # Количество вершин и количество ребер
    N = len(g.nodes)
    E = len(g.edges)

    # Def f
    # In our case it's r in power of closes path
    paths = dict(nx.shortest_path(g))

    def f(s, t):
        return r ** Fraction(len(paths[s][t]) - 1)

    # Calculate f for all nodes
    Fv = {n: f(v, n) for n in sorted(g.nodes)}

    # Sort values asc, saving nodes names
    Fv = dict(sorted(Fv.items(), key=lambda item: (item[1], item[0])))

    # Re-mapping nodes according to Fv
    mapping = dict(zip(
        Fv.keys(),
        sorted(g.nodes)
    ))

    g = nx.relabel_nodes(g, mapping)
    Fv = {mapping[i]: Fv[i] for i in Fv}

    # Calc all mu values
    muAs = []
    for i in Fv.keys():
        muAs.append(Fraction(len(g.edges), E))
        g.remove_node(i)

    # Adding case f(0) = 0
    Fv[0] = 0

    # Calculate Shoquet Integral values
    R = sum([(Fv[i] - Fv[i - 1]) * muAs[i - 1] for i in range(1, N)])
    return R


def choquet_value_frac_all(g):
    return [choquet_value_frac(g, i, Fraction(1, 4)) for i in g.nodes]
