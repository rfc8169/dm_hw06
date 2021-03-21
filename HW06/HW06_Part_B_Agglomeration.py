"""
Assignment: HW06
Description: An agglomerative clustering algorithm that groups clusters using a euclidean distance metric.
Author: Reed Cogliano, Neel Raj
"""

import math
import statistics

import numpy
import pandas


def remove_duplicates(csv_file):
    """
    Removes duplicates from the dataframe created from the csv data file and outputs that result to the console,
    which is the exact same as the original data since there are not duplicates.
    :param csv_file: The student data
    :return:
    """
    student_df = pandas.read_csv(csv_file)
    student_df.drop_duplicates()
    print(student_df.to_string())


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
    student_df = pandas.read_csv(csv_file)
    for cluster_index in range(len(student_df)):
        array_from_df = student_df.iloc[cluster_index].to_numpy()
        clusters.append(Cluster([array_from_df], array_from_df))
    agglomerative_clustering(clusters)


def euclidean_distance(clusterA, clusterB):
    euclidean_distance = 0
    average_a = 0
    average_b = 0
    for data_index in range(1, len(clusterA.center)):
        average_a += clusterA.center[data_index]
        average_b += clusterB.center[data_index]
    average_a /= len(clusterA.center) - 1
    average_b /= len(clusterB.center) - 1

    euclidean_distance = numpy.linalg.norm(average_a - average_b)
    return euclidean_distance


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
    and added their merged cluster back in. Recurse until there are only two clusters remaining.
    """
    best_cluster_dist = math.inf
    for clusterA in clusters:
        for clusterB in clusters:
            # Compares cluster IDs to ensure the same cluster isn't compared with itself
            if clusterA.center[0] != clusterB.center[0]:
                current_dist = euclidean_distance(clusterA, clusterB)
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

    mean_array = []
    # Takes the mean of each element in all the clusters and creates one center array for the new merged cluster
    for array in merge_array:
        mean_array.append(statistics.mean(array))
    # The new merged cluster
    if sum(clusterA.center[1:]) > sum(clusterB.center[1:]):
        #print("smaller: ", clusterB.center)
        print("Merging Cluster #", clusterA.clusters[0][0], ": ",  len(clusterA.clusters))
    else:
        #print("smaller: ", clusterA.center)
        print("Merging Cluster #", clusterB.clusters[0][0], ": ", len(clusterB.clusters))

    mergedCluster = Cluster(allClusters, mean_array)

    if len(clusters) <= 6:
        # Ends the recursion when the number of clusters in the group reaches 2
        for c in clusters:
            print("Final Six Clusters - Number of Clusters: ", len(c.clusters), 'Cluster Center: ', c.center, "Cluster ID: ", c.clusters[0][0])
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
    prepare_agglomerative("test.csv")
