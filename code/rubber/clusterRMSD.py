#!/usr/bin/python
## Run cluster analysis on given JSON file
## Much of this script has been adapted from
## masili's scripts
##
## Mehdi Nellen, Tuebingen 2015


import sys, os
import json
import logging
import argparse
from scipy import cluster, spatial
import numpy as np


def getArguments(command_line):
    '''create the command line argument parser 
    @return: a ArgumentParser.parse_args() Namespace
    with the parameters. (adapted from masili)'''
    parser = argparse.ArgumentParser(description='Do cluster analysis on a distance matrix',   fromfile_prefix_chars='@',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('distance_matrix', 
                        help='The JSON file created by runProFit.py containing '
                        'the distance matrix for the clustering',
                        type=file)
    parser.add_argument('nClust', 
                        help='The number of clusters to return',
                        type=int)
    parser.add_argument('clustMeth', 
                        help="Clustering method to use. Alowed: 'single' 'complete' 'weighted' 'centroid' 'median' 'ward'",
                        type=str)
    args = parser.parse_args(command_line)

    return args

def Cluster(distmat, nClust, clustMeth):
    ''' This runs the clustering from the SciPy module
        it runs the calculations with the specified method
        and makes 'nClust' clusters after finishing it 
        returns an array with numbers of the clusters 
        given to each element of the original dictionairy '''
        
    # use distance matrix to generate linkage matrix
    z = cluster.hierarchy.linkage(distmat, method=clustMeth, metric='euclidean')
        
    # generate clusters
    clust_arr = cluster.hierarchy.fcluster(z, nClust, criterion='maxclust')
    
    return clust_arr

def whereMediod(distmat, clust_arr, clustNum):
    ''' get mediod of a cluster. Input: Distance matrix, 
    which will be subset with the cluster array on the 
    given clusternumber. returns mediod's index '''
    # First make the distance matrix  in square form
    distmat = spatial.distance.squareform(distmat)

    # make logic vector to subset distance matrix
    mask  = clust_arr == clustNum
    imask = np.where(mask)
    # subset the distance matrix for
    sub_DM = distmat[:,imask][imask,:]
    # sum the rows
    c_sum  = np.cumsum(sub_DM, axis=1)
    # get the index of the minimum value in the array
    min_in = np.argmin(c_sum)
    # mediod index 
    med_in = imask[min_in]
    
    return med_in[0]

def getAllMediods(nClust, distmat, clust_arr, pdb_names):
    # get the mediod indices for all clusters
    print "#"*24 + "\nMEDIODS FOR ALL CLUSTERS\n" + "#"*24
    f = open('RosettaBackrubClusterMediods.txt', 'w')
    for clustNum in range(1, nClust+1):
        med_in = whereMediod(distmat, clust_arr, clustNum)
        print pdb_names[med_in]
        f.write(pdb_names[med_in] + '\n')
    f.close

def getCorNam(clust_arr, name_arr, nClust):
    ''' return  corresponding names. Prints all names within clusters '''
    for clust in range(1, nClust+1):
        indices = [i for i, x in enumerate(clust_arr) if x == clust]
        containing = [name_arr[i] for i in indices]
        print 'Cluster %s contains:\n'%clust
        print '\n'.join(containing)
        print '*'*30
        

def main( command_line):
    '''Run everything'''
    # set logger
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    logger = logging.getLogger(__name__)
    args = getArguments( command_line)
    
    logging.info('\nusing following settings:' +
                 '\nClustering method:\t' + args.clustMeth +
                 '\nNumber of clusters:\t' + str(args.nClust) +
                 '\nJSON data file:\t\t' + 'lol')

    distmat = json.load(args.distance_matrix)
    logging.info('JSON data loaded\n'
                 'Starting cluster analysis')
    clust_arr = Cluster(distmat['rmsd'], args.nClust, args.clustMeth) 
    logging.info('Cluster analysis completed\n\n\n')
    print getCorNam(clust_arr, distmat['pdb_list_0'], args.nClust)
    getAllMediods(args.nClust, distmat['rmsd'], clust_arr,  distmat['pdb_list_0'])

if __name__ == "__main__":
    main( sys.argv[1:])
