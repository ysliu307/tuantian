from sklearn.cluster import KMeans
import numpy as np
from util import tsv_to_matrix


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

def main(train_file):
    data = tsv_to_matrix(train_file, 942, 1682)
    kmeans = KMeans(n_clusters=2, random_state=0).fit(data)
    print (data.shape)
    k = 4
    # k-means picking the first k points as centroids

    centroids = kmeans.cluster_centers
    labels = kmeans.labels_
    print(centroids)

if __name__ == "__main__":
    main('train_data.tsv')
