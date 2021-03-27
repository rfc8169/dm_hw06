"""
Assignment: HW06
Description: An agglomerative clustering algorithm that groups clusters using a euclidean distance metric.
Author: Reed Cogliano, Neel Raj
"""

import math
import numpy
import pandas
import time

from scipy.cluster import hierarchy
import matplotlib.pyplot as plt


class Cluster:
    """
    A class that stores the data of the merging clusters and their resulting mode arrays
    """

    def __init__(self, clusters, center):
        """
        The initialization for the class
        :param clusters: A list of all the clusters that have been merged for this cluster, stored as arrays in an array
        :param center: The resulting array of taking the mode of all the clusters that were merged to create this cluster
        """
        self.clusters = clusters
        self.center = center


def create_dendrogram(merged_clusters):
    Z = hierarchy.linkage(merged_clusters, 'single')
    plt.figure()
    dn = hierarchy.dendrogram(Z)
    plt.show()


def prepare_agglomerative(csv_file):
    """
    Converts the dataframe data to binary values and converts the dataframe values to arrays
    to make it easier to work with
    :param csv_file: The file the data is taken from
    :return:
    """
    clusters = []
    student_df = pandas.read_csv(csv_file)
    for cluster_index in range(len(student_df)):
        array_from_df = student_df.iloc[cluster_index].to_numpy()
        clusters.append(Cluster([array_from_df], array_from_df))
    #   Start time of Agglomerative Clustering Algo
    start = time.time()
    merged_clusters = agglomerative_clustering(clusters, numpy.array([]))
    #   End time of Agglomerative Clustering Algo
    end = time.time()
    print("Runtime: " + str(round(int(end - start), 3)))
    create_dendrogram(merged_clusters)


def euclidean_distance(clusterA, clusterB):
    euclidean_dist = numpy.linalg.norm(clusterA.center - clusterB.center)
    return euclidean_dist


def agglomerative_clustering(clusters, merged_clusters):
    """
    Loops through every cluster and finds two clusters with the shortest euclidean distance.
    Once the closest clusters are found it takes the mode of their binary values and stores that result into a new
    cluster as its center, the actual data in each cluster is also stored in the cluster object so it can calculate a
    new center if it has to merge again. Once it has created a merged cluster it deletes the two older clusters from
    the array and adds the merged cluster. Then it will recurse and execute this function again, until
    there are only two clusters remaining in the array
    :param clusters - an array of all the grouped clusters that exist
    :param: merged_clusters -
    :return: Recursively calls this function on the new list that removed the two closest clusters
    and added their merged cluster back in. Recurse until there are only two clusters remaining.
    """
    similarClusterA = None
    similarClusterB = None
    best_cluster_dist = math.inf
    for clusterA in clusters:
        for clusterB in clusters:
            # Compares cluster IDs to ensure the same cluster isn't compared with itself
            if clusterA.center[0] != clusterB.center[0]:
                current_dist = euclidean_distance(clusterA, clusterB)
                # The function for getting the hamming distance between two clusters
                # current_dist = hamming_cluster_distance(clusterA, clusterB)
                if current_dist <= best_cluster_dist:
                    # Finds the two clusters with the shortest distance between each other from all the clusters
                    best_cluster_dist = current_dist
                    similarClusterA = clusterA
                    similarClusterB = clusterB

    allClusters = numpy.append(similarClusterA.clusters, similarClusterB.clusters, axis=0)

    mean_array = numpy.mean(allClusters, axis=0)
    min_id = math.inf
    for min_id_index in range(len(allClusters)):
        if allClusters[min_id_index][0] < min_id:
            min_id = allClusters[min_id_index][0]
    mean_array[0] = min_id

    # The new merged cluster
    # if sum(clusterA.center[1:]) > sum(clusterB.center[1:]):
    # print("smaller: ", clusterB.center)
    # print("Merging Cluster #", clusterA.clusters[0][0], ": ",  len(clusterA.clusters))
    # else:
    # print("smaller: ", clusterA.center)
    # print("Merging Cluster #", clusterB.clusters[0][0], ": ", len(clusterB.clusters))
    # print("CLUSTERING: ", allClusters)

    mergedCluster = Cluster(allClusters, mean_array)

    if len(clusters) == 6:
        # Ends the recursion when the number of clusters in the group reaches 2
        for c in clusters:
            print("Final Two Clusters - Cluster ID:", c.center[0], "Number of Clusters: ", len(c.clusters),
                  'Cluster Center: ', c.center)
        return merged_clusters
    else:
        # Recursively calls this function group the clusters, removing the grouped clusters and adding the new
        # merged cluster before passing the array of clusters
        linkage_data = numpy.array(
            [similarClusterA.center[0], similarClusterB.center[0], best_cluster_dist, len(allClusters)])
        if merged_clusters.size == 0:
            merged_clusters = linkage_data
        else:
            merged_clusters = numpy.vstack((merged_clusters, linkage_data))
        clusters.remove(similarClusterA)
        clusters.remove(similarClusterB)
        clusters.append(mergedCluster)
        return agglomerative_clustering(clusters, merged_clusters)


if __name__ == '__main__':
    """
    Expects the first argument when calling the program to be the filename of the csv data
    """
    prepare_agglomerative("HW_PCA_SHOPPING_CART_v896.csv")
