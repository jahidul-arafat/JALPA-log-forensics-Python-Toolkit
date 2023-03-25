'''
Objective: To draw all the UD Subgraphs and DiG_SCC Subgraphs, this doesnt draw the main graph.
Remebermber: mergedJSON and mergedCSV are not controlled from here, this is done at netDraw.py

'''
__author__ = """Jahid Arafat (jahidapon@gmail.com)"""
#    Copyright (C) 2018 by
#    Jahid Arafat <jahidapon@gmail.com>
#    All rights reserved.
#    BSD license.

import pprint
import csv
import json
import sys
import os
import networkx as nx
from operator import itemgetter
import communityme as communityme
import logPuzzleSupportTools as tool
from networkx.drawing.nx_pydot import write_dot
import netDraw
import matplotlib.pyplot as plt
from pylab import rcParams
import pandas as pd

from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from pycallgraph import Config
from pycallgraph import GlobbingFilter

def diGraphNotSupportMessage():
    msg="Directed Graph Dont Support the following features:\n\
    1. no is_connected()\n\
    2. No Subgraph creation\n\
    3. no Modularity\n\
    4. no Components findings\n\
    5. and you cant Find per community Hubs,Influentials,brokers"
    print (msg)

def netxGraphBuilding(node_names,edges,sGraph=None,graphType="UD"):
    #------Part2: NexworkX Graph Building------------------------
    print("Graph Type: {}".format(graphType))
    if sGraph==None:
        if graphType=="UD":
            G=nx.Graph()
            G.add_nodes_from(node_names)
            G.add_edges_from(edges) #remember this is an unweighted undirected graph# why undirected will be explained later
        elif graphType=="DiG":
            diGraphNotSupportMessage()
            G=nx.DiGraph()
            G.add_nodes_from(node_names)
            G.add_edges_from(edges)
    else:
        spos=nx.spring_layout(sGraph)
        SUB_UD_DegCent=nx.degree_centrality(sGraph)
        SUB_UD_BetCent=nx.betweenness_centrality(sGraph)
        SUB_UD_ClosenessCent=nx.closeness_centrality(sGraph)
        SUB_UD_EigenCent=nx.eigenvector_centrality(sGraph) #better use DiG
        SUB_UD_KatzCent=nx.katz_centrality(sGraph,alpha=0.10,beta=1.0) #better use DiG
        SUB_UD_PagerankCent=nx.pagerank(sGraph,alpha=0.85) #better use DiG
        SUB_UD_HitsHubsCent,SUB_UD_HitsAuthoritiesCent=nx.hits(sGraph)#better use DiG
        return sGraph,spos,SUB_UD_DegCent,SUB_UD_BetCent,SUB_UD_ClosenessCent,SUB_UD_EigenCent,SUB_UD_KatzCent,SUB_UD_PagerankCent,SUB_UD_HitsHubsCent,SUB_UD_HitsAuthoritiesCent
    return G

def netxGraphAddingAttributes(G,nodes):
    date_dict={}
    from_time_dict={}
    to_time_dict={}
    total_time_hit_dict={}
    browser_dict={}
    os_dict={}
    email_dict={}
    get_dict={}
    seng_dict={}

    for node in nodes:
        date_dict[node[0]]=node[1]
        from_time_dict[node[0]]=node[2]
        to_time_dict[node[0]]=node[3]
        total_time_hit_dict[node[0]]=node[4]
        browser_dict[node[0]]=node[5]
        os_dict[node[0]]=node[6]
        email_dict[node[0]]=node[7]
        get_dict[node[0]]=node[8]
        seng_dict[node[0]]=node[9]


        nx.set_node_attributes(G, date_dict, "date")
        nx.set_node_attributes(G, from_time_dict, "from_time")
        nx.set_node_attributes(G, to_time_dict, "to_date")
        nx.set_node_attributes(G, total_time_hit_dict, "total_time_hit")
        nx.set_node_attributes(G, browser_dict, "browser")
        nx.set_node_attributes(G, os_dict, "os")
        nx.set_node_attributes(G, email_dict, "email")
        nx.set_node_attributes(G, get_dict, "GETURL")
        nx.set_node_attributes(G, seng_dict, "seng")

    return G

def shortestPathCalculationAndSavingToFile(unalteredRepoDict,G,node_names,fileName): #../animalLogSimulation
    shortestPaths=[]
    sPathStr=""
    attemptedNode=0
    for fromIndex in range(len(node_names)):
        sPathStr+="{}\n-------------\n".format(node_names[fromIndex])
        for toIndex in range(len(node_names)):
            try:
                if not node_names[fromIndex]==node_names[toIndex]:
                    attemptedNode+=1
                    sPathStr+="{}-->{}:::".format(node_names[fromIndex],node_names[toIndex])
                    sPath=nx.shortest_path(G, node_names[fromIndex], node_names[toIndex])
                    shortestPaths.append(sPath)
                    sPathStr+="{}-->{}\n".format(sPath,len(sPath)-1)
            except:
                continue
        sPathStr+="Summary:\nTotal {} nodes have found shortest paths from {}".format(attemptedNode,node_names[fromIndex])
        sPathStr+="\n\n"
        attemptedNode=0

    #Writing the all pair shortest paths into a file
    #shortestPathDir="/home/jahid/Desktop/AllMyWorks/InformationSecurity/google/google-python-exercises/logpuzzle/logSolverMyCodeRepo/simulationResults/outputGenerated/animalLogSimulation"
    shortestPathDir=unalteredRepoDict
    with open(shortestPathDir+"/"+fileName,'w') as fp:
        fp.write(sPathStr)

