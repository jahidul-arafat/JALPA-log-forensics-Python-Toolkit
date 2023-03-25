from __future__ import division
import os
import re
import sys
import urllib
import csv
import json
import random
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pylab import rcParams
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


#https://www.zamzar.com/convert/csv-to-html/
#--------------------old tools--------------------------------
def isPathExists(dirname):
    return os.path.isdir(dirname)

#5a. Action upon the file not exists
def checkPathExists(dirname):
    if not isPathExists(dirname):
        os.makedirs(dirname)
    else:
        print("Directory# {} already exists. (C)ontinure or (Q)uit?"\
        .format(dirname))
    response=input("Enter your choice: 1.(C)ontinure\t 2.(Q)uit:\t ")
    return response

def writeReportToFile(reportFile,reportStr):
    fp=open(reportFile,'w')
    fp.write(reportStr)
    fp.close()


def saveToDirectory(toDir,fileName,fileContent,mode="w"):
    if not isPathExists(toDir):
        os.mkdirs(toDir)
    with open(os.path.join(toDir,fileName), mode) as file1:
        file1.write(fileContent)

def createDirectory(toDir):
    if not isPathExists(toDir):
        os.makedirs(toDir)


#-------------------Updating the tools 17 June, 2018 3.43PM---------------------
#@tool
def printCentralityValues(inputList):
    outputStr=""
    for node,value in inputList:
        outputStr+="{}->{}\n".format(node,round(value,5))
    return outputStr

#@tool
def dummyNodesEdges():

    nodeList=[1,2,3,4,5,6,7,8,9,10,11]
    edgeList=[(2,3), (4, 1), (4, 2), (5, 2), (5, 4),
                    (5, 6), (6, 2), (6, 5), (7, 2), (7, 5), (8, 2),
                    (8, 5), (9, 2), (9, 5), (10, 5), (11, 5)]
    '''
    nodeList=['A','B','C','D','E','F','X']
    edgeList=[('A','B'),('A','C'),('B','C'),('C','X'),('X','D'),('D','E'),('D','F'),('E','F')]
    '''

    return nodeList,edgeList

#@tool
def getCoordinates(nodeList):
    #------------Creating the random x-y coordinates-----------------------
    cords_set = set()
    while len(cords_set) < len(nodeList):
        x, y = 1, 0
        while (x, y) == (1, 0): #means dont accept (1,0)
            x, y = round(random.uniform(0, 1),2), round(random.uniform(0, 1),2)
        # that will make sure we don't add (7, 0) to cords_set
        cords_set.add((x, y))
    cords_list=list(cords_set)
    return cords_list
    #----------------------------------------------------------------------



#@tool
def operatingChoice():
    response=input("Enter your choice: 1.Using Dummy Data ('D')\t 2.Using Original NX Data ('O')\t")
    return response.lower()

#@tool
def allInOneDict(inputDict,toDict={}):
    for node,value in inputDict.items():
        if not node in toDict:
            toDict[node]=[value]
        else:
            toDict[node].append(value)
    return toDict

#@tool
def writingIntoCSV(sortedCentralityDict,fileName):
    csv=open(fileName,'w')
    columnTitleRow="IP,DC(UD-G), DC(DiG), DC(DiG-In), DC(DiG-Out), BC(UD-G), BC(DiG), EV(UD-G), EV(DiG), CC(UD), CC(DiG),KC(UD),KC(DiG),PR(UD),PR(DiG),HITSHUBS(DiG),HITSAUTHORITIES(DiG)\n"
    csv.write(columnTitleRow)
    for node,value in sortedCentralityDict.items():
        row="{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".\
        format(
            node,#1 IP
            round(sortedCentralityDict[node][0],2),#2 DC(UD)
            round(sortedCentralityDict[node][1],2),#3 DC(DiG)
            round(sortedCentralityDict[node][2],2),#4 DC(DiG-IN)
            round(sortedCentralityDict[node][3],2),#5 DC(DiG-OUT)
            round(sortedCentralityDict[node][4],2),#6 BC(UD)
            round(sortedCentralityDict[node][5],2),#7 BC(DiG)
            sortedCentralityDict[node][6],#8 EV(UD)
            sortedCentralityDict[node][7],#9 EV(DiG)
            round(sortedCentralityDict[node][8],5), #10 CC(UD)
            round(sortedCentralityDict[node][9],5), #11 CC(DiG)
            sortedCentralityDict[node][10], #12 KC(UD)
            sortedCentralityDict[node][11], #13 KC(DD)
            sortedCentralityDict[node][12], #14 PR(UD)
            sortedCentralityDict[node][13], #15 PR(DiG)
            sortedCentralityDict[node][14], #16 HITSHUBS(DiG)
            sortedCentralityDict[node][15] #17 HITSAUTHORITIES(DiG)

        )
        csv.write(row)
    csv.close()

def writingIntoCSV_funcCall(funcList,fileName):
    csv=open(fileName,"w")
    columnTitleRow="FuncName\n"
    csv.write(columnTitleRow)
    for func in funcList:
        row="{}\n".format(func)
        csv.write(row)
    csv.close()


