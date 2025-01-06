#!/usr/bin/env python3

import scipy
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score


def find_permutation(n_clusters, real_labels, labels):
    permutation=[]
    for i in range(n_clusters):
        idx = labels == i
        # Choose the most common label among data points in the cluster
        new_label=scipy.stats.mode(real_labels[idx])[0]#[0]
        permutation.append(new_label)
    return permutation

def plant_clustering():
    d, t = load_iris().data, load_iris().target
    malli = KMeans(3, random_state = 0)
    malli.fit(d)
    permutaatio = find_permutation(3, t, malli.labels_)
    labels_ennuste = [permutaatio[i] for i in malli.labels_]
    return accuracy_score(t, labels_ennuste)

def main():
    print(plant_clustering())

if __name__ == "__main__":
    main()
