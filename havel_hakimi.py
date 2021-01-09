## =========================================
## Comment section.
"""
    This code invokes the havel-hakimi method to generate graphs from an eligible degree sequence, printing the generated graph to an outputFile in uel format

    program invocation: python havel_hakimi.py --myDegreeSequence degreeSequence --order graphOrder --outputFile outputfilename

    program arguments:

        argument variable name: degreeSequence
        argument variable type: list
        default argument variable value: --
        argument type in method signature (e.g., input, output): input
        variable description: A list containing the desired degrees of nodes in a graph. If a graph exists with this degree sequence, 
        this code will generate it

        argument variable name: order
        argument variable type: int
        default argument variable value: --
        argument type in method signature (e.g., input, output): input
        variable description: Represents the desired order to add nodes to the graph from the degree sequence. 0 will add nodes with the shortest degree first,
        1 will add nodes with the largest degree first, and any other number will add nodes in random order.

        argument variable name: outputfilename
        argument variable type: string
        default argument variable value: --
        variable description: The file we will be outputting the graph to. Contains all of the edges of the graph in uel format. Duplicate edges are not included.

    Notes
        1. This code prints nodes from the generated graph file, one per line
        2. This algorithm is based on the havel-hakimi algorithm
        3. This algorithm is used to test the fragility of scale-free networks based off the findings of the paper
        Scale-free networks need not be fragile by Rouzbeh Hasheminezhad, Moses Boudourides, and Ulrik Brandes
"""


## ===================================
## Imports
import argparse
import time
import copy
import random
## ==================================

def parse_args():
    parser = argparse.ArgumentParser(description='Generate a graph')
    parser.add_argument('--degreeSequence', nargs='+', type=int, help='Input file. Contents of a degree sequence in list format')
    parser.add_argument('--order', type=int, help='Order for the graph to be generated in. 0 for smallest degree first, 1 for largest degree first, any other number for randomized')
    parser.add_argument('--outputFile', type=str, help='Output file. All of the edges of the graph in uel format')

    return parser.parse_args()

def addEdge(adjList, n01, n02):
    ##Only entering an edge from n01 to n02. On an undirected graph this method must be called twice per undirected edge
    if n01 in adjList:
        aset = adjList[n01]
        aset.add(n02)
    else:
        aset = set()
        aset.add(n02)
        adjList[n01]=aset

def havel_hakimi(degSeq, seqOrder):
    ##degSeq is a list of degrees we want our nodes to have
    ##seqOrder is the order we want to connect vertices in. 0 is shortest first, 1 is largest first, 2 is randomized
    ##For now return graph as adjacency list

    adjList = dict()
    nodeId = 0

    #Make every element in the degree sequence a tuple, where the first element is the node ID and the 
    #second element is the degree of that node
    for n in range(len(degSeq)):
        deg = degSeq[n]
        degSeq[n] = (nodeId, deg)
        nodeId += 1
    #degSeq always needs to be sorted with the highest degree first because we always have to add edges to nodes with the highest degree,
    #nodeOrder is for the order that we want to add nodes to the graph in
    nodeOrder = copy.deepcopy(degSeq)
    ##We always have to connect nodes to the ones with the highest degree
    if seqOrder > 1 or seqOrder < 0:
        random.shuffle(nodeOrder)

    # Keep performing the operations until one
    # of the stopping condition is met
    while True:
        #Have to sort degSeq by highest degree each iteration in case the order changed
        degSeq = sorted(degSeq, key = lambda x: x[1], reverse=True)
        # Sort the list according to the argument specified
        if seqOrder == 0:
            nodeOrder = sorted(nodeOrder, key = lambda x: x[1])
        elif seqOrder == 1:
            nodeOrder = sorted(nodeOrder, key = lambda x: x[1], reverse=True)

        print ("nodeOrder: " + str(nodeOrder))
        print ("degSeq: " + str(degSeq))
        
        # Check if all the elements are equal to 0
        #This means that we have successfully generated a graph, and we return this graph
        if degSeq[0][1]== 0 and degSeq[len(degSeq)-1][1]== 0:
            return adjList

        # Store the first element in a variable
        # and delete it from the list
        curNode = nodeOrder[0]
        nodeOrder.pop(0)
        degSeq.remove(curNode)

        # Check if enough elements
        # are present in the list
        if curNode[1]>len(degSeq):
            print("No graph with this degree sequence exists. ERROR.")
            exit(1)

        #Add node to the graph and update degSeq and nodeOrder
        #loop over the degree of the current nodeId
        for i in range(curNode[1]):
            addNode = degSeq[i]
            addEdge(adjList,curNode[0],addNode[0])
            addEdge(adjList,addNode[0],curNode[0])
            degSeq[i] = (addNode[0], addNode[1]-1)
            nodeOrder[nodeOrder.index(addNode)] = (addNode[0], addNode[1]-1)
            

            # Check if negative element is
            # encountered after subtraction
            if degSeq[i][1]<0:
                print ("Degree sequence went negative. ERROR")
                exit(1)


def writeGraph(hh_graph, outputFile):
    o = open(outputFile,'w')
    for key in hh_graph:
        for neighbor in hh_graph[key]:
            ##write nodes to files
            if neighbor > key:
                o.write(str(key) + " " + str(neighbor) + "\n")
    o.close()



def main():
    beginTime = time.time()
    args = parse_args()
    g = havel_hakimi(args.degreeSequence, args.order)
    print (g)
    writeGraph(g, args.outputFile)
    endTime = time.time()
    duration = endTime-beginTime
    dur = duration/3600
    print ("Execution duration (seconds) = ", duration)
    print ("Execution duration (hours) = ", dur)
    return 

## ==================================
if __name__ == "__main__":
    ## Driver.
    main()
    print (" ----- good termination -----")
