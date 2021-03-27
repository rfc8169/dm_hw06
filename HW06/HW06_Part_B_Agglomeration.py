"""
Assignment: HW06
Description: An agglomerative clustering algorithm that groups clusters using a euclidean distance metric.
Author: Reed Cogliano, Neel Raj
"""

import math
import numpy
import pandas

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
    """
    Creates a dendrogram of all the merges in the agglomerative clustering algorithm and displays it.
    :param merged_clusters: Contains the cluster centers of each cluster merged, the distance used to find the clusters
    and the length of the newly merged clusters
    :return:
    """
    # Uses single linkage to find the closest distance between merges
    Z = hierarchy.linkage(merged_clusters, 'single')
    plt.figure()
    dn = hierarchy.dendrogram(Z)
    plt.show()


def prepare_agglomerative(csv_file):
    """
    Creates a cluster for each row in the csv file, each cluster will start with a cluster center and
    a list of all the clusters inside it. Those clusters are then passed to the agglomerative clustering
    function and then creates a dendrogram from all of the merges created in the agglomeration.
    :param csv_file: The file the data is taken from
    :return:
    """
    clusters = []
    student_df = pandas.read_csv(csv_file)
    for cluster_index in range(len(student_df)):
        array_from_df = student_df.iloc[cluster_index].to_numpy()
        clusters.append(Cluster([array_from_df], array_from_df))
    merged_clusters = agglomerative_clustering(clusters, numpy.array([]))
    create_dendrogram(merged_clusters)


def euclidean_distance(clusterA, clusterB):
    """
    Gets the euclidean distance between cluster centers
    :param clusterA: The first cluster
    :param clusterB: The second cluster
    :return: The euclidean distance between two clusters
    """
    # Uses a numpy function to get the euclidean distance of the two cluster centers
    euclidean_dist = numpy.linalg.norm(clusterA.center - clusterB.center)
    return euclidean_dist


def agglomerative_clustering(clusters, merged_clusters):
    """
    Loops through every cluster and finds two clusters with the shortest euclidean distance.
    Once the closest clusters are found it takes the mean of all the cluster values for each record and stores
    that result into a new cluster as its center, the actual data in each cluster is also stored in the cluster object so it can calculate a
    new center if it has to merge again. Once it has created a merged cluster it deletes the two older clusters from
    the array and adds the merged cluster. Then it will recurse and execute this function again, until
    there are only two clusters remaining in the array. It also has to keep track of all the merges performed since they
    are used to create a dendrogram once it has finished agglomerating.
    :param clusters - An array of all the grouped clusters that exist
    :param: merged_clusters - An array of all the merges performed, the cluster centers of the merged clusters, the distance used
    to find those clusters, and their new cluster size.
    :return: Recursively calls this function on the new list that removed the two closest clusters
    and added their merged cluster back in. Also keeps track of and adds the new cluster merges for the dendrogram.
    Recurse until there are only two clusters remaining.
    """
    similarClusterA = None
    similarClusterB = None
    # smallClusters = []
    best_cluster_dist = math.inf
    for clusterA in clusters:
        for clusterB in clusters:
            # Compares cluster IDs to ensure the same cluster isn't compared with itself
            if clusterA.center[0] != clusterB.center[0]:
                # The function for getting the euclidean distance between two clusters
                current_dist = euclidean_distance(clusterA, clusterB)
                if current_dist <= best_cluster_dist:
                    # Finds the two clusters with the shortest distance between each other from all the clusters
                    best_cluster_dist = current_dist
                    similarClusterA = clusterA
                    similarClusterB = clusterB

    # Creates one array that contains all of the clusters that were in the two clusters that are being merged
    allClusters = numpy.append(similarClusterA.clusters, similarClusterB.clusters, axis=0)

    # Gets the mean of all the cluster values between the two clusters being merged
    mean_array = numpy.mean(allClusters, axis=0)
    min_id = math.inf
    # Gets the minimum cluster id in all of the clusters between the clusters being merged
    for min_id_index in range(len(allClusters)):
        if allClusters[min_id_index][0] < min_id:
            min_id = allClusters[min_id_index][0]
    mean_array[0] = min_id

    # Saves the smaller clusters that were merged
    # if len(similarClusterA.clusters) > len(similarClusterB.clusters):
    #     smallClusters.append(similarClusterB)
    # else:
    #     smallClusters.append(similarClusterA)

    # Creates the new merged cluster
    mergedCluster = Cluster(allClusters, mean_array)

    if len(clusters) == 6:
        # Ends the recursion when the number of clusters in the group reaches 2
        for c in clusters:
            print("Final Six Clusters - Cluster ID:", c.center[0], "Number of Clusters: ", len(c.clusters),
                  'Cluster Center: ', c.center)

        # Outputs the last 18 smallest merged clusters
        # for small in range(len(smallClusters) - 1, len(smallClusters) - 19, -1):
        #     print("SMALL CLUSTER - index: ", small, "center: ", smallClusters[small].center, "size: ", len(smallClusters[small].clusters))
        return merged_clusters
    else:
        # Recursively calls this function group the clusters, removing the grouped clusters and adding the new
        # merged cluster before passing the array of clusters

        # Creates an array of the attributes needed for the dendrogram
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
