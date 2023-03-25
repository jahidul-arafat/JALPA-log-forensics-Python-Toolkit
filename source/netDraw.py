#when you run this program, following files and folders will be updated
'''
https://aksakalli.github.io/2017/07/17/network-centrality-measures-and-their-visualization.html
http://programminghistorian.github.io/ph-submissions/lessons/published/exploring-and-analyzing-network-data-with-python

Objective: This program draws the main Graph
Files:
    1. JSON_Files>Graphs
    2. JSON_Files>mergedJSON.json
    3. JSON_Files>allCentralities.json
    4. CSV_Files>allCentralities.csv

Remember:
This program generates:
    1. root graph centralities (for both directed and undirected graph): degreeCent, betCent, closeCent, eigenCent
    2. subgraph centralities are not handled here, these are handled in (networkxSimulation.py)
    3. this pg generates (matplotlib plt graphs) for those centralities
    4. Also generates Graph folder inside JSON_Files folder
    5. write the updatedAllCentralitiesDict into CSV-Files>allCentralities.csv
    6. read the nodeLists from allCentralities.csv and load these into allCentralitites.json
    7. Then merge the allCentralities.json and old ipLogWithAttributes_General.json into mergedJSON.json
    8. Finally, store the infos of mergedJSON.json into CSV_Files>mergedCSV.csv using pandas module

'''
__author__ = """Jahid Arafat (jahidapon@gmail.com)"""
#    Copyright (C) 2018 by
#    Jahid Arafat <jahidapon@gmail.com>
#    All rights reserved.
#    BSD license.

import pprint
import logPuzzleSupportTools as tool
import graphPreparation as gprep
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy,scipy
import random
from operator import itemgetter
import os
from pylab import rcParams
import json, csv
import centrality

from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
 #I have moved the draw in tool bcoz of error of networkxSimulation.py