def dealingWithRootGraph(G,node_names):
    rootGraphMatrix={}
    traidic_closure=nx.transitivity(G) #both UD and DiG support traidic closure
    rootGraphMatrix[len(node_names)]=["density:{}".format(nx.density(G)),\
    "traidic_closure: {}".format(traidic_closure)]#testing

    if not type(G)==nx.DiGraph: #directed graph dont have diameter and is_connected features
        if nx.is_connected(G):
            rootGraphMatrix[len(node_names)].extend(["root diameter :{}".format(nx.diameter(G))])
        else:
            rootGraphMatrix[len(node_names)].extend(["root diameter :None"])

    print (rootGraphMatrix)
    return rootGraphMatrix


def drawSubgraphs(subG,spos,measure,measure_name):
    tool.draw(subG, spos,measure,measure_name)


def dealingWithSubGraphs_SCC_DiG(DiG):
    scc_len_list=[len(GScc) for GScc in sorted(nx.strongly_connected_component_subgraphs(DiG),key=len,reverse=True)]
    scc_subgraphs=[GScc for GScc in sorted(nx.strongly_connected_components(DiG),key=len,reverse=True)]

    return scc_subgraphs,scc_len_list
    #use graph condensation for DiG subgraph generation


def removingDefaultsAttributesFromSubGraphSCCDiG(sGraph):
    attributeToBeRemoved=["GETURL","browser","date","email","from_time","os","seng","to_date","total_time_hit"]
    for ip in sGraph.nodes:
        for attr in attributeToBeRemoved:
            del dict(sGraph.nodes)[ip][attr] #netx V2 supported
    return sGraph #basic attributes are removed from sub Graph

def sortedSubGraphSCCDiGAttributes(SUB_DiG_DegCent,SUB_DiG_BetCent,SUB_DiG_CloseCent,SUB_DiG_EigenCent,SUB_DiG_KatzCent,
            SUB_DiG_PageCent,SUB_DiG_HITSHUBS,SUB_DiG_HITSAUTHORITY):
    sorted_SUB_DiG_DegCent=sorted(SUB_DiG_DegCent.items(),key=itemgetter(1),reverse=True)
    sorted_SUB_DiG_BetCent=sorted(SUB_DiG_BetCent.items(),key=itemgetter(1),reverse=True)
    sorted_SUB_DiG_CloseCent=sorted(SUB_DiG_CloseCent.items(),key=itemgetter(1),reverse=True)
    sorted_SUB_DiG_EigenCent=sorted(SUB_DiG_EigenCent.items(),key=itemgetter(1),reverse=True)
    sorted_SUB_DiG_KatzCent=sorted(SUB_DiG_KatzCent.items(),key=itemgetter(1),reverse=True)
    sorted_SUB_DiG_PageCent=sorted(SUB_DiG_PageCent.items(),key=itemgetter(1),reverse=True)
    sorted_SUB_DiG_HITSHUBS=sorted(SUB_DiG_HITSHUBS.items(),key=itemgetter(1),reverse=True)
    sorted_SUB_DiG_HITSAUTHORITY=sorted(SUB_DiG_HITSAUTHORITY.items(),key=itemgetter(1),reverse=True)
    return sorted_SUB_DiG_DegCent,sorted_SUB_DiG_BetCent,sorted_SUB_DiG_CloseCent,sorted_SUB_DiG_EigenCent,sorted_SUB_DiG_KatzCent,sorted_SUB_DiG_PageCent,sorted_SUB_DiG_HITSHUBS,sorted_SUB_DiG_HITSAUTHORITY

def drawingAndSavingSubGraphSCC_DiG(sGraph,sCounter,figCounter,sorted_SUB_DiG_DegCent,sorted_SUB_DiG_BetCent,
sorted_SUB_DiG_CloseCent,sorted_SUB_DiG_EigenCent,sorted_SUB_DiG_KatzCent,sorted_SUB_DiG_PageCent,
sorted_SUB_DiG_HITSHUBS,sorted_SUB_DiG_HITSAUTHORITY,SUB_DiG_DegCent,SUB_DiG_BetCent,
SUB_DiG_CloseCent,SUB_DiG_EigenCent,SUB_DiG_KatzCent,SUB_DiG_PageCent,SUB_DiG_HITSHUBS,SUB_DiG_HITSAUTHORITY,jsonDir,csvDir):
    spos=nx.spring_layout(sGraph)
    rcParams['figure.figsize'] = 20, 10 #width,height

    plt.figure() #dont give figure number error, it creates some bug output with a default red figure
    plt.subplot(221)
    print("sorted_SUB_DiG_DegCent\n{}\n\n".format(tool.printCentralityValues(sorted_SUB_DiG_DegCent)))
    drawSubgraphs(sGraph,spos,SUB_DiG_DegCent,"Sub-Graph DiG-SCC DegCentrality {}".format(sCounter))

    plt.subplot(222)
    print("sorted_SUB_DiG_BetCent\n{}\n\n".format(tool.printCentralityValues(sorted_SUB_DiG_BetCent)))
    drawSubgraphs(sGraph,spos,SUB_DiG_BetCent,"Sub-Graph DiG-SCC BetCentrality {}".format(sCounter))

    plt.subplot(223)
    print("sorted_SUB_DiG_CloseCent\n{}\n\n".format(tool.printCentralityValues(sorted_SUB_DiG_CloseCent)))
    drawSubgraphs(sGraph,spos,SUB_DiG_CloseCent,"Sub-Graph DiG-SCC CloseCentrality {}".format(sCounter))

    plt.subplot(224)
    print("sorted_SUB_DiG_EigenCent\n{}\n\n".format(tool.printCentralityValues(sorted_SUB_DiG_EigenCent)))
    drawSubgraphs(sGraph,spos,SUB_DiG_EigenCent,"Sub-Graph DiG-SCC EigenCentrality {}".format(sCounter))

    plt.savefig("subGraphDiG_SCC{}_part_{}.png".format(sCounter,figCounter))
    plt.show()

    figCounter+=1

    plt.figure()
    plt.subplot(221)
    print("sorted_SUB_DiG_KatzCent\n{}\n\n".format(tool.printCentralityValues(sorted_SUB_DiG_KatzCent)))
    drawSubgraphs(sGraph,spos,SUB_DiG_KatzCent,"Sub_Graph DiG-SCC KatzCentrality {}".format(sCounter))

    plt.subplot(222)
    print("sorted_SUB_DiG_PageCent\n{}\n\n".format(tool.printCentralityValues(sorted_SUB_DiG_PageCent)))
    drawSubgraphs(sGraph,spos,SUB_DiG_PageCent,"Sub_Graph DiG-SCC PageCentrality {}".format(sCounter))

    plt.subplot(223)
    print("sorted_SUB_DiG_HITSHUBS\n{}\n\n".format(tool.printCentralityValues(sorted_SUB_DiG_HITSHUBS)))
    drawSubgraphs(sGraph,spos,SUB_DiG_HITSHUBS,"Sub_Graph DiG-SCC HITSHUBS {}".format(sCounter))

    plt.subplot(224)
    print("sorted_SUB_DiG_HITSAUTHORITIES\n{}\n\n".format(tool.printCentralityValues(sorted_SUB_DiG_HITSAUTHORITY)))
    drawSubgraphs(sGraph,spos,SUB_DiG_HITSAUTHORITY,"Sub_Graph DiG-SCC HITSAUTHORITY {}".format(sCounter))


    plt.savefig("subGraphDiG_SCC{}_part_{}.png".format(sCounter,figCounter))
    plt.show()

    os.chdir(jsonDir)
    jsonFileName="dig_scc_subgraph_{}.json".format(sCounter)
    csvFileName="dig_scc_subgraph_{}.csv".format(sCounter)

    tool.dumpingIntoJSON(sGraph,jsonFileName)
    tool.loadJsonToCSV(jsonDir,csvDir,jsonFileName,csvFileName)

    sCounter+=1
    return sCounter,figCounter

