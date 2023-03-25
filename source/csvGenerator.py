import re
import os
import logPuzzleSupportTools as tool

def isValid(ip):
    ipParts=ip.split(".")
    status=all(int(part)>=0 and int(part)<=255 for part in ipParts)
    return status

def getMatchedIP(ipRe,sourceLine):
    matchedIp=re.findall(ipRe,sourceLine)
    #uniqueIps=list(set(matchedIp))
    validIpList=[]
    for ip in matchedIp:
        if isValid(ip):
            validIpList.append(ip)
    return validIpList

def getMatchedDate(dateRe,sourceLine):
    matchedDate=re.search(dateRe,sourceLine)
    if matchedDate:
        return matchedDate.group(0)

def getMatchedTime(timeRe,sourceLine):
    matchedTime=re.search(timeRe,sourceLine)
    if matchedTime:
        return matchedTime.group(0)

def getMatchedBrowser(browserRe,sourceLine):
    matchedBrowser=re.findall(browserRe,sourceLine)
    versionBrowser=[]
    if matchedBrowser:
        for browser in matchedBrowser:
            browserVersion="{}V{}".format(browser[0],browser[1])
            versionBrowser.append(browserVersion)
    else:
        versionBrowser.append("None")
    #return ",".join(versionBrowser)
    return versionBrowser

def getMatchedOS(osRe,sourceLine):
    matchedOS=re.findall(osRe,sourceLine)
    sortedMatchedOS=list(set(matchedOS))
    if sortedMatchedOS:
        #return ",".join(sortedMatchedOS)
        return sortedMatchedOS
    else:
        return ["None"]

def getMatchedEmails(emailRe,sourceLine):
    matchedEmail=re.findall(emailRe,sourceLine)
    sortedMatchedEmail=list(set(matchedEmail))
    if sortedMatchedEmail:
        #return ",".join(sortedMatchedEmail)
        return sortedMatchedEmail
    else:
        return ["None"]

def getMatchedGETURL(getRe,sourceLine):
    matchedGETURL=re.search(getRe,sourceLine)
    if matchedGETURL:
        return [matchedGETURL.group(0)]
    else:
        return ["None"]

def getMatchedSearchEngineen(sengRe,sourceLine):
    matchedSearcheEng=re.findall(sengRe,sourceLine)
    if matchedSearcheEng:
        return [x.lower() for x in matchedSearcheEng]
    else:
        return ["None"]

def infoDictGenerator(sourceLogFile):
    #ipRe=r'^([1][0-9][0-9].|^[2][5][0-5].|^[2][0-4][0-9].|^[1][0-9][0-9].|^[0-9][0-9].|^[0-9].)([1][0-9][0-9].|[2][5][0-5].|[2][0-4][0-9].|[1][0-9][0-9].|[0-9][0-9].|[0-9].)([1][0-9][0-9].|[2][5][0-5].|[2][0-4][0-9].|[1][0-9][0-9].|[0-9][0-9].|[0-9].)([1][0-9][0-9]|[2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[0-9][0-9]|[0-9])'

    ipRe=r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    emailRe=r'[\w\.-]+@[\w\.-]+'
    getRe=r'\"GET \/.* HTTP\/\d+\.\d+\"'
    browserRe=r'(?i)(firefox|msie|chrome|safari|mozilla)[/\s]([\d.]+)'
    osRe=r'(?i)(linux|windows|mac)'
    sengRe=r'(?i)(google|ask)'
    timeRe=r'00\:\d{2}\:\d{2}'
    dateRe=r'[0-2]?[0-9]?\/[A-Za-z]{3}\/2[0-9]{3}'

    #----- create an infoDict dictionary---------
    infoDict={}


    with open(sourceLogFile,'r') as fp:
        fContentList=fp.readlines()

    for line in fContentList:
        ips=getMatchedIP(ipRe,line)
        date=getMatchedDate(dateRe,line)
        time=getMatchedTime(timeRe,line)
        browser=getMatchedBrowser(browserRe,line)
        os=getMatchedOS(osRe,line)
        email=getMatchedEmails(emailRe,line)
        getURL=getMatchedGETURL(getRe,line)
        seng=getMatchedSearchEngineen(sengRe,line)
        #print(ips, len(ips))
        if not len(ips)==0:
            for ip in ips:
                if ip not in infoDict:
                    infoDict[ip]=[date,[time],browser,os,email,getURL,seng]
                else:
                    if date not in infoDict[ip]:infoDict[ip].append(date)
                    if time not in infoDict[ip][1]:infoDict[ip][1].append(time)
                    #browser is a string here
                    infoDict[ip][4].extend(email)
                    infoDict[ip][5].extend(getURL)
                    infoDict[ip][6].extend(seng)

                infoDict[ip][4]=list(set(infoDict[ip][4]))
                infoDict[ip][6]=list(set(infoDict[ip][6]))

                #if len(infoDict[ip])>1:
                    #infoDict[ip]=list(set(infoDict[ip]))
    #print infoDict
    return infoDict


def csvGenerator(sourceLogFile,toDir,fileName): #fileName=csvFile="animalCSVGeneral.csv"
    ##toDir=../animalLogSimulation/CSV_Files
    infoDict=infoDictGenerator(sourceLogFile)
    tool.createDirectory(toDir)

    csv=open(os.path.join(toDir,fileName),"w") #../animalLogSimulation/CSV_Files/animalCSVGeneral
    #csv=open(fileName,"w")
    columnTileRow="IP, Date(M), Time(From), Time(To), TotalTimeHits, Browser, OS, EMAILS, GETCommandExecuted, SearchEngineen\n"
    csv.write(columnTileRow)
    for ip in infoDict.keys():
        row="{},{},{},{},{},{},{},{},{},{}\n".\
        format(ip,infoDict[ip][0],min(infoDict[ip][1]),max(infoDict[ip][1]),len(infoDict[ip][1]),
        "\""+",".join(infoDict[ip][2])+"\"","\""+",".join(infoDict[ip][3])+"\"",
        "\""+",".join(infoDict[ip][4])+"\"",len(infoDict[ip][5]),"\""+"_".join(infoDict[ip][6])+"\"")
        csv.write(row)
    csv.close()
    #return csv

def main():
    toDir="/home/jahid/Desktop/AllMyWorks/InformationSecurity/google/google-python-exercises/logpuzzle/logSolverMyCodeRepo/CSV File"
    sourceLogFile="animal_code.google.com"
    fileName="animalloginfo.csv"
    csv=csvGenerator(sourceLogFile,toDir,fileName)

if __name__ == '__main__':
    main()
