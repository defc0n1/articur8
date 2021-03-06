import jsonpickle
import math

import clusterer, clusterformats
from articurate.pymotherlode import api
from articurate.pymotherlode.api import *
import articurate.utils.loader as loader
from articurate.utils.class_definitions import ParamObj     
from articurate.utils.config import *


# get articles from wherever
#articles = loader.get_latest_dump()
articles = loader.collect_last_dumps()

# define parameters
if config['db.coldStart']:
	params = ParamObj(config['db.coldStartNumClusters'], 'nmf', True) # (num_clusters, clustering_method, only_titles)
else:
	params = ParamObj(config['db.numClusters'], 'nmf', True) # (num_clusters, clustering_method, only_titles)

# get clusters, result has assignment list and cluster objects
result = clusterer.cluster(articles, params)

# print output
for cluster in result['clusters']:
	print cluster.identifier, ":", len(cluster.article_list), ":", cluster.closest_article.title, ":", cluster.NE_list, "\n"
	#for article in cluster.article_list:
	#	print article.feed_title, article.updated_at, article.title
	#print "\n\n"

# stores a copy of the cluster in JSON in the motherlode, with or without content
clusterformats.clustersToJSONNew(result['clusters']) #Deprecated