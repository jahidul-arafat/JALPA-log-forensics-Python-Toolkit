#https://www.ip2location.com/developers/python
import logPuzzleSupportTools as tool
import IP2Location
import os
import json
from geoip import geolite2
import ipapi
from json2html import *
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

def saveasJSONCSV(funcName,ipLocInfoDict,csvDir,jsonDir):
    #change to json dir
    os.chdir(jsonDir)
    jsonFileName="ipLocInfoUsing_{}.json".format(funcName)
    with open(jsonFileName,'w') as out_file:
        json.dump(ipLocInfoDict,out_file,sort_keys = True, indent = 4, ensure_ascii = False)

    #change to csv dir
    csvFileName="ipLocInfoUsing_{}.csv".format(funcName)
    tool.loadJsonToCSV(jsonDir,csvDir,jsonFileName,csvFileName)

    #load into html
    #http://json2html.varunmalhotra.xyz/
    os.chdir(jsonDir)
    htmlStr=json2html.convert(json=ipLocInfoDict)
    tool.writeReportToFile("ipLocInfo.html",htmlStr)

def IPLocationFinderUsingIPAPImodule(csvDir,jsonDir,ipListCSV):
    #https://github.com/ipapi-co/ipapi-python
    ipLocInfoDict={}
    ip_names=tool.getTheIPs(csvDir,ipListCSV)
    for ip in ip_names:
        fetchedInfo=ipapi.location(ip)
        if ip not in ipLocInfoDict:
            ipLocInfoDict[ip]=fetchedInfo
        else:
            ipLocInfoDict[ip].update(fetchedInfo)

    saveasJSONCSV(IPLocationFinderUsingIPAPImodule.__name__,ipLocInfoDict,csvDir,jsonDir)


def IPLocationFinderUsingGeoIpModule(csvDir,jsonDir,ipListCSV):
    #https://pythonhosted.org/python-geoip/
    ipLocInfoDict={}
    ip_names=tool.getTheIPs(csvDir,ipListCSV)
    for ip in ip_names:
        match=geolite2.lookup(ip)
        ipLocInfoDict[ip]={}
        if match is not None:
            ipLocInfoDict[ip].update({"country":match.country})
            ipLocInfoDict[ip].update({"continent":match.continent})
            ipLocInfoDict[ip].update({"timezone":match.timezone})
            ipLocInfoDict[ip].update({"subdivisions":",".join([n for n in (match.subdivisions)])}) #subdivisions returns a frozenset

    saveasJSONCSV(IPLocationFinderUsingGeoIpModule.__name__,ipLocInfoDict,csvDir,jsonDir) #__name__ will gibve you the function name


def IPLocationFinderUsingIP2LocationModule(csvDir,jsonDir,ipListCSV,ipDB):
    #https://www.ip2location.com/developers/python
    ipLocInfoDict={}
    ip_names=tool.getTheIPs(csvDir,ipListCSV)
    #print(ip_names)
    IP2LocObj=IP2Location.IP2Location()
    IP2LocObj.open(ipDB)
    for ip in ip_names:
        ipLocInfoDict[ip]=(IP2LocObj.get_all(ip)).__dict__ #get_all returns an instance, __dict__ convert instance to dictionary

    saveasJSONCSV(IPLocationFinderUsingIP2LocationModule.__name__,ipLocInfoDict,csvDir,jsonDir)


def main():
    csvDir="/home/jahid/Desktop/AllMyWorks/InformationSecurity/google/google-python-exercises/logpuzzle/logSolverMyCodeRepo/simulationResults/outputGenerated/animalLogSimulation/CSV_Files"
    jsonDir="/home/jahid/Desktop/AllMyWorks/InformationSecurity/google/google-python-exercises/logpuzzle/logSolverMyCodeRepo/simulationResults/outputGenerated/animalLogSimulation/JSON_Files"
    ipListCSV="animalCSVGeneral.csv"

    ipDB1="/home/jahid/Desktop/AllMyWorks/InformationSecurity/google/google-python-exercises/logpuzzle/logSolverMyCodeRepo/IP Database/sample.bin.db24/IP-COUNTRY-REGION-CITY-LATITUDE-LONGITUDE-ZIPCODE-TIMEZONE-ISP-DOMAIN-NETSPEED-AREACODE-WEATHER-MOBILE-ELEVATION-USAGETYPE-SAMPLE.BIN"
    #IPLocationFinder(csvDir,jsonDir,ipListCSV,ipDB1)
    #IPLocationFinderUsingGeoIpModule(csvDir,jsonDir,ipListCSV)

    #PyCallGraph
    #tool.pyCallGraph(jsonDir,IPLocationFinderUsingIPAPImodule.__name__,IPLocationFinderUsingIPAPImodule(csvDir,jsonDir,ipListCSV))
    graphviz=GraphvizOutput()
    graphviz.output_file="{}.png".format(IPLocationFinderUsingIPAPImodule.__name__)
    with PyCallGraph(output=graphviz):
        IPLocationFinderUsingIPAPImodule(csvDir,jsonDir,ipListCSV)

    #change the working directory back at the end
    os.chdir("/home/jahid/Desktop/AllMyWorks/InformationSecurity/google/google-python-exercises/logpuzzle/logSolverMyCodeRepo/source/")



if __name__ == '__main__':
    main()