#@tool
def dumpingIntoJSON(G,fileName):
     with open(fileName,'w') as out_file:
        json.dump(dict(G.nodes),out_file,sort_keys = True, indent = 4, ensure_ascii = False)

def dumpDictIntoJSON(inputDict,fileName):
    with open(fileName,'w') as out_file:
        json.dump(inputDict,out_file,sort_keys = True, indent = 4, ensure_ascii = False)



#@tool
def getTheNodesFromCSV(nodeCSVFile):

    #Getting the nodes or ips
    with open(nodeCSVFile, 'r') as nodecsv:
        nodereader=csv.reader(nodecsv)
        nodeList=[n for n in nodereader][1:] #1: bcoz first line in the csv file is titles

    return nodeList

#@tool
def loadJsonToDict(fromDir,jsonFileName):
    os.chdir(fromDir)
    with open(jsonFileName) as fp:
        dictData=json.load(fp)
    return dictData

#@tool
def loadJsonToCSV(jsonDir,csvDir,jsonFileName,csvFileName):
    reload(pd) #I was facing the typeerror, value error, thats why added it a pandas was having trouble in loading the JSON contents
    #but reload() cant solve 'valueError: Arrays must be of same length'
    os.chdir(jsonDir)
    df=pd.read_json(jsonFileName)

    #data = pd.DataFrame.from_dict(df, orient='index')
    #print(data)

    os.chdir(csvDir)
    df.to_csv(csvFileName)

def getTheNodesAndEdges(fromDir,ipListCSV,adjListCSV): #..animalLogSimulation/CSV_Files
    ipListCSV=fromDir+"/"+ipListCSV ##..animalLogSimulation/CSV_Files/animalCSVGeneral.csv
    adjListCSV=fromDir+"/"+adjListCSV ##..animalLogSimulation/CSV_Files/adjListAnimalCSV_final.csv

    #Getting the nodes or ips
    with open(ipListCSV, 'r') as nodecsv:
        nodereader=csv.reader(nodecsv)
        nodes=[n for n in nodereader][1:] #1: bcoz first line in the csv file is titles

    node_names=[n[0] for n in nodes] #reading the ip address a t n[0] index in the nodes

    #Reading the edgecsv file and reading the tuples from line 2, bcoz first line is title
    with open(adjListCSV, 'r') as edgecsv:
        edgereader=csv.reader(edgecsv)
        edges=[tuple(e) for e in edgereader][1:]
    return node_names,edges,nodes #you will get the IP names from here

#@This will be used in ipLocationTracker.py
def getTheIPs(fromDir,ipListCSV): #..animalLogSimulation/CSV_Files
    ipListCSV=fromDir+"/"+ipListCSV ##..animalLogSimulation/CSV_Files/animalCSVGeneral.csv
    with open(ipListCSV, 'r') as nodecsv:
        nodereader=csv.reader(nodecsv)
        nodes=[n for n in nodereader][1:] #1: bcoz first line in the csv file is titles

    ip_names=[n[0] for n in nodes] #reading the ip address a t n[0] index in the nodes
    return ip_names


def dictMerge(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, [])
            dictMerge(value, node)
        else:
            destination[key]=value

    return destination

def dictMergerHavingLists(source,destination):
    for key,value in source.items():
        if isinstance(value,list):
            if key in destination:
                destination[key].extend(value)
            else:
                destination[key]=value
    return destination


def mergingJSONs(fileToBeMerged_1,fileToBeMerged_2,jsonDir):
    os.chdir(jsonDir)
    inputFile_1=loadJsonToDict(jsonDir,fileToBeMerged_1) #tool
    inputFile_2=loadJsonToDict(jsonDir,fileToBeMerged_2) #tool

    #step-2: merge the dicts
    mergedDict=dictMerge(inputFile_1,inputFile_2) #tool

    #Step-3: Writing the merged dict into mergedJSON.json file
    with open("mergedJSON.json",'w') as out_file:
        json.dump(mergedDict,out_file,sort_keys = True, indent = 4, ensure_ascii = False)


def draw(G, pos, measures, measure_name):
    #os.chdir("/home/jahid/Desktop/AllMyWorks/InformationSecurity/google/google-python-exercises/logpuzzle/logSolverMyCodeRepo/simulationResults/outputGenerated/animalLogSimulation/JSON_Files")
    nodes = nx.draw_networkx_nodes(G, pos, node_size=150, cmap=plt.cm.spring,
                                   node_color=measures.values(),
                                   nodelist=measures.keys())
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.02, linscale=10))

    labels = nx.draw_networkx_labels(G, pos)
    edges = nx.draw_networkx_edges(G, pos)

    plt.title(measure_name)
    plt.colorbar(nodes)
    #plt.xlabel("x-cord")
    #plt.ylabel("y-cord")
    plt.axis('off')
    plt.grid(True)
    #plt.show()


def pyCallGraph(toDir,funcName,funcFull=None):
    os.chdir(toDir)
    graphviz=GraphvizOutput()
    graphviz.output_file="{}.png".format(funcName)
    if not funcFull:
        with PyCallGraph(output=graphviz):
            funcFull



