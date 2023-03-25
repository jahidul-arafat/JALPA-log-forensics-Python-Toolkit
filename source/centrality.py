import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter
import os
from pylab import rcParams
import logPuzzleSupportTools as tool
#from netDraw import draw

def degreeCentrality(G,pos,DiG,dpos,toDir):
    graphDir=toDir+"/"+"Graphs"
    tool.createDirectory(graphDir)
    os.chdir(graphDir)

    rcParams['figure.figsize'] = 20, 10 #width=5 inches, height=10 inches
    plt.figure(1)

    #Undirected
    plt.subplot(221)
    unDir_DegCent=nx.degree_centrality(G)
    emptyDict={}
    updatedAllDict=tool.allInOneDict(unDir_DegCent,toDict=emptyDict,)
    sorted_unDir_DegCent=sorted(unDir_DegCent.items(),key=itemgetter(1),reverse=True)
    print("UnDirected Graph (Degree Centrality):\n{}\n\n".format(tool.printCentralityValues(sorted_unDir_DegCent)))
    tool.draw(G, pos,unDir_DegCent, 'Degree Centrality (UnDireccted Hub)')


    #Directed- Degree Centrality
    #plt.figure(2)
    plt.subplot(222)
    dir_DegCent=nx.degree_centrality(DiG)
    updatedAllDict=tool.allInOneDict(dir_DegCent,toDict=updatedAllDict)
    sorted_dir_DegCent=sorted(dir_DegCent.items(),key=itemgetter(1),reverse=True)
    print("Directed Graph (Degree Centrality):\n{}\n\n".format(tool.printCentralityValues(sorted_dir_DegCent)))
    tool.draw(DiG, dpos,dir_DegCent, 'Degree Centrality (Directed Hub)')

    #Directed- in_degree Centrality
    #plt.figure(3)
    plt.subplot(223)
    in_dir_DegCent=nx.in_degree_centrality(DiG)
    updatedAllDict=tool.allInOneDict(in_dir_DegCent,toDict=updatedAllDict)
    sorted_in_dir_DegCent=sorted(in_dir_DegCent.items(),key=itemgetter(1),reverse=True)
    print("Directed Graph (In Degree Centrality):\n{}\n\n".format(tool.printCentralityValues(sorted_in_dir_DegCent)))
    tool.draw(DiG,dpos,in_dir_DegCent, "In Degree Centrality (Directed Graph)")

    #Directed- out_degree Centrality
    #plt.figure(4)
    plt.subplot(224)
    out_dir_DegCent=nx.out_degree_centrality(DiG)
    updatedAllDict=tool.allInOneDict(out_dir_DegCent,toDict=updatedAllDict)
    sorted_out_dir_DegCent=sorted(out_dir_DegCent.items(),key=itemgetter(1),reverse=True)
    print("Directed Graph (Out Degree Centrality):\n{}\n\n".format(tool.printCentralityValues(sorted_out_dir_DegCent)))
    tool.draw(DiG,dpos,out_dir_DegCent, "Out Degree Centrality (Directed Graph)")

    plt.savefig("degreeCentrality(root_graph).png")
    plt.show()
    os.chdir(toDir)
    return updatedAllDict



def betweennessCentrality(G,pos,DiG,dpos,toDir,updatedAllDict):
    #you must update graphPreparation.addingAttributesToNodes(G,nodeList,jsonDir,fileName) function
    #while addifing new attributes i.e. centralities in graph
    #also change the tool.writingIntoCSV(sortedCentralityDict,fileName) function
    graphDir=toDir+"/"+"Graphs"
    tool.createDirectory(graphDir)
    os.chdir(graphDir)

    rcParams['figure.figsize'] = 20, 10 #width=5 inches, height=10 inches
    plt.figure(1)

    plt.subplot(121)
    unDir_betCent=nx.betweenness_centrality(G)
    updatedAllDict=tool.allInOneDict(unDir_betCent,toDict=updatedAllDict)
    sorted_unDir_betCent=sorted(unDir_betCent.items(),key=itemgetter(1),reverse=True)
    print("Undirected Graph (Betweenness Centrality):\n{}\n\n".format(tool.printCentralityValues(sorted_unDir_betCent)))
    tool.draw(G,pos,unDir_betCent,"Betweenness Centrality (Undirected Graph)")

    plt.subplot(122)
    dir_betCent=nx.betweenness_centrality(DiG)
    updatedAllDict=tool.allInOneDict(dir_betCent,toDict=updatedAllDict)
    sorted_dir_betCent=sorted(dir_betCent.items(),key=itemgetter(1),reverse=True)
    print("Directed Graph (Betweenness Centrality):\n{}\n\n".format(tool.printCentralityValues(sorted_dir_betCent)))
    tool.draw(DiG,dpos,dir_betCent,"Betweenness Centrality (Directed Graph)")

    plt.savefig("betweennessCentrality(root_graph).png")
    plt.show()
    os.chdir(toDir) #revert back to json dir
    return updatedAllDict

