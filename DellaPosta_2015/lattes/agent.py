import networkx as nx
import scipy.spatial


class Agent(object):
    def __init__(self, traits, attitudes, social_network, name):
        """

        Parameters
        ----------
        traits: list
            "Each agent has five static attributes corresponding to fixed demographic
            traits" (p1491)

        attitudes: list
            "[Each agent has] 20 dynamic attributes corresponding to changeable attitudes (i.e.,
            political opinions and lifestyle preferences)" (p1491)

            "For simplicity, these 25 dimensions are binary (as gender, favor/oppose, or whether or
             not the agent engages in some activity)." (p1491)

        social_network: networkx graph
        name: the name of this agent in the social network


        """
        self.traits = traits
        self.attitudes = attitudes
        self.social_network = social_network
        self.name = name

        self.neighbor_weights = []

    def weight_neighbors(self):


        #
        neighbor_distances = []
        for neighbor in nx.neighbors(self.social_network, self.name):
            # todo: add here a noise component to the array of neighbor's beliefs
            neighbor_array = neighbor.agent.attitudes + neighbor.agent.traits
            self_array = self.attitudes + self.traits

            neighbor_distances.append(scipy.spatial.distance.pdist([neighbor_array, self_array],
                                                                 metric='euclidean'))

        self.neighbor_weights = neighbor_distances
