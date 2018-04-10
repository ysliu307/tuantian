from scipy.spatial import distance
import numpy as np
import random
from random import uniform
from random import randint 
import math
from util import tsv_to_matrix
import math



def cost(centroids, clusters):
    return sum(distance.cdist([centroid], cluster, 'sqeuclidean').sum()
            for centroid, cluster in zip(centroids, clusters))


def compute_centroids(clusters):
    return [np.mean(cluster, axis=0) for cluster in clusters]


def kmeans(k, centroids, points, method):
    clusters = [[] for _ in range(k)]
    labels = []
    for point in points:
        labels.append(closest_centroid(point, centroids))
        clusters[closest_centroid(point, centroids)].append(point)

    new_centroids = compute_centroids(clusters)

    print("shape of new centroids: " + str(len(new_centroids[0])))
    #print("shape of new centroids: " + str(len(new_centroids)[1]))

    if not equals(centroids, new_centroids):
        #print("cost [k={}, {}] = {}".format(k, method, cost(new_centroids, clusters)))

        clusters,labels, tmp_centroids = kmeans(k, new_centroids, points, method)

    return clusters,labels, new_centroids


def equals(points1, points2):
    if len(points1) != len(points2):
        return False

    i = 0
    for point1, point2 in zip(points1, points2):
        i += 1
        #print("shape of new point: " + str(len(point2)))
        if i == 2:
            print("point2: " + str(point2))
        if point1[0] != point2[0] or point1[1] != point2[1]:
        # if any(x != y for x, y in izip(points1, points2)):
            return False

    return True

def closest_centroid(point, centroids):
    min_distance = float('inf')
    belongs_to_cluster = None
    for i in range(4):
        dist = distance.sqeuclidean(point, centroids[i])
        if dist < min_distance:
            min_distance = dist
            belongs_to_cluster = i

    return belongs_to_cluster


# def contains(point1, points):
#   for point2 in points:
#       if point1[0] == point2[0] and point1[1] == point2[1]:
#       # if all(x == y for x, y in izip(points1, points2)):
#           return True

#   return False



def cuckoo_search(n, dim, init_nest):
    lb = -1
    ub = 1
    N_IterTotal = 100
    pa = 0.25


    # if init_nest == None:
    #   nest = np.random.rand(n, dim) * (ub - lb) + lb
    # else:
    nest = np.copy(init_nest)

    new_nest = np.zeros((n, dim))
    new_nest = np.copy(nest)

    bestnest = [0] * dim

    fitness = np.zeros(n)
    fitness.fill(float("inf"))

    fmin, bestnest, nest, fitness = get_best_nest(nest, new_nest, fitness, n, dim)
    convergence = []

    # Main loop counter
    for iter in range (0,N_IterTotal):
        # Generate new solutions (but keep the current best)
     
        new_nest = get_cuckoos(nest,bestnest,lb,ub,n,dim)    
         
        # Evaluate new solutions and find best
        fnew, best, nest, fitness = get_best_nest(nest, new_nest, fitness, n, dim)
            
        new_nest = empty_nests(new_nest, pa, n, dim)
                
        # Evaluate new solutions and find best
        fnew, best, nest, fitness=get_best_nest(nest, new_nest, fitness, n, dim)
    
        if fnew < fmin:
            fmin = fnew
            bestnest = best
    
        if (iter % 10 == 0):
            print(['At iteration ' + str(iter) + ' the best fitness is ' + str(fmin)])
        convergence.append(fmin)
    return new_nest

def get_cuckoos(nest, best, lb, ub, n, dim):
    
    # perform Levy flights
    tempnest = np.zeros((n,dim))
    tempnest = np.array(nest)
    beta = 3/2;
    sigma = (math.gamma(1 + beta) * math.sin(math.pi * beta / 2) / (math.gamma(( 1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))) ** (1 / beta)

    s = np.zeros(dim)

    for j in range (0, n):
        s = nest[j,:]
        u = np.random.randn(len(s)) * sigma
        v = np.random.randn(len(s))
        step = u / abs(v) ** (1 / beta)
 
        stepsize = 0.01 * (step * (s - best))

        s = s + stepsize * np.random.randn(len(s))
    
    
        tempnest[j,:] = np.clip(s, lb, ub)

    return tempnest

def get_best_nest(nest, newnest, fitness, n, dim):
# Evaluating all new solutions
    tempnest = np.zeros((n,dim))
    tempnest = np.copy(nest)

    for j in range(0,n):
    #for j=1:size(nest,1),
        fnew = objf(newnest[j,:])
        if fnew <= fitness[j]:
           fitness[j] = fnew
           tempnest[j,:] = newnest[j,:]
        
    # Find the current best

    fmin = min(fitness)
    K = np.argmin(fitness)
    bestlocal = tempnest[K,:]

    return fmin, bestlocal, tempnest, fitness

# Replace some nests by constructing new solutions/nests
def empty_nests(nest, pa, n, dim):

    # Discovered or not 
    tempnest = np.zeros((n,dim))

    K = np.random.uniform(0, 1, (n,dim)) > pa
    
    stepsize = random.random() * (nest[np.random.permutation(n),:] - nest[np.random.permutation(n),:])

    tempnest = nest + stepsize * K
 
    return tempnest

def objf(x): 
    dim = len(x);
    o = -20 * np.exp(-.2 * np.sqrt(np.sum(x ** 2) / dim)) - np.exp(np.sum(np.cos(2 * math.pi * x)) / dim) + 20 + np.exp(1)
    return o

def main(train_file):
    data = tsv_to_matrix(train_file, 942, 1682).toarray()

    k = 4
#shape[0] is 4, shape[1] is 1682
    dim = data.shape[1]

#    print("data shape0:" + str(data[:k].shape[0]))
#    print("data shape1:" + str(data[:k].shape[1]))

    iteration = 10

    for i in range(0, iteration):
        #call cuckoo search
        if i == 0:
            centroids = cuckoo_search(k, dim, data[:k])
        else:
            centroids = cuckoo_search(k, dim, new_centroids)

        # k-means picking the first k points as centroids
        #centroids = data[:k]

        print("shape[0]: " + str(centroids.shape[0]))
        print("shape[1]: " + str(centroids.shape[1]))

        clusters, labels, new_centroids = kmeans(k, centroids, data, "first")

        if i == iteration - 1:  
            train0 = np.array(clusters[0])
            train1 = np.array(clusters[1])
            train2 = np.array(clusters[2])
            train3 = np.array(clusters[3])
            file = open('label.txt', 'w')
            for i in range(len(labels)):
                file.write("%s\n" %(str(labels[i])))
            file.close()
            print(len(train0))
            print(len(train1))
            print(len(train2))
            print(len(train3))




if __name__ == "__main__":
    main('train_50.tsv')