def eigenvectorCentrality(G,pos,DiG,dpos,toDir,updatedAllDict):
    #you must update graphPreparation.addingAttributesToNodes(G,nodeList,jsonDir,fileName) function
    #while addifing new attributes i.e. centralities in graph
    #also change the tool.writingIntoCSV(sortedCentralityDict,fileName) function
    graphDir=toDir+"/"+"Graphs"
    tool.createDirectory(graphDir)
    os.chdir(graphDir)

    rcParams['figure.figsize'] = 20, 10 #width=5 inches, height=10 inches
    plt.figure(1)

    plt.subplot(121)
    unDir_eigenCent=nx.eigenvector_centrality(G)
    updatedAllDict=tool.allInOneDict(unDir_eigenCent,toDict=updatedAllDict)
    sorted_unDir_eigenCent=sorted(unDir_eigenCent.items(),key=itemgetter(1),reverse=True)
    print("Undirected Graph (Eigenvector Centrality):\n{}\n\n".format(tool.printCentralityValues(sorted_unDir_eigenCent)))
    tool.draw(G,pos,unDir_eigenCent,"Eigenvector Centrality (Undirected Graph)")

    plt.subplot(122) #for directed graph use nx.eigenvector_centrality_numpy(DiG)
    dir_eigenCent=nx.eigenvector_centrality_numpy(DiG)
    updatedAllDict=tool.allInOneDict(dir_eigenCent,toDict=updatedAllDict)
    sorted_dir_eigenCent=sorted(dir_eigenCent.items(),key=itemgetter(1),reverse=True)
    print("Directed Graph (Eigenvector Centrality):\n{}\n\n".format(tool.printCentralityValues(sorted_dir_eigenCent)))
    tool.draw(DiG,dpos,dir_eigenCent,"Eigenvector Centrality (Directed Graph)")

    plt.savefig("eigenVectorCentrality(root_graph).png")
    plt.show()
    os.chdir(toDir) #revert back to json dir
    return updatedAllDict


def closenessCentrality(G,pos,DiG,dpos,toDir,updatedAllDict):
    #you must update graphPreparation.addingAttributesToNodes(G,nodeList,jsonDir,fileName) function
    #while adding new attributes i.e. centralities in graph
    #also change the tool.writingIntoCSV(sortedCentralityDict,fileName) function
    graphDir=toDir+"/"+"Graphs"
    tool.createDirectory(graphDir)
    os.chdir(graphDir)

    rcParams['figure.figsize'] = 20, 10 #width=5 inches, height=10 inches
    plt.figure(1)

    plt.subplot(121)
    unDir_closeCent=nx.closeness_centrality(G)
    updatedAllDict=tool.allInOneDict(unDir_closeCent,toDict=updatedAllDict)
    sorted_unDir_closeCent=sorted(unDir_closeCent.items(),key=itemgetter(1),reverse=True)
    print("Undirected Graph (Closeness Centrality):\n{}\n\n".\
    format(tool.printCentralityValues(sorted_unDir_closeCent)))
    tool.draw(G,pos,unDir_closeCent,"Closeness Centrality (Undirected Graph)")

    plt.subplot(122)
    dir_closeCent=nx.closeness_centrality(DiG)
    updatedAllDict=tool.allInOneDict(dir_closeCent,toDict=updatedAllDict)
    sorted_dir_closeCent=sorted(dir_closeCent.items(),key=itemgetter(1),reverse=True)
    print("Directed Graph (Closeness Centrality):\n{}\n\n".\
    format(tool.printCentralityValues(sorted_dir_closeCent)))
    tool.draw(DiG,dpos,dir_closeCent,"Closeness Centrality (Directed Graph)")

    plt.savefig("closenessCentrality(root_graph).png")
    plt.show()
    os.chdir(toDir) #revert back to json dir
    return updatedAllDict

def katzCentrality(G,pos,DiG,dpos,toDir,updatedAllDict):
    #you must update graphPreparation.addingAttributesToNodes(G,nodeList,jsonDir,fileName) function
    #while addifing new attributes i.e. centralities in graph
    #also change the tool.writingIntoCSV(sortedCentralityDict,fileName) function
    graphDir=toDir+"/"+"Graphs"
    tool.createDirectory(graphDir)
    os.chdir(graphDir)

    rcParams['figure.figsize'] = 20, 10 #width=5 inches, height=10 inches
    plt.figure(1)

    plt.subplot(121)
    unDir_katzCent=nx.katz_centrality(G,alpha=0.01,beta=1.0) #remember: powerIteration error could happen here, for animalLog set alpha=0.10, for place Log alpha=0.10 to avoid the error
    updatedAllDict=tool.allInOneDict(unDir_katzCent,toDict=updatedAllDict)
    sorted_unDir_katzCent=sorted(unDir_katzCent.items(),key=itemgetter(1),reverse=True)
    print("Undirected Graph (Katz Centrality):\n{}\n\n".format(tool.printCentralityValues(sorted_unDir_katzCent)))
    tool.draw(G,pos,unDir_katzCent,"Katz Centrality (Undirected Graph)")

    plt.subplot(122) #for directed graph use nx.katz_centrality_numpy(DiG)
    dir_katzCent=nx.katz_centrality_numpy(DiG,alpha=0.01, beta=1.0)#remember: powerIteration error could happen here, for animalLog set alpha=0.10, for place Log alpha=0.10 to avoid the error
    updatedAllDict=tool.allInOneDict(dir_katzCent,toDict=updatedAllDict)
    sorted_dir_katzCent=sorted(dir_katzCent.items(),key=itemgetter(1),reverse=True)
    print("Directed Graph (Katz Centrality):\n{}\n\n".format(tool.printCentralityValues(sorted_dir_katzCent)))
    tool.draw(DiG,dpos,dir_katzCent,"Katz Centrality (Directed Graph)")

    plt.savefig("katzCentrality(root_graph).png")
    plt.show()
    os.chdir(toDir) #revert back to json dir
    return updatedAllDict


