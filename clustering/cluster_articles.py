from __future__ import division
import re, pprint, numpy
import time

from nltk import cluster
from nltk.cluster import euclidean_distance, cosine_distance

import loader
import vectorer

# TO DO:
# 1) Give more weight to Nouns
# 2) Ignore numbers in text -- DONE
# 3) Add tech sites to stopword list -- DONE
# 4) Try PCA/SVD/NMF


def print_cluster_means(cluster_means, unique_tokens): # displays top words in each mean

    for count, array in enumerate(cluster_means):
        indices = sorted(range(len(array)),key=lambda x:array[x])
        top_indices = indices[len(indices)-10:len(indices)]
        print count, " : ",
        for index in top_indices:
            print unique_tokens[index],
        print ""    

def cluster_means_from_assignment(vectors, assignment):

    num_labels = len(set(assignment))

    print assignment

    cluster_means = []

    for i in range(0, num_labels):
        
        indices = [j for j in range(len(assignment)) if assignment[j] == i]

        print i, indices

        cluster_vectors = numpy.array([vectors[j] for j in indices])

        print numpy.mean(cluster_vectors, axis=0)
        cluster_means.append(numpy.mean(cluster_vectors, axis=0))

    return cluster_means
        

def cluster_nmf(vectors, rank):

    print "Starting NMF clustering"
    
    start_time = time.time()
    
    # Generate random matrix factors which we will pass as fixed factors to Nimfa.
    rank = 5
    init_W = np.random.rand(len(vectors), rank)
    init_H = np.random.rand(rank, len(vectors[0]))

    # Run NMF.
    # We don't specify any algorithm parameters. Defaults will be used.
    # We specify fixed initialization method and pass matrix factors.
    fctr = nimfa.mf(vectors, method = "nmf", seed = "fixed", W = init_W, H = init_H, rank = rank)
    fctr_res = nimfa.mf_run(fctr)

    # Print the loss function (Euclidean distance between target matrix and its estimate). 
    print "Euclidean distance: %5.3e" % fctr_res.distance(metric = "euclidean")

    # It should print 'fixed'.
    print fctr_res.seeding

    # By default, max 30 iterations are performed.
    print fctr_res.n_iter

    end_time = time.time()
    print "Clustering required", (end_time-start_time),"seconds"
    
    print "done"


def cluster_kmeans(vectors, num_clusters, distance_metric):

    print "Starting KMeans clustering"
    
    start_time = time.time()

    # initialize
    if distance_metric == "euclidean":
        clusterer = cluster.KMeansClusterer(num_clusters, euclidean_distance)
    elif distance_metric == "cosine":
        clusterer = cluster.KMeansClusterer(num_clusters, cosine_distance)

    assignment = clusterer.cluster(vectors, False)
    cluster_means = clusterer.means()

    end_time = time.time()
    print "Clustering required", (end_time-start_time),"seconds"

    return assignment, cluster_means


def cluster_gaac(vectors, num_clusters):

    print "Starting GAAC clustering"
    
    start_time = time.time()

    # nltk implementation might not be that good
    clusterer = cluster.GAAClusterer(num_clusters)
    assignment = clusterer.cluster(vectors, True)

    # get cluster means from assignment
    cluster_means = cluster_means_from_assignment(vectors, assignment)

    end_time = time.time()
    print "Clustering required", (end_time-start_time),"seconds"

    return assignment, cluster_means
    
def cluster_articles(articles, num_clusters, method):

    # convert articles to tf-idf vectors
    IDF, unique_tokens_dict, unique_tokens, vectors = vectorer.vectorize_articles(articles)

    # cluster the article vectors
    if method == 'kmeans':
        assignment, cluster_means = cluster_kmeans(vectors, num_clusters, "cosine");
        print_cluster_means(cluster_means, unique_tokens)
    elif method == 'gaac':
        assignment, cluster_means = cluster_gaac(vectors, num_clusters)
        print_cluster_means(cluster_means, unique_tokens)
    elif method == 'nmf':
        cluster_nmf(vectors, num_clusters)


    return None
    
if __name__ == "__main__":

    file_name = "../feeddumps/201309282106.opml"

    # get articles from wherever
    articles = loader.load_xml_data(file_name)

    articles = articles[:200]

    # cluster the articles
    num_clusters = 10
    clusters = cluster_articles(articles, num_clusters, 'gaac')
    clusters = cluster_articles(articles, num_clusters, 'kmeans')






