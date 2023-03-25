__author__ = """Jahid Arafat (jahidapon@gmail.com)"""
#    Copyright (C) 2018 by
#    Jahid Arafat <jahidapon@gmail.com>
#    All rights reserved.
#    BSD license.

import logPuzzleSupportTools as tool
import networkx as nx
import os

#@Graph preparation
def preparingNXGraph_undirected(nodeList,edgeList):
    #------------Preparing Undirected Graph--------------------------------
    G=nx.Graph()
    G.add_nodes_from(nodeList)
    G.add_edges_from(edgeList)
    pos=nx.spring_layout(G)
    return G,pos

#@Graph preparation
def preparingNXGraph_directed(nodeList,edgeList,cords_list):
    DiG=nx.DiGraph()
    DiG.add_nodes_from(nodeList)
    DiG.add_edges_from(edgeList)
    dpos={}
    nodeIndex=0

    for cord in cords_list:
        dpos[nodeList[nodeIndex]]=cord
        nodeIndex+=1
    return DiG,dpos

#@Graph preparation addingCentralityAttributesToNodes
def addingAttributesToNodes(G,nodeList,jsonDir,fileName):
    #we get the nodeList from the csv file which contains all node information
    #checkout tool.writingIntoCSV(sortedCentralityDict,fileName) function
    os.chdir(jsonDir)

    UDG_centralities={}
    DiG_Centralities={}
    DiG_IN_Centralities={}
    DiG_OUT_Centralities={}
    UDG_betweenness_centralities={}
    DiG_betweenness_centralities={}

    UDG_eigenvector_centralities={}
    DiG_eigenvector_centralities={}

    UDG_closeness_centralities={}
    DiG_closeness_centralities={}

    UDG_katz_centralities={}
    DiG_katz_centralities={}

    UDG_pagerank_centralities={}
    DiG_pagerank_centralities={}

    DiG_hitshubs_centralities={}
    DiG_hitsauthorities_centralities={}

    for node in nodeList: #node[0] -->IP
        UDG_centralities[node[0]]=node[1]
        DiG_Centralities[node[0]]=node[2]
        DiG_IN_Centralities[node[0]]=node[3]
        DiG_OUT_Centralities[node[0]]=node[4]
        UDG_betweenness_centralities[node[0]]=node[5]
        DiG_betweenness_centralities[node[0]]=node[6]
        UDG_closeness_centralities[node[0]]=node[7]
        DiG_closeness_centralities[node[0]]=node[8]
        UDG_eigenvector_centralities[node[0]]=node[9]
        DiG_eigenvector_centralities[node[0]]=node[10]
        UDG_katz_centralities[node[0]]=node[11]
        DiG_katz_centralities[node[0]]=node[12]
        UDG_pagerank_centralities[node[0]]=node[13]
        DiG_pagerank_centralities[node[0]]=node[14]
        DiG_hitshubs_centralities[node[0]]=node[15]
        DiG_hitsauthorities_centralities[node[0]]=node[16]



    nx.set_node_attributes(G, UDG_centralities, "UDG_centralities")
    nx.set_node_attributes(G, DiG_Centralities, "DiG_Centralities")
    nx.set_node_attributes(G, DiG_IN_Centralities, "DiG_IN_Centralities")
    nx.set_node_attributes(G, DiG_OUT_Centralities, "DiG_OUT_Centralities")
    nx.set_node_attributes(G, UDG_betweenness_centralities, "UDG_betweenness_centralities")
    nx.set_node_attributes(G, DiG_betweenness_centralities, "DiG_betweenness_centralities")

    nx.set_node_attributes(G, UDG_eigenvector_centralities, "UDG_eigenvector_centralities")
    nx.set_node_attributes(G, DiG_eigenvector_centralities, "DiG_eigenvector_centralities")

    nx.set_node_attributes(G, UDG_closeness_centralities, "UDG_closeness_centralities")
    nx.set_node_attributes(G, DiG_closeness_centralities, "DiG_closeness_centralities")

    nx.set_node_attributes(G, UDG_katz_centralities, "UDG_katz_centralities")
    nx.set_node_attributes(G, DiG_katz_centralities, "DiG_katz_centralities")

    nx.set_node_attributes(G, UDG_pagerank_centralities, "UDG_pagerank_centralities")
    nx.set_node_attributes(G, DiG_pagerank_centralities, "DiG_pagerank_centralities")

    nx.set_node_attributes(G, DiG_hitshubs_centralities, "DiG_hitshubs_centralities")
    nx.set_node_attributes(G, DiG_hitsauthorities_centralities, "DiG_hitsauthorities_centralities")


    tool.dumpingIntoJSON(G,fileName) #storing into allCentralities.json
def main():
    pass

if __name__ == '__main__':
    main()
