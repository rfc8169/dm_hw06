"""
Assignment: HW03
Description: An agglomerative clustering algorithm that groups clusters using a jaccard similarity coefficient
converted to a distance or hamming distance.
Author: Reed Cogliano
"""

import math
import statistics
import sys
import numpy



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


def prepare_agglomerative(csv_file):
    """
    Converts the dataframe data to binary values and converts the dataframe values to arrays
    to make it easier to work with
    :param csv_file: The file the data is taken from
    :return:
    """
    clusters = []
    student_df = binary_to_numeric(csv_file)
    for cluster_index in range(len(student_df)):
        array_from_df = student_df.iloc[cluster_index].to_numpy()
        clusters.append(Cluster([array_from_df], array_from_df))
    agglomerative_clustering(clusters)


def jaccard_cluster_distance(clusterA, clusterB):
    """
    Calculates the Jaccard coefficient between clusters, and then converts that similarity value to a distance value
    :param clusterA: The first cluster being compared
    :param clusterB: The second cluster being compared
    :return: The jaccard similarity converts to a distance, between two clusters
    """
    jaccard_present_and_matching = 0
    jaccard_total_present = 0
    for data_index in range(2, len(clusterA.center)):
        # Calculates the intersection and union of the clusters A and B
        if clusterA.center[data_index] == clusterB.center[data_index] and clusterA.center[data_index] != 0:
            jaccard_present_and_matching += int(clusterA.center[data_index])
            jaccard_total_present += int(clusterA.center[data_index])
        elif clusterA.center[data_index] != 0:
            jaccard_total_present += int(clusterA.center[data_index])
        elif clusterB.center[data_index] != 0:
            jaccard_total_present += int(clusterB.center[data_index])
    jaccard_coefficient = jaccard_present_and_matching / jaccard_total_present
    # Converts the jaccard similarity to a distance by subtracting it from 1
    jaccard_distance = 1 - jaccard_coefficient
    return jaccard_distance


def hamming_cluster_distance(clusterA, clusterB):
    """
    Calculates the Hamming distance between clusters
    :param clusterA: The first cluster being compared
    :param clusterB: The second cluster being compared
    :return: The hamming distance between two clusters
    """
    hamming_distance = 0
    for data_index in range(2, len(clusterA.center)):
        # Only increments the distance for values that differm such as [0, 1] and [1, 0]
        if clusterA.center[data_index] != clusterB.center[data_index]:
            hamming_distance += int(clusterA.center[data_index])
    return hamming_distance


def agglomerative_clustering(clusters):
    """
    Loops through every cluster and finds two clusters with the shortest jaccard distance or hamming distance.
    Once the closest clusters are found it takes the mode of their binary values and stores that result into a new
    cluster as its center, the actual data in each cluster is also stored in the cluster object so it can calculate a
    new center if it has to merge again. Once it has created a merged cluster it deletes the two older clusters from
    the array and adds the merged cluster. Then it will recurse and execute this function again, until
    there are only two clusters remaining in the array
    :param clusters: An array of all the grouped clusters that exist
    :return: Recursively calls this function on the new list that removed the two closest clusters
    and added their merged cluster back in. Recurses until there are only two clusters remaining.
    """
    best_cluster_dist = math.inf
    for clusterA in clusters:
        for clusterB in clusters:
            # Compares cluster IDs to ensure the same cluster isn't compared with itself
            if clusterA.center[0] != clusterB.center[0]:
                current_dist = jaccard_cluster_distance(clusterA, clusterB)
                # The function for getting the hamming distance between two clusters
                # current_dist = hamming_cluster_distance(clusterA, clusterB)
                if current_dist < best_cluster_dist:
                    # Finds the two clusters with the shortest distance between each other from all the clusters
                    best_cluster_dist = current_dist
                    similarClusterA = clusterA
                    similarClusterB = clusterB

    # Creates initialized arrays used to create a new merged cluster
    merge_array = similarClusterA.clusters[0]
    allClusters = [similarClusterA.clusters[0]]
    # Stores all the clusters in each cluster into their own array so the mode of all the clusters can be easily found
    for a_cluster_index in range(1, len(similarClusterA.clusters)):
        merge_array = numpy.column_stack((merge_array, similarClusterA.clusters[a_cluster_index]))
        allClusters.append(similarClusterA.clusters[a_cluster_index])
    for b_cluster in similarClusterB.clusters:
        merge_array = numpy.column_stack((merge_array, b_cluster))
        allClusters.append(b_cluster)

    mode_array = []
    # Takes the mode of each element in all the clusters and creates one center array for the new merged cluster
    for array in merge_array:
        mode_array.append(statistics.mode(array))
    # The new merged cluster
    mergedCluster = Cluster(allClusters, mode_array)

    if len(clusters) <= 2:
        # Ends the recursion when the number of clusters in the group reaches 2
        for c in clusters:
            print("Final Two Clusters - Number of Clusters: ", len(c.clusters), 'Cluster Center: ', c.center)
        return clusters
    else:
        # Recursively calls this function group the clusters, removing the grouped clusters and adding the new
        # merged cluster before passing the array of clusters
        clusters.remove(similarClusterA)
        clusters.remove(similarClusterB)
        clusters.append(mergedCluster)
        return agglomerative_clustering(clusters)

if __name__ == '__main__':
    """
    Expects the first argument when calling the program to be the filename of the csv data
    """
    prepare_agglomerative(sys.argv[1])

