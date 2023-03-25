from pattern.graph import Graph,  adjacency
#from django.http import HttpResponse
#from pattern.graph import bfs, dfs
#import cherrypy
import random
import operator

def networkGraphVisualization(toDir,adjacencyList):
        networkReport=""
        adjReport=""
        ipWeightReport=""
        isolatedNodeReport=""
        centralityReport=""
        g=Graph(distance=18)
        #add vertices and edges for words in the same bucket
        for ip1 in adjacencyList.keys():
                for ip2 in adjacencyList[ip1]:
                            g.add_edge(ip1, ip2, stroke=(0,0,0,0.75))

        ipWeightReport+="Weight/IP Pairs\n"
        for node in sorted(g.nodes,  key=lambda node:node.weight):
            ipWeightReport+="{}:{}\n".format(node, node.weight)

        adjReport+="Adjacency Graph:\n{}\n".format(adjacency(g))


        #graph.prune(depth=0)           # Removes nodes + edges if len(node.links) <= depth.
        isolatedNodeReport+="Removing Any Isolated Node: {}".format(g.prune(0))


        #graph.betweenness_centrality() # Updates all Node.centrality values.
        #A node with higher betweeness centrality would have more control over the network bcoz more information will pass through that node
        #Algo- Floyed-Warshell
        centralityReport="Calculating the betweenness Centrality:\n{}\n\n".format(dictSorter(g.betweenness_centrality()))


        #graph.eigenvector_centrality() # Updates all Node.weight values.
        centralityReport+="Calculating the eigen vector centrality:\n{}\n".format(dictSorter(g.eigenvector_centrality()))


        #graph.density                  # < 0.35 => sparse, > 0.65 => dense
        #print ("The graph is densed:"+str(g.density))



        toDir=toDir+"/"+'networkGraphLogForensics' #../animalLogSimulation/networkGraphLogForensics

        for n in g.sorted(): # Sort by Node.weight.
            n.fill = (0, 0.5, 1, 0.75 * n.weight)

        g.export(toDir, directed=True, weighted=0.6) ##../animalLogSimulation/networkGraphLogForensics
        #print (g.nodes)


        print("Generating IP Tree............")

        #------------------------------------More informations--------------
        generalReport="General Information\n----------------------\n"
        generalReport+="Graph Nodes/Edges/isDense {}/{}/{}\n".format(len(g.nodes), len(g.edges), g.is_dense)
        generalReport+="Eigen Vector Centrality: Most Important Node/Least Important Node: {}/{}\n".\
        format(keywithmaxminval(g.eigenvector_centrality()), keywithmaxminval(g.eigenvector_centrality(), mode="min"))

        generalReport+="Betweeness Centrality: Most Important Node/Least Important Node: {}/{}\n".\
        format(keywithmaxminval(g.betweenness_centrality()), keywithmaxminval(g.betweenness_centrality(), mode="min"))

        networkReport=generalReport+"\n"+adjReport+"\n"+ipWeightReport+"\n"+\
        isolatedNodeReport+"\n"+centralityReport+"\n"+\
        "(************REPORT ENDS HERE**************)"

        return networkReport


def keywithmaxminval(d, mode="max"):
    """ a) create a list of the dict's keys and values;
    b) return the key with the max value"""
    v=list(d.values())
    k=list(d.keys())
    if mode=="max":
        return "{}:{}".format(k[v.index(max(v))], max(v))
    else:
        return "{}:{}".format(k[v.index(min(v))], min(v))

def dictSorter(myDict, mode="val"):
    if mode=="val":
        sortedMyDict=sorted(myDict.items(),key=operator.itemgetter(1))
    else:
        sortedMyDict=sorted(myDict.items(),key=operator.itemgetter(0))
    return sortedMyDict


def main():
    #toDir="/home/jahid/Desktop/AllMyWorks/InformationSecurity/google/google-python-exercises/logpuzzle/animalDir"
    toDir="/home/jahid/Desktop/AllMyWorks/InformationSecurity/google/google-python-exercises/logpuzzle/logSolverMyCodeRepo/simulationResults/outputGenerated/animalLogSimulation"
    adjacencyList={'10.1.40.113': ['Opps', '10.254.254.138'],
        '10.254.254.37': ['1.8.1.6', '5.1.707.665', '2.0.0.6', '10.254.254.28'],
        '10.254.254.103': ['Opps', '10.254.254.28'], '10.254.254.38': ['Opps', '10.254.254.138'],
        '10.254.254.42': ['1.8.1.4', '2.0.0.4', '10.254.254.28'], '10.254.254.58': ['Opps', '10.254.254.28'],
        '10.254.254.74': ['1.8.0.12', '1.5.0.12', '10.254.254.28'], '10.254.254.28': ['Opps'],
        '10.254.254.29': ['Opps', '10.254.254.138', '1.8.1.6', '2.0.0.6', '10.1.40.113'], '10.254.254.66': ['Opps', '10.254.254.28'],
        '10.254.254.138': ['Opps', '10.1.40.113', '1.8.1.6', '2.0.0.6', '10.254.254.65'], '10.254.254.137': ['Opps', '10.254.254.28'],
        '10.254.254.94': ['1.8.1.6', '2.0.0.6', '10.254.254.138', '1.8.1.6', '2.0.0.6', '10.254.254.138'], '10.254.254.193': ['Opps', '10.254.254.58'],
        '10.254.254.57': ['Opps', '10.254.254.28', '1.8.1.6', '2.0.0.6', '10.254.254.58'],
        '10.254.254.65': ['Opps', '10.254.254.29', '1.8.1.6', '2.0.0.6', '10.254.254.28']}

    networkGraphVisualization(toDir,adjacencyList)

if __name__ == '__main__':
  main()
