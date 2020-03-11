"""Class for constructing stakeholder networks, producing analytics
and storing plots."""
import itertools
import logging
import os
import pickle

import daiquiri
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.centrality import betweenness_centrality
import numpy as np
import pandas as pd
import scipy.stats as stats

from database import Database

class StakeholderNetwork:
    """Builds out the stakeholder network. If rebuild=False, then
    the class will look for a saved version of the stakeholder network
    first. Otherwise, the network information will be pulled from
    the database."""
    def __init__(self, organization, package, rebuild=False):
        self.database = Database()
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.image_path = os.path.join(self.path, '../network_plots')
        self.binary_path = os.path.join(self.path, '../network_binaries')

        self.organization = organization
        self.package = package

        if rebuild:
            self.network = self.build_network()
        else:
            organization = organization.replace(' ', '-')
            package = package.replace(' ', '-')
            filename=f'{organization}-{package}.pickle'
            with open(filename 'rb') as f:
                self.network = pickle.load(f)

        self.gini = self.compute_gini()
        self.avg_min_path = self.compute_avg_min_path()
        self.avg_clustering = self.compute_avg_clustering()
        self.betweenness_centrality = betweenness_centrality(self.network,
                                                             normalized=True)

    def get_links(self):
        """Pulls links from the database that are used to build
        the stakeholder network."""
        sql = """
            SELECT *
            FROM open_source.issue_comments
            WHERE organization = '{}' AND package = '{}'
        """.format(self.organization, self.package)
        df = pd.read_sql(sql, self.database.connection)
        return df

    def build_network(self):
        """Builds a networkx graph from a dataframe of links."""
        network = nx.Graph()
        df = self.get_links()
        issues = df.groupby('issue_number')
        for issue_number, issue in issues:
            users = list(issue['user_id'].unique())
            pairs = itertools.combinations(users, 2)
            for pair in pairs:
                network.add_edge(*pair)
        network.remove_nodes_from(nx.isolates(network))
        return network

    def compute_gini(self):
        """Computes the gini coefficient for the network."""
        if self.network:
            degrees = [self.network.degree(x) for x in self.network.nodes]
            gini_coefficient = gini(degrees)
        else:
            gini_coefficient = None
        return gini_coefficient

    def compute_avg_min_path(self):
        """Computes the average shortest path between two
        nodes in the network."""
        if self.network:
            subgraph = biggest_subgraph(self.network)
            return nx.average_shortest_path_length(subgraph)
        else:
            return None

    def compute_avg_clustering(self):
        """Computes the avg clustering coefficient for the network."""
        if self.network:
            subgraph = biggest_subgraph(self.network)
            return nx.algorithms.average_clustering(subgraph)
        else:
            return None

    def load_network(self, crowd_pct):
        """Loads the network into the database."""
        item = {
            'organization': self.organization,
            'package': self.package,
            'gini_coefficient': self.gini,
            'avg_clustering': self.avg_clustering,
            'avg_min_path': self.avg_min_path,
            'crowd_pct': crowd_pct,
            'nodes': len(self.network.nodes),
            'stakeholder_network': pickle.dumps(self.network)
        }
        self.database.load_item(item, 'stakeholder_networks')
        self.plot_network(save=True)

    def delete_network(self):
        """Loads the network into the database."""
        sql = """
            DELETE FROM open_source.stakeholder_networks
            WHERE organization = '{}' AND package = '{}'
        """.format(self.organization, self.package)
        self.database.run_query(sql)

    def plot_network(self, save=False):
        """Plots the stakeholder network. If save is set to True,
        the plot is saved as a .jpg to the images folder."""
        if self.network:
            subgraph = biggest_subgraph(self.network)
            pos = nx.drawing.spring_layout(subgraph)
            plt.clf()
            plt.figure(figsize=(20,10))
            nx.draw(subgraph, pos, node_size=50)
            if save:
                filename = '-'.join(['network', self.organization, self.package])
                filename += '.png'
                plt.savefig(self.image_path + '/' + filename)
            else:
                plt.show()

    def load_user_centralities(self):
        """Loads betweenness centrality for each user into the database."""
        for user_id in self.betweenness_centrality:
            betweenness_centrality = self.betweenness_centrality[user_id]
            item = {
                'organization': self.organization,
                'package': self.package,
                'user_id': user_id,
                'betweenness_centrality': betweenness_centrality
            }
            self.database.load_item(item, 'network_centrality')

    def delete_user_centrality(self, user_id):
        """Deletes the current betweenness centrality for the user from
        the database."""
        sql = """
            DELETE FROM open_source.network_centrality
            WHERE organization = '{}' AND package = '{}' and user_id = '{}'
        """.format(self.organization, self.package, user_id)
        self.database.run_query(sql)


def gini(x):
    """Computes the Gini coefficient for a discrete distribution."""
    mad = np.abs(np.subtract.outer(x, x)).mean()
    # Relative mean absolute difference
    rmad = mad/np.mean(x)
    # Gini coefficient
    g = 0.5 * rmad
    return g

def biggest_subgraph(network):
    """Finds the biggest fully connected subgraph in the network."""
    connected_components = nx.connected_components(network)
    graphs = [network.subgraph(x).copy() for x in connected_components]
    sizes = [len(x.nodes) for x in graphs]
    if sizes:
        idx = sizes.index(max(sizes))
        biggest_graph = graphs[idx]
    else:
        biggest_graph = None
    return biggest_graph
