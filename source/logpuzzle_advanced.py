from __future__ import division
__author__ = """Jahid Arafat (jahidapon@gmail.com)"""
#    Copyright (C) 2018 by
#    Jahid Arafat <jahidapon@gmail.com>
#    All rights reserved.
#    BSD license.

import os
import re
import sys
import urllib
import emailVarificationTool as ev
import emailManupulator as em
import networkGraph as ng
import imageDownloader as imgD
import ipFetchingAdjTableGenerator as ipf
import logPuzzleSupportTools as tool
import csvGenerator as csv
import adjListToCSVConversion as adjCSVCoverter
import networkxSimulation as netx
import netDraw
import ipLocationTracker as ipTracker
import generateHTMLFromJSON as genHTJS
import pprint

step=1

def stepIncrement():
    global step
    step=step+1


def mainLogMachine():
    funcCallDict={}#0
    scriptName=os.path.basename(__file__).split(".")[0] #this will remove the .py from logpuzzle_advanced.py

    toDir="/home/jahid/Desktop/AllMyWorks/InformationSecurity/google/google-python-exercises/logpuzzle/logSolverMyCodeRepo/simulationResults/outputGenerated"
    #outputFolderName="customLogSimulation"
    outputFolderName="ThesisGroup03"
    toDir=toDir+"/"+outputFolderName #../animalLogSimulation (This directory was not changed further)
    unalteredRepoDir=toDir #../animalLogSimulation

    print("Simulating Project: {}\n------------------------\n:".format(outputFolderName))


    #Files where we are saving our outputs
    domainReportFile="domainReport.txt"
    ipReportFile="ipReport.txt"
    networkReportFile="networkReport.txt"

    #sourceLogFile="animal_code.google.com"
    #make sure there is no space at the end of your csv file, otherwise the adjTable creation error will happen.
    sourceLogFile="/home/jahid/Desktop/AllMyWorks/InformationSecurity/google/google-python-exercises/logpuzzle/logSolverMyCodeRepo/source log/place_code.google.com"

    imageDownloadDir=toDir+"/"+"imgForensics" #../animalLogSimulation/imgForensics
    imageReportFile="imageReport.txt"
    csvFile="animalCSVGeneral.csv" #this will go to the networkx simulator
    tempCsvAdjListFile="adjListAnimalCSV_temp.csv" #this will be deleted once after created
    finalCsvAdjListFile="adjListAnimalCSV_final.csv"#this will go to the networkx simulator


    #------------------------------
    domainReportStr=""
    ipReportStr=""
    imageReportStr=""
    #------------------------------

    #Step-1: Extract the images urls from the source file
    funcCallDict[scriptName]=[imgD.__name__]#1
    funcCallDict[imgD.__name__]=[imgD.read_urls.__name__]#2
    funcCallDict[scriptName].append(tool.__name__)#3
    funcCallDict[tool.__name__]=[tool.checkPathExists.__name__]#4
    funcCallDict[imgD.__name__].append(imgD.download_images.__name__)#5
    funcCallDict[imgD.__name__].append(imgD.numberOfImageFileRetrieved.__name__)#6
    funcCallDict[tool.__name__].append(tool.saveToDirectory.__name__)#7
    funcCallDict[scriptName].append(stepIncrement.__name__)#8

    img_urls=imgD.read_urls(sourceLogFile)
    response=tool.checkPathExists(imageDownloadDir)
    if response.lower().startswith('c'):
        imgD.download_images(img_urls,imageDownloadDir)
    imageFileCount=imgD.numberOfImageFileRetrieved(imageDownloadDir)

    imageReportStr+="Image URLS\n----------\n{}".format("\n".join(img_urls))

    imageReportStr+="\n\nNumber of Image File recovered: "+str(imageFileCount)

    print("Step {}->Generating image file: {}".format(step,imageReportFile))
    stepIncrement()
    tool.saveToDirectory(toDir,imageReportFile,imageReportStr) #../animalLogSimulation

    #Step-2: get all the emails
    funcCallDict[scriptName].append(em.__name__)#9
    funcCallDict[em.__name__]=[em.getTheEmails.__name__]#10
    funcCallDict[em.__name__].append(em.emailsWeightImportance.__name__)#11
    funcCallDict[em.__name__].append(em.getEmailListStrVersion.__name__)#12
    funcCallDict[em.__name__].append(em.domainSplitting.__name__)#13

    allEmails, setEmails=em.getTheEmails(sourceLogFile)
    emailWeights=em.emailsWeightImportance(allEmails,setEmails)
    emailStr=em.getEmailListStrVersion(sourceLogFile)
    domainStr,domainList=em.domainSplitting(setEmails)


    domainReportStr+="The Emails are:\n-----------------\n"
    domainReportStr+=emailStr+"\n\n"
    domainReportStr+="The Domains are: \n------------------\n"+domainStr

    #Step-3: Verifying emails and domains and writing into domainReportStr
    funcCallDict[scriptName].append(stepIncrement.__name__) # 14 (Repeat) #if not stepIncrement.__name__ in funcCallDict[scriptName]
    funcCallDict[scriptName].append(ev.__name__)#15
    funcCallDict[ev.__name__]=[ev.emailValidityChecker.__name__]#16
    funcCallDict[scriptName].append(stepIncrement.__name__) # 17 (Repeat)
    funcCallDict[tool.__name__].append(tool.saveToDirectory.__name__)#18


    print("{} Domains Detected: {}".format(len(domainList),domainList))
    response=input("Do you want to verify emails and domains: 1.(Y)es\t 2.(N)o:\t ")
    if response.lower().startswith('y'):
        print("Step {}->Veryfying the emails and domains......".format(step))
        stepIncrement()
        emailValidityDict=ev.emailValidityChecker(setEmails)

        domainReportStr+="\n\nEmail Validity Checking:\n-----------------\n"+str(emailValidityDict)
        print("\nStep {}->Generating domainReportFile: {}".format(step,domainReportFile))
        stepIncrement()
        tool.saveToDirectory(toDir,domainReportFile,domainReportStr) #../animalLogSimulation

    #Step-4: Generating IP reports
    funcCallDict[scriptName].append(ipf.__name__)#19
    funcCallDict[ipf.__name__]=[ipf.fetchIpFromLog.__name__]#20
    funcCallDict[tool.__name__].append(tool.saveToDirectory.__name__)#21
    funcCallDict[scriptName].append(stepIncrement.__name__)#22

    ipReportStr+="IP Addressed Fetched:\n------------------\n"+ipf.fetchIpFromLog(sourceLogFile)
    print("\nStep {}->Generating ipReportFile: {}".format(step,ipReportFile))
    stepIncrement()
    tool.saveToDirectory(toDir,ipReportFile,ipReportStr) #../animalLogSimulation

    #Step-5: Generating the IP Adjacency Table from source text each line testing
    funcCallDict[ipf.__name__].append(ipf.generateIpAdjacencyTable.__name__)#23

    adjTab=ipf.generateIpAdjacencyTable(sourceLogFile)
    #print(adjTab) #I will use this adjTab later to get the ips and to get the IP locations and IPLocation.csv and IPLocation.json

    #Step-6: Drawing the network Graph using HTML, Django
    funcCallDict[scriptName].append(stepIncrement.__name__)#24
    funcCallDict[scriptName].append(ng.__name__)#25
    funcCallDict[ng.__name__]=[ng.networkGraphVisualization.__name__]#26

    print("\nStep {}->Drawing the network Graph".format(step))
    stepIncrement()
    networkReport=ng.networkGraphVisualization(toDir,adjTab) #../animalLogSimulation ###../animalLogSimulation/networkGraphLogForensics

    #Step-7: Generating network report
    funcCallDict[scriptName].append(stepIncrement.__name__)#27
    funcCallDict[tool.__name__].append(tool.saveToDirectory.__name__)#28

    print("\nStep {}->Generating network Report: {}".format(step,networkReportFile))
    stepIncrement()
    tool.saveToDirectory(toDir,networkReportFile,networkReport) #../animalLogSimulation

    #Step-8: Generating CSV file from source log
    funcCallDict[scriptName].append(stepIncrement.__name__)#29
    funcCallDict[scriptName].append(csv.__name__)#30
    funcCallDict[csv.__name__]=[csv.csvGenerator.__name__]#31

    toDirCSV=toDir+"/"+"CSV_Files" #../animalLogSimulation/CSV_Files
    print("\nStep {}->Generating CSV file from sourceLog: {}".format(step,csvFile)) #csvFile="animalCSVGeneral.csv"
    stepIncrement()
    csvGenerated=csv.csvGenerator(sourceLogFile,toDirCSV,csvFile)
    #wrote to: ../animalLogSimulation/CSV_Files/animalCSVGeneral

    #Step-9:networkxSimulation.py call--> Generating adjListToCSV file from adjacent list of sourceLogFile, check duplicates
    #csv contents and remove the temp file after operation
    funcCallDict[scriptName].append(adjCSVCoverter.__name__)#32
    funcCallDict[adjCSVCoverter.__name__]=[adjCSVCoverter.adjListToCSVConverter.__name__]#33
    funcCallDict[adjCSVCoverter.__name__].append(adjCSVCoverter.removeDuplicatedCSVContents.__name__)#34
    funcCallDict[adjCSVCoverter.__name__].append(adjCSVCoverter.removeAFile.__name__)#35
    funcCallDict[scriptName].append(stepIncrement.__name__)#36

    print("\nStep {}->Generating adjListToCSV file from adjacent list of sourceLogFile: {}".\
    format(step,finalCsvAdjListFile)) #adjListAnimalCSV_final.csv
    adjCSVCoverter.adjListToCSVConverter(adjTab,toDirCSV,tempCsvAdjListFile)#../animalLogSimulation/CSV_Files #
    adjCSVCoverter.removeDuplicatedCSVContents(toDirCSV,tempCsvAdjListFile,finalCsvAdjListFile)#../animalLogSimulation/CSV_Files #adjListAnimalCSV_temp.csv #adjListAnimalCSV_final.csv
    adjCSVCoverter.removeAFile(toDirCSV,tempCsvAdjListFile) #adjListAnimalCSV_temp.csv
    stepIncrement()

    #-------------------
    csvDir=toDirCSV #../animalLogSimulation/CSV_Files
    jsonDir=unalteredRepoDir+"/"+"JSON_Files" #../animalLogSimulation/JSON_Files
    sourceCodeDir="/home/jahid/Desktop/AllMyWorks/InformationSecurity/google/google-python-exercises/logpuzzle/logSolverMyCodeRepo/source"

    ipListCSV=csvFile #animalCSVGeneral.csv #_(copy)
    adjListCSV=finalCsvAdjListFile #"adjListAnimalCSV_final.csv" #_(copy)
    #ipListCSV="animalCSVGeneral_(copy).csv"
    #adjListCSV="adjListAnimalCSV_final_(copy).csv"


    #------------------------

    #-----Set the mode of executions---------------
    executionModes=["DiG","UD"]

    #----------------------------------------
    for mode in executionModes:
        funcCallDict[scriptName].append(netx.__name__)#37
        funcCallDict[netx.__name__]=[netx.networkxSimulation.__name__]#38
        funcCallDict[tool.__name__].append(tool.saveToDirectory.__name__)#39
        funcCallDict[scriptName].append(stepIncrement.__name__)#40

        print("Executing Mode: {}".format(mode))
        #Step-10: Generating Graph all attributes 02 json files using netx
        print("\nStep {}-->Generating 02 JSON, 1 Gephi, 1 Dot and 1 Dot>PS Files using netX".format(step))
        netReportX,netxFuncCallDict=netx.networkxSimulation(unalteredRepoDir,csvDir,jsonDir,ipListCSV,adjListCSV,mode) #Graph type, set the user graph type here DiG vs UD
        tool.saveToDirectory(toDir,networkReportFile,netReportX,mode="a")
        stepIncrement()

    #Step-11: NetDraw, allCentralititesCSV, allCentralitiesJSON, Merging AllCentralititesJSON and general
    #feature JSON into merged JSON, saving the picture of centralities
    funcCallDict[scriptName].append(netDraw.__name__)#41
    funcCallDict[netDraw.__name__]=[netDraw.netDrawSetUpAndExecution.__name__]#42

    netDrawReadme="Here in NetDraw, allCentralititesCSV, allCentralitiesJSON, Merging AllCentralititesJSON and generalfeature JSON into merged JSON, saving the picture of centralities"
    print("\nStep {}-->{}".format(step,netDrawReadme))

    netDrawFuncCallDict=netDraw.netDrawSetUpAndExecution(jsonDir,csvDir,sourceCodeDir,ipListCSV,adjListCSV)#waring: from pylab import rcParams doesnt work from here, plz run netDraw directly


    #Step-12: Getting the IPLocation Informations, generating ipLocInfo.json and ipLocInfo.csv
    funcCallDict[scriptName].append(ipTracker.__name__)#43
    funcCallDict[ipTracker.__name__]=[ipTracker.IPLocationFinderUsingIPAPImodule.__name__]#44
    funcCallDict[scriptName].append(stepIncrement.__name__)#45

    print("\nStep {}-> Getting the IP Location information".format(step))
    #ipDB1="/home/jahid/Desktop/AllMyWorks/InformationSecurity/google/google-python-exercises/logpuzzle/logSolverMyCodeRepo/IP Database/sample.bin.db24/IP-COUNTRY-REGION-CITY-LATITUDE-LONGITUDE-ZIPCODE-TIMEZONE-ISP-DOMAIN-NETSPEED-AREACODE-WEATHER-MOBILE-ELEVATION-USAGETYPE-SAMPLE.BIN"
    response=input("Do you want to fetch IP Location: 1.Yes (Y) 2.No (n)")
    if response.lower().startswith('y'):
        ipTracker.IPLocationFinderUsingIPAPImodule(csvDir,jsonDir,ipListCSV)
        stepIncrement()


    #Step-13: Generating HTML from all JSON files we have generated
    funcCallDict[scriptName].append(genHTJS.__name__)#46
    funcCallDict[genHTJS.__name__]=[genHTJS.getAllJSONFiles.__name__]#47
    funcCallDict[genHTJS.__name__].append(genHTJS.generateHTMLFromJSON.__name__)#48

    print("\nStep {}->Generating HTML from all JSON files we have generated".format(step))
    jsonFilesDict=genHTJS.getAllJSONFiles(jsonDir) #get all the jsonFileNames along with jsonFilesPath
    genHTJS.generateHTMLFromJSON(unalteredRepoDir,jsonFilesDict)

    #Step-Final: Reverting back to the source code directory
    os.chdir(unalteredRepoDir)

    return unalteredRepoDir,funcCallDict,netxFuncCallDict,netDrawFuncCallDict