def pagerankCentrality(G,pos,DiG,dpos,toDir,updatedAllDict):
    #make a update in netDraw, add the emelemts into dict there
    #you must update graphPreparation.addingAttributesToNodes(G,nodeList,jsonDir,fileName) function
    #while addifing new attributes i.e. centralities in graph
    #also change the tool.writingIntoCSV(sortedCentralityDict,fileName) function
    graphDir=toDir+"/"+"Graphs"
    tool.createDirectory(graphDir)
    os.chdir(graphDir)

    rcParams['figure.figsize'] = 20, 10 #width=5 inches, height=10 inches
    plt.figure(1)

    plt.subplot(121)
    unDir_pagerankCent=nx.pagerank(G,alpha=0.85) #default beta=1.0, alpha=edge weigh
    updatedAllDict=tool.allInOneDict(unDir_pagerankCent,toDict=updatedAllDict)
    sorted_unDir_pagerankCent=sorted(unDir_pagerankCent.items(),key=itemgetter(1),reverse=True)
    print("Undirected Graph (Pagerank Centrality):\n{}\n\n".format(tool.printCentralityValues(sorted_unDir_pagerankCent)))
    tool.draw(G,pos,unDir_pagerankCent,"Page rank Centrality (Undirected Graph)")

    plt.subplot(122) #for directed graph use nx.pagerank_centrality_numpy(DiG)
    dir_pagerankCent=nx.pagerank_numpy(DiG,alpha=0.85) #alpha=edge weight
    updatedAllDict=tool.allInOneDict(dir_pagerankCent,toDict=updatedAllDict)
    sorted_dir_pagerankCent=sorted(dir_pagerankCent.items(),key=itemgetter(1),reverse=True)
    print("Directed Graph (Page rank Centrality):\n{}\n\n".format(tool.printCentralityValues(sorted_dir_pagerankCent)))
    tool.draw(DiG,dpos,dir_pagerankCent,"Page rank Centrality (Directed Graph)")

    plt.savefig("pagerankCentrality(root_graph).png")
    plt.show()
    os.chdir(toDir) #revert back to json dir
    return updatedAllDict

def hitsHubsAndAuthorities(DiG,dpos,toDir,updatedAllDict):
    #make a update in netDraw, add the emelemts into dict there
    #you must update graphPreparation.addingAttributesToNodes(G,nodeList,jsonDir,fileName) function
    #while addifing new attributes i.e. centralities in graph
    #also change the tool.writingIntoCSV(sortedCentralityDict,fileName) function
    graphDir=toDir+"/"+"Graphs"
    tool.createDirectory(graphDir)
    os.chdir(graphDir)

    rcParams['figure.figsize'] = 20, 10 #width=5 inches, height=10 inches
    plt.figure(1)

    hubDict,authorityDict=nx.hits(DiG)
    plt.subplot(121)
    updatedAllDict=tool.allInOneDict(hubDict,toDict=updatedAllDict)
    sorted_hubDict=sorted(hubDict.items(),key=itemgetter(1),reverse=True)
    print("Directed Graph (HITS HUBS):\n{}\n\n".format(tool.printCentralityValues(sorted_hubDict)))
    tool.draw(DiG,dpos,hubDict,"HUBS-Connected with most high Authority nodes (Directed Graph)")

    plt.subplot(122)
    updatedAllDict=tool.allInOneDict(authorityDict,toDict=updatedAllDict)
    sorted_authorityDict=sorted(authorityDict.items(),key=itemgetter(1),reverse=True)
    print("Directed Graph (HITS AUTHORITIES):\n{}\n\n".format(tool.printCentralityValues(sorted_authorityDict)))
    tool.draw(DiG,dpos,authorityDict,"Authorities(Nodes most cited by Hubs) (Directed Graph)")

    plt.savefig("hitsHubsAuthorities(root_graph).png")
    plt.show()
    os.chdir(toDir) #revert back to json dir
    return updatedAllDict

def main():
    pass

if __name__ == '__main__':
    main()
