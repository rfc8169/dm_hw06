"""
Assignment: HW06
Description: Perform k-means clustering on provided data
Author: Reed Cogliano, Neel Raj
"""
from sklearn.cluster import KMeans
import pandas


def prepare_k_means(csv_file):
    """
    Converts the csv file to a pandas dataframe to form a list of clusters to perform k-means clustering on
    :param: csv_file - csv file containing data to process
    """
    student_df = pandas.read_csv(csv_file)
    clusters = []
    for cluster_index in range(len(student_df)):
        array_from_df = student_df.iloc[cluster_index].to_numpy()
        clusters.append(array_from_df[1:])
    k_means_clustering(clusters)


def k_means_clustering(clusters):
    """
    Takes the individual clusters and performs k-means on these clusters until there are six clusters
    :param: clusters - list of individual clusters to perform k-means on
    """
    number_of_clusters = 6
    k_means = KMeans(number_of_clusters)
    k_means.fit(clusters)
    print(k_means.cluster_centers_)


if __name__ == '__main__':
    """
    Expects the first argument when calling the program to be the filename of the csv data
    """
    prepare_k_means("HW_PCA_SHOPPING_CART_v896.csv")