def addingCentralityAttributesToSubGraphDiGSCC(sGraph):
    SUB_DiG_DegCent=nx.degree_centrality(sGraph)
    sorted_SUB_DiG_DegCent=sorted(SUB_DiG_DegCent.items(),key=itemgetter(1),reverse=True)

    SUB_DiG_BetCent=nx.betweenness_centrality(sGraph)
    SUB_DiG_CloseCent=nx.closeness_centrality(sGraph)
    SUB_DiG_EigenCent=nx.eigenvector_centrality_numpy(sGraph)

    SUB_DiG_KatzCent=nx.katz_centrality_numpy(sGraph,alpha=0.10,beta=1.0)
    SUB_DiG_PageCent=nx.pagerank_numpy(sGraph,alpha=0.85)
    SUB_DiG_HITSHUBS,SUB_DiG_HITSAUTHORITY=nx.hits_numpy(sGraph)


    nx.set_node_attributes(sGraph,SUB_DiG_DegCent,"DiG_SCC_SUB_degreeCentrality")
    nx.set_node_attributes(sGraph,SUB_DiG_BetCent,"DiG_SCC_SUB_BetCentrality")
    nx.set_node_attributes(sGraph,SUB_DiG_CloseCent,"DiG_SCC_SUB_closeCentrality")
    nx.set_node_attributes(sGraph,SUB_DiG_EigenCent,"DiG_SCC_SUB_eigenCentrality")
    nx.set_node_attributes(sGraph,SUB_DiG_KatzCent,"DiG_SCC_SUB_katzCentrality")
    nx.set_node_attributes(sGraph,SUB_DiG_PageCent,"DiG_SCC_SUB_pageCentrality")
    nx.set_node_attributes(sGraph,SUB_DiG_HITSHUBS,"DiG_SCC_SUB_hitshubsCentrality")
    nx.set_node_attributes(sGraph,SUB_DiG_HITSAUTHORITY,"DiG_SCC_SUB_hitsauthorityCentrality")
    return sGraph,SUB_DiG_DegCent,SUB_DiG_BetCent,SUB_DiG_CloseCent,SUB_DiG_EigenCent,SUB_DiG_KatzCent,SUB_DiG_PageCent,SUB_DiG_HITSHUBS,SUB_DiG_HITSAUTHORITY



