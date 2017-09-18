import numpy as np
import networkx as nx


def maslov_sneppen(g, phi):
    """
    Degree-preserving random rewiring

    "Take a simple example with four network “nodes” A, B, C, and D. Further assume that A shares
    an “edge” with (i.e., is tied to) B while C shares an edge with D. To “rewire” these ties,
    the Maslov-Sneppen procedure would simply swap them such that A becomes connected to D and C
    to B, thereby preserving the original degree of each node. Edges are selected at random from
    the network and rewired using this procedure until F percentage of the edges have been
    swapped." (p1491)

    Parameters
    ----------
    g: the network to rewire
    phi: the degree of rewiring

    Returns
    -------

    """

    edgelist = iter(np.random.permutation(nx.edges(g)))

    for _ in range(int(nx.number_of_edges(g) * phi / 2)):
        (a1, a2), (b1, b2) = next(edgelist), next(edgelist)
        g.remove_edges_from([(a1, a2), (b1, b2)])
        g.add_edges_from([(a1, b1), (a2, b2)])

    return g
