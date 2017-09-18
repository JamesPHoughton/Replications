import networkx as nx
from lattes import utils


class Society(object):
    def __init__(
            self,
            k=99,  # "We set k=99, approximating the cognitive limit to the number of people
            #         with whom one can maintain a stable social relationship (Dunbar 1992)"
            n=1000,
            phi=0.1,  # "We set phi=10%, which Watts (1999) found was sufficient to produce
            #            the characteristic small-world condition" (p1491)
    ):
        """
        Parameters
        ----------
        k: "each agent has k immediate neighbors in the same cave" (p1490)
        n: "n is the population size" (p1490)
        phi: "A chosen percentage phi of the edges (or network ties) are randomly re-wired using
              the degree-preserving procedure introduced by Maslov and Sneppen (2002)" (p1490)
        """

        n_caves = n / (k + 1)  # "the network consists of n/(k+1) caves" (p1490)

        social_network = nx.connected_caveman_graph(n_caves, k + 1)
        social_network = utils.maslov_sneppen(social_network, phi)
