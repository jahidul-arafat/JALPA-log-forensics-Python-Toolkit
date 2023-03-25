from __future__ import division
import os
import re
import sys
import urllib

def ipValidityChecking(ip):
    ipParts=ip.split(".")
    status=all(int(part)>=0 and int(part)<=255 for part in ipParts)
    return status

#------------------------ip fetching---------------------------
def fetchIpFromLog(sourceLogFile):
    matchedIp=[]
    with open(sourceLogFile,'r') as fp:
        fContent=fp.readlines()
    ipRe=r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    #ipRe=r'([1][0-9][0-9].|^[2][5][0-5].|^[2][0-4][0-9].|^[1][0-9][0-9].|^[0-9][0-9].|^[0-9].)([1][0-9][0-9].|[2][5][0-5].|[2][0-4][0-9].|[1][0-9][0-9].|[0-9][0-9].|[0-9].)([1][0-9][0-9].|[2][5][0-5].|[2][0-4][0-9].|[1][0-9][0-9].|[0-9][0-9].|[0-9].)([1][0-9][0-9]|[2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[0-9][0-9]|[0-9])'
    for line in fContent:
        fetchedIP=re.findall(ipRe,line)
        matchedIp.extend(fetchedIP)
    filteredIp=[]
    for ip in matchedIp:
        if ipValidityChecking(ip):
            filteredIp.append(ip)
    uniqueIps=list(set(filteredIp))
    ipStr="\n".join(filteredIp)
    uniqueIpStr="\n".join(uniqueIps)
    #print ipStr
    #print uniqueIps
    return ipStr+"\n\nUnique IPS:{}\n--------------\n".format(len(uniqueIps))+uniqueIpStr

def generateIpAdjacencyTable(sourceLogFile):
    ipRe=r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    #ipRe=r'^([1][0-9][0-9].|^[2][5][0-5].|^[2][0-4][0-9].|^[1][0-9][0-9].|^[0-9][0-9].|^[0-9].)([1][0-9][0-9].|[2][5][0-5].|[2][0-4][0-9].|[1][0-9][0-9].|[0-9][0-9].|[0-9].)([1][0-9][0-9].|[2][5][0-5].|[2][0-4][0-9].|[1][0-9][0-9].|[0-9][0-9].|[0-9].)([1][0-9][0-9]|[2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[0-9][0-9]|[0-9])'

    ipVisitedList=[]
    prevIp=0
    adjDict={}
    with open(sourceLogFile,'r') as fp:
        fContentList=fp.readlines()

    for line in fContentList:
        matchedIps=re.findall(ipRe,line)
        #print("Visiting:{}-->{}\n".format(matchedIps[0],matchedIps))
        ipVisitedList.append(matchedIps[0])

        if len(matchedIps)>1: #probably this will not execute, bcoz each line has only one valid ip
            if matchedIps[0] not in adjDict:
                adjDict[matchedIps[0]]=matchedIps[1:]
            else:
                adjDict[matchedIps[0]].extend(matchedIps[1:])
        else:
            if matchedIps[0] not in adjDict:
                adjDict[matchedIps[0]]=[]
            else:
                adjDict[matchedIps[0]].extend([])


        if prevIp>=1:
            adjDict[ipVisitedList[prevIp-1]].append(matchedIps[0])
        prevIp+=1

    #print (ipVisitedList)
    adjDictSorted={}
    for key in adjDict.keys():
        adjDictSorted[key]=list(set(adjDict[key]))
    return adjDictSorted