#Subgraph katz,pagerank,hits hubs and authorities --into figure(2)
#Subgraph centralitites csv,json
#Module Centralities
#Permodule csv,json and plt
#---------------------------------------------------------------------------------
def netDrawSetUpAndExecution(jsonDir,csvDir,sourceCodeDir,ipListCSV,adjListCSV,executionMode="log"):
    scriptName=os.path.basename(__file__).split(".")[0] #this will remove .py from test.py
    funcCallDict={}#0

    print("Into netDraw")

    fromDir=csvDir

    funcCallDict[scriptName]=[tool.__name__]#1
    choice=tool.operatingChoice() #tool
    funcCallDict[tool.__name__]=[tool.operatingChoice.__name__]#2

    if choice=='d':#Dummy Data
        nodeList,edgeList=tool.dummyNodesEdges() #tool
        funcCallDict[tool.__name__].append(tool.dummyNodesEdges.__name__)#3
    else:
        nodeList,edgeList,nodes=tool.getTheNodesAndEdges(csvDir,ipListCSV,adjListCSV) #networkx simulator
        funcCallDict[tool.__name__].append(tool.getTheNodesAndEdges.__name__)#4

    cords_list=tool.getCoordinates(nodeList) #tool
    funcCallDict[tool.__name__].append(tool.getCoordinates.__name__)#5

    #-----------Prepating Directed Graph-----------------------------------
    funcCallDict[scriptName].append(gprep.__name__)#6
    DiG,dpos=gprep.preparingNXGraph_directed(nodeList,edgeList,cords_list) #graph preparation
    funcCallDict[gprep.__name__]=[gprep.preparingNXGraph_directed.__name__]#7

    #------------Preparing Undirected Graph--------------------------------
    G,pos=gprep.preparingNXGraph_undirected(nodeList,edgeList) #graph preparation
    funcCallDict[gprep.__name__].append(gprep.preparingNXGraph_undirected.__name__)#8

    #Showing the degree centrality graph

    #Call the Degree_Centrality Function and show the plt -Important Hubs
    funcCallDict[scriptName].append(centrality.__name__)#9
    updatedAllInOneDict=centrality.degreeCentrality(G,pos,DiG,dpos,jsonDir)
    funcCallDict[centrality.__name__]=[centrality.degreeCentrality.__name__]#10

    #Call the Betweenness Centrality Function and show the plt -
    #How many shortest paths goes through it,bridge,broker
    updatedAllInOneDict=centrality.betweennessCentrality(G,pos,DiG,dpos,jsonDir,updatedAllInOneDict)
    funcCallDict[centrality.__name__].append(centrality.betweennessCentrality.__name__)#11

    #Call the Closeness Centrality Function and show the plt -
    #the sum of the length of the shortest paths between node(action) to all other nodes- finding actors who are in best placed to influence the entire network more quickly
    updatedAllInOneDict=centrality.closenessCentrality(G,pos,DiG,dpos,jsonDir,updatedAllInOneDict)
    funcCallDict[centrality.__name__].append(centrality.closenessCentrality.__name__)#12

    #Call the Eigenvector Centrality Function and show the plt -
    #problem: nodes with zero in dergee, ev=0, consider importance of its fnds
    #Best for DiG
    updatedAllInOneDict=centrality.eigenvectorCentrality(G,pos,DiG,dpos,jsonDir,updatedAllInOneDict)
    funcCallDict[centrality.__name__].append(centrality.eigenvectorCentrality.__name__)#13

    #Call the Katz Centrality Function and show the plt -
    #solved the problem of eigenvector
    #Best for DiG
    updatedAllInOneDict=centrality.katzCentrality(G,pos,DiG,dpos,jsonDir,updatedAllInOneDict)
    funcCallDict[centrality.__name__].append(centrality.katzCentrality.__name__)#14

    #Call the Pagerank Centrality Function and show the plt -
    #pagerank solves the problem of katz, 3 gets ints importance back in dummy data
    #Best for DiG
    updatedAllInOneDict=centrality.pagerankCentrality(G,pos,DiG,dpos,jsonDir,updatedAllInOneDict)
    funcCallDict[centrality.__name__].append(centrality.pagerankCentrality.__name__)#15

    #Call the HITS Hubs and Authority function and show the plt -to get the impact of nodes which have zero in-degree nodes
    #i.e. a review paper citing lots of papers
    #Node getting most citation is the Authority node
    #Node citing most is the Hub node
    updatedAllInOneDict=centrality.hitsHubsAndAuthorities(DiG,dpos,jsonDir,updatedAllInOneDict)
    funcCallDict[centrality.__name__].append(centrality.hitsHubsAndAuthorities.__name__)#16

    #print(updatedAllInOneDict)

    #Sort the updatedAllInOneDict
    sortedUpdateAllInOneDict=dict(sorted(updatedAllInOneDict.items(),key=itemgetter(1)))


    #Writing the updatedAllInOneDict centrality scores into CSV sheet
    csvFileName="allCentralities.csv"
    tool.writingIntoCSV(sortedUpdateAllInOneDict,os.path.join(csvDir,csvFileName)) #tool
    funcCallDict[tool.__name__].append(tool.writingIntoCSV.__name__)#17


    #get the nodelist from "allCentralities.csv"
    os.chdir(csvDir)
    nodeList=tool.getTheNodesFromCSV(csvFileName) #tool
    funcCallDict[tool.__name__].append(tool.getTheNodesFromCSV.__name__)#18

    #adding attributes to nodes, Dumping into JSON and generating allCentralities.json
    jsonFileName="allCentralities.json"
    gprep.addingAttributesToNodes(G,nodeList,jsonDir,jsonFileName) #this has called tool.dumpingIntoJSON() function
    funcCallDict[gprep.__name__].append(gprep.addingAttributesToNodes.__name__)#19

    #Merging to different json files into a single file
    #step1. Load the json files into dict
    fileToBeMerged_1="allCentralities.json"
    if executionMode=="log": #this is added to handle the funcCallGraphs and its json, csv generation
        fileToBeMerged_2="ipLogWithAttributes_General.json"
    else:
        fileToBeMerged_2=fileToBeMerged_1

    tool.mergingJSONs(fileToBeMerged_1,fileToBeMerged_2,jsonDir)
    funcCallDict[tool.__name__].append(tool.mergingJSONs.__name__)#20


    #now Generate the mergedCSV.csv from mergedJSON.json file
    #For that we are gonna use pandas
    #sudo apt-get install python-pandas
    tool.loadJsonToCSV(jsonDir,csvDir,"mergedJSON.json","mergedCSV.csv")
    funcCallDict[tool.__name__].append(tool.loadJsonToCSV.__name__) #21

    #Changed back to the source directory
    os.chdir(sourceCodeDir)
    return funcCallDict


def main():
    csvDir="/home/jahid/Desktop/AllMyWorks/InformationSecurity/google/google-python-exercises/logpuzzle/logSolverMyCodeRepo/simulationResults/outputGenerated/placeLogSimulation/CSV_Files"
    jsonDir="/home/jahid/Desktop/AllMyWorks/InformationSecurity/google/google-python-exercises/logpuzzle/logSolverMyCodeRepo/simulationResults/outputGenerated/placeLogSimulation/JSON_Files"
    sourceCodeDir="/home/jahid/Desktop/AllMyWorks/InformationSecurity/google/google-python-exercises/logpuzzle/logSolverMyCodeRepo/source"

    ipListCSV="animalCSVGeneral.csv"
    adjListCSV="adjListAnimalCSV_final.csv"

    #graphviz=GraphvizOutput()
    #graphviz.output_file="{}.png".format(netDrawSetUpAndExecution.__name__)
    #with PyCallGraph(output=graphviz):
    funcCallDict=netDrawSetUpAndExecution(jsonDir,csvDir,sourceCodeDir,ipListCSV,adjListCSV)
    pprint.pprint(funcCallDict)


if __name__ == '__main__':
    main()
