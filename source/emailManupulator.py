from __future__ import division
import os
import re
import sys
import urllib

def getEmailListStrVersion(sourceFile):
    allEmails,setEmails=getTheEmails(sourceFile)
    emStr="\n".join(allEmails)
    return emStr

def getTheEmails(sourceFile):
    emailPattern=r'[\w\.-]+@[\w\.-]+'
    f=open(sourceFile,'r')
    allLines=f.read()
    f.close()
    allMatchedEmails=re.findall(emailPattern,allLines)
    return allMatchedEmails,list(set(allMatchedEmails))

def emailsWeightImportance(allEmailLists,setEmailList):
    emailsWeight={}
    for email in setEmailList:
        emailsWeight[email]=[allEmailLists.count(email),round(allEmailLists.count(email)/len(allEmailLists),2)]
    return emailsWeight

def domainSplitting(setEmails):
    domainList=[]
    for email in setEmails:
        splitAddress = email.split('@')
        domain = str(splitAddress[1])
        #print (domain)
        domainList.append(domain)
    domainList=list(set(domainList))
    domainStr="\n".join(domainList)
    return domainStr,domainList
