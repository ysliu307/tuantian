from scipy.spatial import distance
import numpy as np
import random
from random import uniform
from random import randint 
import math


def cost(centroids, clusters):
    return sum(distance.cdist([centroid], cluster, 'sqeuclidean').sum()
            for centroid, cluster in zip(centroids, clusters))


def compute_centroids(clusters):
    return [np.mean(cluster, axis=0) for cluster in clusters]


def kmeans(k, centroids, points, method):
    clusters = [[] for _ in range(k)]

    for point in points:
        clusters[closest_centroid(point, centroids)].append(point)

    new_centroids = compute_centroids(clusters)

    if not equals(centroids, new_centroids):
        print("cost [k={}, {}] = {}".format(k, method, cost(new_centroids, clusters)))

        clusters = kmeans(k, new_centroids, points, method)

    return clusters


def closest_centroid(point, centroids):
    min_distance = float('inf')
    belongs_to_cluster = None
    for j, centroid in enumerate(centroids):
        dist = distance.sqeuclidean(point, centroid)
        if dist < min_distance:
            min_distance = dist
            belongs_to_cluster = j

    return belongs_to_cluster


def contains(point1, points):
    for point2 in points:
        if point1[0] == point2[0] and point1[1] == point2[1]:
        # if all(x == y for x, y in izip(points1, points2)):
            return True

    return False


def equals(points1, points2):
    if len(points1) != len(points2):
        return False

    for point1, point2 in zip(points1, points2):
        if point1[0] != point2[0] or point1[1] != point2[1]:
        # if any(x != y for x, y in izip(points1, points2)):
            return False

    return True

# def cuckoo_search(data):
#     n = len(data)
#     pa = 0.25;
#     Tol = 1.0e-5
#     fitness = (10 ^ 10) * np.ones((n))
#     fmin, bestnest, nest, fitness = get_best_nest(data, data, fitness)
#     N_iter = 0
#     while (fmin > Tol):
#         new_nest = get_cuckoos(nest, bestnest)
#         N_iter = N_iter + n
#         new_nest = empty_nests(nest, pa)
#         fnew, best, nest, fitness = get_best_nest(nest, new_nest, fitness)
#         N_iter = N_iter + n
#         if fnew < fmin:
#             fmin = fnew
#             bestnest = best

#     return bestnest, fmin

# def get_cuckoos(nest, best):
#     n = nest.shape[0]
#     beta = 1.5
#     sigma = (gamma(1+beta)*sin(pi*beta/2)/(gamma((1+beta)/2)*beta*2^((beta-1)/2)))^(1/beta)

#     for j in range(n):
#         s = nest[j, :]
#         u = np.random(len(s)) * sigma
#         v = np.random(len(s))
#         step = u ./ abs(v) .^ (1 / beta)
#         stepsize = 0.01 * step .* (s - best)
#         s = s + stepsize .* random(len(s))
#         nest[j, :] = s


if __name__ == "__main__":
    data = [[-19.0748,     -8.536       ],
            [ 22.0108,      -10.9737    ],
            [ 12.6597,      19.2601     ],
            [ 11.26884087,  19.90132146 ],
            [ 15.44640731,  21.13121676 ],
            [-20.03865146,  -8.820872829],
            [-19.65417726,  -8.211477352],
            [-15.97295894,  -9.648002534],
            [-18.74359696,  -5.383551586],
            [-19.453215,   -8.146120006],
            [-16.43074088,  -7.524968005],
            [-19.75512437,  -8.533215751],
            [-19.56237082,  -8.798668569],
            [-19.47135573,  -8.057217004],
            [-18.60946986,  -4.475888949],
            [-21.59368337,  -10.38712463],
            [-15.39158057,  -3.8336522  ],
            [-40.0,          40.0       ]]
    k = 4

    # k-means picking the first k points as centroids
    #for i = 1 : 50:
    centroids = data[:k]
    #centroids = cuckoo_search(data[:k])
    clusters = kmeans(k, centroids, data, "first")

    
    print(centroids)