def netxSubGraphBuilding_SCC_DiG(DiG,scc_subgraphList,scc_subgraphLenList,jsonDir,csvDir):
    lenIndex=0
    sCounter=1
    subGraphDir=jsonDir+"/"+"Graphs"
    tool.createDirectory(subGraphDir)
    os.chdir(subGraphDir)
    figCounter=1

    for scc_sg in scc_subgraphList:
        if scc_subgraphLenList[lenIndex]>1:
            sGraph=nx.subgraph(DiG,scc_sg) #here the graph will automatically get its defaults attributes which I set before along with the new attributes I am setting now

            #removingDefaultsAttributesFromSubGraphSCCDiG
            sGraph=removingDefaultsAttributesFromSubGraphSCCDiG(sGraph)

            #addingCentralityAttributesToSubGraphDiGSCC(sGraph)
            sGraph,SUB_DiG_DegCent,SUB_DiG_BetCent,SUB_DiG_CloseCent,SUB_DiG_EigenCent,SUB_DiG_KatzCent,SUB_DiG_PageCent,SUB_DiG_HITSHUBS,SUB_DiG_HITSAUTHORITY=\
            addingCentralityAttributesToSubGraphDiGSCC(sGraph)

            #get the sortedSubGraphSCCDiGAttributes
            sorted_SUB_DiG_DegCent,sorted_SUB_DiG_BetCent,sorted_SUB_DiG_CloseCent,sorted_SUB_DiG_EigenCent,sorted_SUB_DiG_KatzCent,sorted_SUB_DiG_PageCent,sorted_SUB_DiG_HITSHUBS,sorted_SUB_DiG_HITSAUTHORITY=\
            sortedSubGraphSCCDiGAttributes(SUB_DiG_DegCent,SUB_DiG_BetCent,SUB_DiG_CloseCent,SUB_DiG_EigenCent,SUB_DiG_KatzCent,
            SUB_DiG_PageCent,SUB_DiG_HITSHUBS,SUB_DiG_HITSAUTHORITY)

            #Drawing and Saving the SubGraphSCC_DiG
            sCounter,figCounter= drawingAndSavingSubGraphSCC_DiG(sGraph,sCounter,figCounter,sorted_SUB_DiG_DegCent,sorted_SUB_DiG_BetCent,sorted_SUB_DiG_CloseCent,
            sorted_SUB_DiG_EigenCent,sorted_SUB_DiG_KatzCent,sorted_SUB_DiG_PageCent,
            sorted_SUB_DiG_HITSHUBS,sorted_SUB_DiG_HITSAUTHORITY,SUB_DiG_DegCent,SUB_DiG_BetCent,
            SUB_DiG_CloseCent,SUB_DiG_EigenCent,SUB_DiG_KatzCent,SUB_DiG_PageCent,SUB_DiG_HITSHUBS,SUB_DiG_HITSAUTHORITY,jsonDir,csvDir)

        #if ends here----------------------
        figCounter=1#resetting
        lenIndex+=1
    #for loop ends here------------------------

def dealingWithSubGraphs(G,jsonDir,csvDir,reportStr=""):
    subGraphMatrix={}

    components=nx.connected_components(G) #returns an object #not implemented for DiG
    compLenList=[]
    compList=[]
    for comp in components: #accessing the elements of "components" object
        compLenList.append(len(comp))
        compList.append(comp) #this is not a set but list
    reportStr+="{} components exits of length {}\n".format(len(compList),compLenList)

    sCounter=1
    #rcParams['figure.figsize'] = 20, 10 #width,height

    #--------Save the graphs into Graph directory inside JSON folder----
    subGraphDir=jsonDir+"/"+"Graphs"
    tool.createDirectory(subGraphDir)
    #os.chdir(subGraphDir)
    #------------------------------------------
    figCounter=1
    for cntComponents in compList:
        subGraph=G.subgraph(list(cntComponents))
        print("Subgraph {}::Edges {}".format(sCounter,len(list(subGraph.edges))))

        #removingDefaultsAttributesFromSubGraphSCCDiG
        subGraph=removingDefaultsAttributesFromSubGraphSCCDiG(subGraph) #this function is for both UD and SCC_DiG

        #Getting subgraph parameters
        subGraph,spos,degCent,betCent,closeCent,eigenCent,katzCent,pageCent,hitshubCent,hitsauthorityCent=netxGraphBuilding([],[],subGraph)

        #adding centralities attributes to subGraph_UD
        nx.set_node_attributes(subGraph,degCent,"UD_SUB_degCentrality")
        nx.set_node_attributes(subGraph,betCent,"UD_SUB_betCentrality")
        nx.set_node_attributes(subGraph,closeCent,"UD_SUB_closeCentrality")
        nx.set_node_attributes(subGraph,eigenCent,"UD_SUB_eigenCentrality")
        nx.set_node_attributes(subGraph,katzCent,"UD_SUB_katzCentrality")
        nx.set_node_attributes(subGraph,pageCent,"UD_SUB_pageCentrality")
        nx.set_node_attributes(subGraph,hitshubCent,"UD_SUB_hitshubCentrality")
        nx.set_node_attributes(subGraph,hitsauthorityCent,"UD_SUB_hitsauthorityCentrality")

        #Loading and Saving SubGraph centralitites attributes to JSON
        os.chdir(jsonDir)
        jsonFileName="ud_subgraph_{}.json".format(sCounter)
        tool.dumpingIntoJSON(subGraph,jsonFileName)

        #Saving jsonData into CSV
        csvFileName="ud_subgraph_{}.csv".format(sCounter)
        tool.loadJsonToCSV(jsonDir,csvDir,jsonFileName,csvFileName)

        #-------sub-graph visualization--------------------------
        os.chdir(subGraphDir) #go to graph dir, where subgraph pictures are going to be saved
        rcParams['figure.figsize'] = 20, 10 #width,height

        #part-1:DegCent,BetCent,CloseCent,EigenCent
        plt.figure(figCounter)

        plt.subplot(221)
        sorted_degCent=sorted(degCent.items(),key=itemgetter(1),reverse=True)
        print("SUB_UD_DegCent:\n{}\n\n".format(tool.printCentralityValues(sorted_degCent)))
        drawSubgraphs(subGraph,spos,degCent,"Sub-Graph UD DegCentrality {}".format(sCounter))

        plt.subplot(222)
        sorted_betCent=sorted(betCent.items(),key=itemgetter(1),reverse=True)
        print("SUB_UD_BetCent:\n{}\n\n".format(tool.printCentralityValues(sorted_betCent)))
        drawSubgraphs(subGraph,spos,betCent,"Sub-Graph UD BetCentrality {}".format(sCounter))

        plt.subplot(223)
        sorted_closeCent=sorted(closeCent.items(),key=itemgetter(1),reverse=True)
        print("SUB_UD_CloseCent:\n{}\n\n".format(tool.printCentralityValues(sorted_closeCent)))
        drawSubgraphs(subGraph,spos,closeCent,"Sub-Graph UD ClosenessCentrality {}".format(sCounter))

        plt.subplot(224)
        sorted_eigenCent=sorted(eigenCent.items(),key=itemgetter(1),reverse=True)
        print("SUB_UD_EigenCent:\n{}\n\n".format(tool.printCentralityValues(sorted_eigenCent)))
        drawSubgraphs(subGraph,spos,eigenCent,"Sub-Graph UD EigenVectorCentrality {}".format(sCounter))

        plt.savefig("subGraph{}_part_{}.png".format(sCounter,figCounter))
        plt.show()

        #Part-2: KatxCent,PageRankCent,HitsHubCent,HitsAuthorityCent
        figCounter=figCounter+1
        plt.figure(figCounter)
        plt.subplot(221)
        sorted_katzCent=sorted(katzCent.items(),key=itemgetter(1),reverse=True)
        print("SUB_UD_KatzCent:\n{}\n\n".format(tool.printCentralityValues(sorted_katzCent)))
        drawSubgraphs(subGraph,spos,katzCent,"Sub_Graph UD KatzCent {}".format(sCounter))

        plt.subplot(222)
        sorted_pageCent=sorted(pageCent.items(),key=itemgetter(1),reverse=True)
        print("SUB_UD_PageCent:\n{}\n\n".format(tool.printCentralityValues(sorted_pageCent)))
        drawSubgraphs(subGraph,spos,pageCent,"Sub_Graph UD PageRankCent {}".format(sCounter))

        plt.subplot(223)
        sorted_hitshubsCent=sorted(hitshubCent.items(),key=itemgetter(1),reverse=True)
        print("SUB_UD_HitsHubsCent:\n{}\n\n".format(tool.printCentralityValues(sorted_hitshubsCent)))
        drawSubgraphs(subGraph,spos,hitshubCent,"Sub_Graph UD HitsHub {}".format(sCounter))

        plt.subplot(224)
        sorted_hitsauthorityCent=sorted(hitsauthorityCent.items(),key=itemgetter(1),reverse=True)
        print("SUB_UD_HitsAuthorityCent:\n{}\n\n".format(tool.printCentralityValues(sorted_hitsauthorityCent)))
        drawSubgraphs(subGraph,spos,hitsauthorityCent,"Sub_Graph UD HitsAuthority {}".format(sCounter))

        plt.savefig("subGraph{}_part_{}.png".format(sCounter,figCounter))
        plt.show()

        #--------------------------------------------------------------

        diameter=nx.diameter(subGraph)
        #(a) traidic closure, clustering coefficient, tansitivity- Approximation algorithm
        traidic_closure=nx.transitivity(subGraph)
        if len(cntComponents) not in subGraph:
            subGraphMatrix[len(cntComponents)]=["diameter:{}".format(diameter),
            "traidic_closure:{}".format(traidic_closure),"density:{}".format(nx.density(subGraph))]
        else:
            subGraphMatrix[len(cntComponents)].append(["diameter:{}".format(diameter),
            "traidic_closure:{}".format(traidic_closure),"density:{}".format(nx.density(subGraph))])

        sCounter+=1 #go to next subgraph
        figCounter=1 #reset figCounter to 1

    print (subGraphMatrix)
    os.chdir(jsonDir) #revert back to JSON directory
    return subGraphMatrix,reportStr