def funcCallTracer(sourceCodeDir,unalteredRepoDict,fCallLog,fCallNetDraw,fCallNetXSimu):
    print("Into the {}\n--------------------\n".format(funcCallTracer.__name__))

    #1. Creating funcCall Directory
    funcCallDir= unalteredRepoDict+"/"+"FuncCall"
    tool.createDirectory(funcCallDir)
    os.chdir(funcCallDir)

    #2. Dumping the funcCallLog dictionary type into 3 json files
    tool.dumpDictIntoJSON(fCallLog,"funcCallLog_initial.json")
    tool.dumpDictIntoJSON(fCallNetXSimu,"funcCallNetxSimu.json")
    tool.dumpDictIntoJSON(fCallNetDraw,"funcCallNetDraw.json")

    #3. Merging all the funcCallLog dict into fCallLog dict
    fCallLog=tool.dictMergerHavingLists(fCallNetXSimu,fCallLog) #source, destination
    fCallLog=tool.dictMergerHavingLists(fCallNetDraw,fCallLog)
    tool.dumpDictIntoJSON(fCallLog,"funcCallLog_final.json")

    #4. Visualizing the funcCall Graph with input:fCallLog adjacency table/dict and generating fCallReport.txt
    funcCallReportStr=ng.networkGraphVisualization(funcCallDir,fCallLog)
    funcCallReport="funcCallReport.txt"
    tool.writeReportToFile("funcCallReport.txt",funcCallReportStr)

    #5. Convert the fCallLog adjacency table into funcCallLog.csv which will be later used for netx analysis
    funcCallAdjListCSV="funcCallLog_final.csv"
    adjCSVCoverter.adjListToCSVConverter(fCallLog,funcCallDir,funcCallAdjListCSV)

    #6. Generating the ipList i.e. functionList
    funcList=[]
    for k,valueList in fCallLog.items():
        if k not in funcList:
            funcList.append(k)
        if isinstance(valueList,list):
            for v in valueList:
                if v not in funcList:
                    funcList.append(v)
        else:
            if v not in funcList:
                funcList.append(v)
    #pprint.pprint(funcList)

    #7. Writing the funcList into csv
    funcListCSV="funcList.csv"
    tool.writingIntoCSV_funcCall(funcList,funcListCSV)
    #pprint.pprint(fCallLog)

    #8 networkxSimulation for mode=Directed and UnDirected Graph
    graphTypes=["DiG","UD"]
    for gt in graphTypes:
        print("Executing Mode: {}".format(gt))
        #Step-10: Generating Graph all attributes 02 json files using netx
        funcReportX,netxFuncCallDict=netx.networkxSimulation(funcCallDir,funcCallDir,funcCallDir,funcListCSV,funcCallAdjListCSV,gt,executionMode="fCall") #Graph type, set the user graph type here DiG vs UD
        tool.saveToDirectory(funcCallDir,funcCallReport,funcReportX,mode="a")


    #9. Calling the netDraw for showing root centrality of the funcCallGraph
    unused_netDrawFuncCallDict=netDraw.netDrawSetUpAndExecution(funcCallDir,funcCallDir,sourceCodeDir,funcListCSV,funcCallAdjListCSV,executionMode="fCall")

    #10: Generating HTML from all JSON files we have generated
    jsonFilesDict=genHTJS.getAllJSONFiles(funcCallDir) #get all the jsonFileNames along with jsonFilesPath
    genHTJS.generateHTMLFromJSON(funcCallDir,jsonFilesDict)


def main():
    sourceCodeDir="/home/jahid/Desktop/AllMyWorks/InformationSecurity/google/google-python-exercises/logpuzzle/logSolverMyCodeRepo/source"

    unalteredRepoDict,fCallLog,fCallNetDraw,fCallNetXSimu=mainLogMachine()

    funcCallTracer(sourceCodeDir,unalteredRepoDict,fCallLog,fCallNetDraw,fCallNetXSimu)

    os.chdir(sourceCodeDir)



if __name__ == '__main__':
  main()
