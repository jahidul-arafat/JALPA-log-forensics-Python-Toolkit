import logPuzzleSupportTools as tool
import os
from more_itertools import unique_everseen

def removeAFile(toDir,fileName):
    os.remove(os.path.join(toDir, fileName))

def removeDuplicatedCSVContents(toDir, inpFile, outFile):
    with open(os.path.join(toDir, inpFile), 'r') as inp_file, \
    open(os.path.join(toDir, outFile), 'w') as out_file:
        out_file.writelines(unique_everseen(inp_file))


def adjListToCSVConverter(adjList, toDir, fileName): #../animalLogSimulation/CSV_Files #adjListAnimalCSV_temp.csv
    tool.createDirectory(toDir)
    csv=open(os.path.join(toDir, fileName), "w")
    columnTitleRow="IP, AdjacentTo\n"
    csv.write(columnTitleRow)
    for ip in adjList.keys():
        for adjIP in adjList[ip]:
            row="{},{}\n".format(ip, adjIP)
            csv.write(row)
    csv.close()
    #return csv


def main():
    toDir="/home/jahid/Desktop/AllMyWorks/InformationSecurity/google/google-python-exercises/logpuzzle/logSolverMyCodeRepo/CSV File"
    tempFileName="adjListToCSV_animal_temp.csv"
    finalFileName="adjListToCSV_animal_final.csv"
    adjList={'10.1.40.113': ['Opps', '10.254.254.138'],
        '10.254.254.37': ['1.8.1.6', '5.1.707.665', '2.0.0.6', '10.254.254.28'],
        '10.254.254.103': ['Opps', '10.254.254.28'], '10.254.254.38': ['Opps', '10.254.254.138'],
        '10.254.254.42': ['1.8.1.4', '2.0.0.4', '10.254.254.28'], '10.254.254.58': ['Opps', '10.254.254.28'],
        '10.254.254.74': ['1.8.0.12', '1.5.0.12', '10.254.254.28'], '10.254.254.28': ['Opps'],
        '10.254.254.29': ['Opps', '10.254.254.138', '1.8.1.6', '2.0.0.6', '10.1.40.113'], '10.254.254.66': ['Opps', '10.254.254.28'],
        '10.254.254.138': ['Opps', '10.1.40.113', '1.8.1.6', '2.0.0.6', '10.254.254.65'], '10.254.254.137': ['Opps', '10.254.254.28'],
        '10.254.254.94': ['1.8.1.6', '2.0.0.6', '10.254.254.138', '1.8.1.6', '2.0.0.6', '10.254.254.138'], '10.254.254.193': ['Opps', '10.254.254.58'],
        '10.254.254.57': ['Opps', '10.254.254.28', '1.8.1.6', '2.0.0.6', '10.254.254.58'],
        '10.254.254.65': ['Opps', '10.254.254.29', '1.8.1.6', '2.0.0.6', '10.254.254.28']}
    adjListToCSVConverter(adjList, toDir, tempFileName)
    removeDuplicatedCSVContents(toDir, tempFileName, finalFileName)
    removeAFile(toDir, tempFileName)

if __name__ == '__main__':
    main()