#-------------------Centrality Features--------------------------------
def getDegrees(G):
    degree_dict=dict(G.degree()) #version 2 support
    nx.set_node_attributes(G,degree_dict,'degree')
    sorted_degree_dict=sorted(degree_dict.items(),key=itemgetter(1),reverse=True)

    return degree_dict,sorted_degree_dict

def getDegreeCentralities(G):
    degreeCent_dict=nx.degree_centrality(G)
    nx.set_node_attributes(G,degreeCent_dict,"degreeCentrality")
    sorted_degreeCent_dict=sorted(degreeCent_dict.items(),key=itemgetter(1),reverse=True)
    return sorted_degreeCent_dict

def getEigenVectorCentralities(G):
    eigenvector_dict=nx.eigenvector_centrality(G)
    nx.set_node_attributes(G,eigenvector_dict,"eigenvector")
    sorted_eigenvector_dict=sorted(eigenvector_dict.items(),key=itemgetter(1),reverse=True)
    return sorted_eigenvector_dict

def getBetweennessCentralities(G):
    betweenness_dict=nx.betweenness_centrality(G)
    nx.set_node_attributes(G,betweenness_dict,"betweennesscentrality")
    sorted_betweenness_list=sorted(betweenness_dict.items(),key=itemgetter(1),reverse=True)
    return sorted_betweenness_list

def getHitBroker(topFiveImpIP_betCentrality,degree_dict):
    ''' Info about Broker:
    You can confirm from these results that some people,
    like Leavens and Penington, have high betweenness centrality
    but low degree. This could mean that these women were important brokers,
    connecting otherwise disparate parts of the graph.

    That is to say, simply knowing more people isn't everything.
    '''
    hitBroker=topFiveImpIP_betCentrality[0][0] #[('10.254.254.28', 0.3366013071895425), ('10.254.254.138', 0.14705882352941177)]
    for tb in topFiveImpIP_betCentrality:
        degree=degree_dict[tb[0]]
        if degree<degree_dict[hitBroker]:
            hitBroker=tb[0]
    return hitBroker

def getCommunities(G):
    communities=communityme.best_partition(G) #return dict #only for undirected graph, not for DiG
    nx.set_node_attributes(G,communities,"modularity")
    sorted_communities_list=sorted(communities.items(),key=itemgetter(1),reverse=True)
    return communities,sorted_communities_list

