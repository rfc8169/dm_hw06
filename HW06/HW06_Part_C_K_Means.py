"""
Assignment: HW06
Description:
Author: Reed Cogliano, Neel Raj
"""
from sklearn.cluster import KMeans
import pandas


def prepare_kmeans(csv_file):
    student_df = pandas.read_csv(csv_file)
    clusters = []
    for cluster_index in range(len(student_df)):
        array_from_df = student_df.iloc[cluster_index].to_numpy()
        clusters.append(array_from_df[1:])
    kmeans_clustering(clusters)


def kmeans_clustering(clusters):
    number_of_clusters = 6
    kmeans = KMeans(number_of_clusters)
    kmeans.fit(clusters)
    print(kmeans.cluster_centers_)


if __name__ == '__main__':
    """
    Expects the first argument when calling the program to be the filename of the csv data
    """
    prepare_kmeans("test.csv")