def formingModularities(communities):
    #community wise grouping
    modularityDict={}
    for k,v in communities.items():
        if v not in modularityDict:
            modularityDict[v]=[k]
        else:
            modularityDict[v].append(k)
    return modularityDict

def getPercommunityEigenInfluentials(G,modularityDict,rootGraphMatrix):
    if not rootGraphMatrix:
        rootGraphMatrix={}
    #a. Modularity/Community with sorted eigenvector value
    modularityEigenvector={}
    for k,v in modularityDict.items():
        modularityEigenvector[k]=sorted({n:round(G.node[n]['eigenvector'],2) for n in v}.items(),key=itemgetter(1),reverse=True)
    #print(modularityEigenvector)

    #a1. Detecting percommunity eigenvector topper-most influential
    rootGraphMatrix['perCommunityInfluential']=[]
    for community in modularityEigenvector:
        mostInfluentialPerCommunity=modularityEigenvector[community][0][0] #{0: [('10.1.40.113', 0.38), ('10.254.254.58', 0.3)]}
        rootGraphMatrix['perCommunityInfluential'].append({community:mostInfluentialPerCommunity})
    return rootGraphMatrix

def getPerCommunityHitBroker(G,modularity,rootGraphMatrix):
    if not rootGraphMatrix:
        rootGraphMatrix={}
    #b.Modularity with betweenness centrality
    modularityBetweennesscentrality={}
    for k,v in modularity.items():
        modularityBetweennesscentrality[k]=sorted({n:round(G.node[n]['betweennesscentrality'],2) for n in v}.items(),key=itemgetter(1),reverse=True)

    #b1. Detecting percommunity broker
    rootGraphMatrix['perCommunityHitBroker']=[]
    for community in modularityBetweennesscentrality:
        hitBrokerPerCommunity=modularityBetweennesscentrality[community][0][0]
        rootGraphMatrix['perCommunityHitBroker'].append({community:hitBrokerPerCommunity})
    return rootGraphMatrix

def getPerCommunityImpHub(G,modularity,rootGraphMatrix):
    #c. Modularity with hub- degreeCentralities
    modularityHub={}
    for k,v in modularity.items():
        modularityHub[k]=sorted({n:round(G.node[n]['degreeCentrality'],2) for n in v}.items(),key=itemgetter(1),reverse=True)

    #c1. Dectecting perCommunity inportant hub
    rootGraphMatrix['perCommunityImpHub']=[]
    for community in modularityHub:
        hubPerCommunity=modularityHub[community][0][0]
        rootGraphMatrix['perCommunityImpHub'].append({community:hubPerCommunity})
    return rootGraphMatrix


def createJSONFile(G,jsonDir,jsonFileName,matrix=None):
     with open(jsonDir+"/"+jsonFileName,'w') as out_file:
        if matrix==None:
            elementToDump=dict(G.nodes)
        else:
            elementToDump=matrix
        json.dump(elementToDump,out_file,sort_keys = True, indent = 4, ensure_ascii = False)

def exportGraphInfoIntoGephi(G,jsonDir,fileName):
    nx.write_gexf(G, jsonDir+"/"+fileName)

def exportGraphInfoIntoDotAndSaveAsImg(G,jsonDir,fileName):
    pos = nx.nx_agraph.graphviz_layout(G)
    nx.draw(G,pos=pos)
    write_dot(G,jsonDir+"/"+fileName)
    ##changes to working directory
    os.chdir(jsonDir)
    os.system('dot -Tps ip_network.dot -o ip_network.ps')

#-------------Community wise sorting with centrality values and saving into JSON and CSV files----------------
def getCommunityWiseGroupingWithCentralityValue(G,modularityGroupWiseDict,mode="Eigen"):
    updatedDict={}
    if mode=="Eigen":
        centralityDict=nx.eigenvector_centrality(G)
    elif mode=="Bet":
        centralityDict=nx.betweenness_centrality(G)
    elif mode=="Close":
        centralityDict=nx.closeness_centrality(G)

    #print(modularityGroupWiseDict)
    #print(eigenvectorDict)
    for gpID,ipList in modularityGroupWiseDict.items():
        updatedDict[gpID]={}
        for ip in ipList:
            updatedDict[gpID].update({ip:centralityDict[ip]})

    '''sortedUpdatedDict={}
    for gpID,ipCentralityDict in updatedDict.items():
        sortedUpdatedDict[gpID]=dict(sorted(ipCentralityDict.items(),key=itemgetter(1),reverse=True))
    return sortedUpdatedDict'''
    return updatedDict #removed sorted bcoz dict conversion here unsort it again

def ipSortingCommunityWiseJSONCSVgeneration(G,modularity,rootGraphMatrix,fromDir,toDir):
    communityAllCentralityDict={}
    csvDir=fromDir
    jsonDir=toDir
    modeList=["Eigen","Bet","Close"]
    for mode in modeList:
        communitySortDict=getCommunityWiseGroupingWithCentralityValue(G,modularity,mode) #we get dict return here
        rootGraphMatrix["community_{}".format(mode)]=communitySortDict
        os.chdir(jsonDir)
        jsonCommFileName="community_{}.json".format(mode)
        tool.dumpDictIntoJSON(communitySortDict,jsonCommFileName)

        csvCommFileName="community_{}.csv".format(mode)
        #os.chdir(csvDir)
        tool.loadJsonToCSV(jsonDir,csvDir,jsonCommFileName,csvCommFileName) #this one is giving error:

        communityAllCentralityDict[mode]=communitySortDict

    os.chdir(jsonDir)
    tool.dumpDictIntoJSON(communityAllCentralityDict,"communityAllCentrality.json")
    tool.loadJsonToCSV(jsonDir,csvDir,"communityAllCentrality.json","communityAllCentrality.csv")
    return rootGraphMatrix
#-------------------------------------------------------------------------

#-----------------------------------------------------------------------------------
def networkxSimulation(unalteredRepoDict,fromDir,toDir,ipListCSV,adjListCSV,gt,executionMode="log"): #fromDir=csvDir, toDir=jsonDir gt=GraphType
    scriptName=os.path.basename(__file__).split(".")[0]
    funcCallDict={}#0

    reportStr=""
    funcCallDict[scriptName]=[tool.__name__]#1
    tool.createDirectory(toDir) # we will save all the simulation result here in json files
    funcCallDict[tool.__name__]=[tool.createDirectory.__name__]#2

    #------------------BASIC PART-----------------------------------------
    print("BASIC PART")
    #P-1: Get the nodes, names and edges
    print("P-1: Get the nodes, names and edges")
    node_names,edges,nodes=tool.getTheNodesAndEdges(fromDir,ipListCSV,adjListCSV)
    funcCallDict[tool.__name__].append(tool.getTheNodesAndEdges.__name__)#3

    #P-2: NexworkX Graph Building
    print("#P-2: NexworkX Graph Building")
    funcCallDict[scriptName].append(netxGraphBuilding.__name__)#4
    G=netxGraphBuilding(node_names,edges,sGraph=None,graphType=gt) #change here for UD or DiG graph
    #node_names,edges,sGraph=None,graphType="UD"
    reportStr="{}\n".format(nx.info(G)) #remember [(1,2),(2,3),(1,3),(2,1)]-> DiG will show Edges=4, UD will show Edges=3

    #P-3: Adding attributes to nodes
    if executionMode=="log":
        print("#P-3: Adding attributes to nodes")
        funcCallDict[scriptName].append(netxGraphAddingAttributes.__name__)#5
        G=netxGraphAddingAttributes(G,nodes)

    #--------------------Connected Components Testing (Subgraph exists or not?)----------------------------------
    print("Connected Components Testing (Subgraph exists or not?)")
    #P-1 Network Density Calculation
    print("#P-1 Network Density Calculation")
    funcCallDict[scriptName].append(nx.__name__)#6
    density=nx.density(G) #Approximation algorithm, for this small network density should be small
    reportStr+="Network Density: {}\n".format(density)

    #P-2 Shortest Path Calculation for all nodes pairs and saving into "shortestPaths.txt"
    print('#P-2 Shortest Path Calculation for all nodes pairs and saving into "shortestPaths.txt"')
    funcCallDict[scriptName].append(shortestPathCalculationAndSavingToFile.__name__)#7
    shortestPathCalculationAndSavingToFile(unalteredRepoDict,G,node_names,"shortestPaths.txt") #../animalLogSimulation (should be)

    print("P-3 Checking the number of connected components in the graph-UD VS DiG graph")
    #P-3 Checking the number of connected components in the graph and if only one component then
    #calculate the diameter, else create subgraphs, traidic closure-(number of traingles possible)
    funcCallDict[scriptName].append(dealingWithRootGraph.__name__)#8
    rootGraphMatrix=dealingWithRootGraph(G,node_names)

    if not type(G)==nx.DiGraph and not nx.is_connected(G):
        funcCallDict[scriptName].append(dealingWithSubGraphs.__name__)#9
        subGraphMatrix,reportStr=dealingWithSubGraphs(G,toDir,fromDir,reportStr) #toDir=jsonDir, fromDir=csvDir
        rootGraphMatrix.update(subGraphMatrix)

    if type(G)==nx.DiGraph: #this is still in test phase, i am trying to use SCC for DiG subgraphs
        #find the strongly connected component subgraphs (Only for DiG)
        #In the mathematical theory of directed graphs, a graph is said to be
        #strongly connected or diconnected if every vertex is reachable from every other vertex.
        print("Its Directed Graph")
        funcCallDict[scriptName].append(dealingWithSubGraphs_SCC_DiG.__name__)#10
        scc_subGraphList,scc_subGraphLenList= dealingWithSubGraphs_SCC_DiG(G)
        netxSubGraphBuilding_SCC_DiG(G,scc_subGraphList,scc_subGraphLenList,toDir,fromDir)
        funcCallDict[scriptName].append(netxSubGraphBuilding_SCC_DiG.__name__)#11

    #-------------------------Degree Calculation and sorting-----------------
    #P-1 Degree
    funcCallDict[scriptName].append(getDegrees.__name__)#12
    degree_dict,sorted_degree_list=getDegrees(G) #function call
    topFiveImpIP_degree=sorted_degree_list[:5]

    #--------------Centralities (These are not saving into csv, but into ipMatrixJSON.json file)--------------------
    #P-1 Degree Centrality
    funcCallDict[scriptName].append(getDegreeCentralities.__name__)#13
    sorted_degCent_list=getDegreeCentralities(G) #function call
    topFiveImpIP_degCent=sorted_degCent_list[:5]
    rootGraphMatrix["Biggests Hubs"]=topFiveImpIP_degCent

    #P-2 Eigenvector centrality
    funcCallDict[scriptName].append(getEigenVectorCentralities.__name__)#14
    sorted_eigenvector_list=getEigenVectorCentralities(G) #function call
    topFiveImpIP_eigenVector=sorted_eigenvector_list[:5]
    rootGraphMatrix["Most Influentials"]=topFiveImpIP_eigenVector

    #P-3 Betweenness Centrality - Broker
    funcCallDict[scriptName].append(getBetweennessCentralities.__name__)#15
    sorted_betweenness_list=getBetweennessCentralities(G) #function call
    topFiveImpIP_betCentrality=sorted_betweenness_list[:5]
    rootGraphMatrix["Big Brokers"]=topFiveImpIP_betCentrality

    #P-4 Get Hit Broker
    funcCallDict[scriptName].append(getHitBroker.__name__)#16
    hitBroker=getHitBroker(topFiveImpIP_betCentrality,degree_dict)
    rootGraphMatrix['Root Hit Broker']=hitBroker
    '''What if you want to know which of the high betweenness centrality nodes had low degree? Identifying the key broker?
    Key broker characteristics: Higher betweenness centrality, lower degree, in this small network its difficult
    to find the key broker
    '''


    #---------------Finding per community Hubs,Influentials,brokers-----------------------------
    if not type(G)==nx.DiGraph:
        #P-1: Get the Communities
        funcCallDict[scriptName].append(getCommunities.__name__)#17
        communities,sorted_communities_list=getCommunities(G) #communities-->dict type
        communityCount=len(set(communities.values()))
        rootGraphMatrix["Total Communities:"]=communityCount #newly added
        reportStr+="Total communities found:{}\n".format(communityCount)

        #P-2:Create modularities- Community wise grouping and forming and return dictionary
        funcCallDict[scriptName].append(formingModularities.__name__)#18
        modularity=formingModularities(communities)

        #P-new: IP sorting with centrality values per community------------------------------------------
        funcCallDict[scriptName].append(ipSortingCommunityWiseJSONCSVgeneration.__name__)#19
        rootGraphMatrix=ipSortingCommunityWiseJSONCSVgeneration(G,modularity,rootGraphMatrix,fromDir,toDir)

        #P-3. Detecting percommunity eigenvector topper-most influential and saving into dict
        funcCallDict[scriptName].append(getPercommunityEigenInfluentials.__name__)#20
        rootGraphMatrix=getPercommunityEigenInfluentials(G,modularity,rootGraphMatrix)

        #P-4. Detecting percommunity broker
        funcCallDict[scriptName].append(getPerCommunityHitBroker.__name__)#21
        rootGraphMatrix=getPerCommunityHitBroker(G,modularity,rootGraphMatrix)

        #P-5. Dectecting perCommunity inportant hub
        funcCallDict[scriptName].append(getPerCommunityImpHub.__name__)#22
        rootGraphMatrix=getPerCommunityImpHub(G,modularity,rootGraphMatrix)


    #---Part7: Data Exporting in JSON----------------------
    #http://jsonviewer.stack.hu/#http://
    #https://www.sitepoint.com/demos/online-json-tree-viewer/#
    #https://codebeautify.org/
    #http://chris.photobooks.com/json/default.htm

    #7.1 Exposting dict(G.nodes) general info with node attributes into JSON
    funcCallDict[scriptName].append(createJSONFile.__name__)#23
    createJSONFile(G,toDir,'ipLogWithAttributes_General.json',matrix=None)

    #7.2 Exporting rootGraphMatrix into JSON
    createJSONFile(G,toDir,"ipGraphMatrx.json",matrix=rootGraphMatrix)
    funcCallDict[scriptName].append(createJSONFile.__name__)#24 repeat

    if not type(G)==nx.DiGraph:
        print("Generating gexf and dot image files")
        #7.3 Exporting dict(G.nodes) general info with attributes into Gephi in .gexf format
        #print(G.nodes)
        funcCallDict[scriptName].append(exportGraphInfoIntoGephi.__name__)#25
        exportGraphInfoIntoGephi(G,toDir,'ip_network.gexf') #here, toDir=jsonDir

        #7.4 Exporting G into dot file
        #7.5 Dot file to ps file generation-require python to run linux commands from program
        #dot -Tps ip_network.dot -o ip_network.ps
        funcCallDict[scriptName].append(exportGraphInfoIntoDotAndSaveAsImg.__name__)#26
        exportGraphInfoIntoDotAndSaveAsImg(G,toDir,"ip_network.dot")

    return reportStr,funcCallDict


def main():
    '''config = Config(max_depth=3)

    graphviz=GraphvizOutput()
    graphviz.output_file="networkxSimulation.png"

    with PyCallGraph(output=graphviz,config=config):'''

    jsonDir="/home/jahid/Desktop/AllMyWorks/InformationSecurity/google/google-python-exercises/logpuzzle/logSolverMyCodeRepo/simulationResults/outputGenerated/animalLogSimulation/JSON_Files"
    csvDir="/home/jahid/Desktop/AllMyWorks/InformationSecurity/google/google-python-exercises/logpuzzle/logSolverMyCodeRepo/simulationResults/outputGenerated/animalLogSimulation/CSV_Files"

    unalteredRepoDict="/home/jahid/Desktop/AllMyWorks/InformationSecurity/google/google-python-exercises/logpuzzle/logSolverMyCodeRepo/simulationResults/outputGenerated/animalLogSimulation"
    #toDir=jsonDir
    #fromDir=csvDir

    ipListCSV="animalCSVGeneral.csv"
    adjListCSV="adjListAnimalCSV_final.csv"

    #Call using pyCallGraph
    #graphviz=GraphvizOutput()
    #graphviz.output_file="{}.png".format(networkxSimulation.__name__)
    #with PyCallGraph(output=graphviz):
    report,funcCallDict=networkxSimulation(unalteredRepoDict,csvDir,jsonDir,ipListCSV,adjListCSV,"UD")

    print("Report By NetworkX:\n--------------------------\n")
    print(report)
    pprint.pprint(funcCallDict)
    #change the working directory back at the end


    os.chdir("/home/jahid/Desktop/AllMyWorks/InformationSecurity/google/google-python-exercises/logpuzzle/logSolverMyCodeRepo/source/")

if __name__ == '__main__':
    main()