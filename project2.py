# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 09:48:52 2019

@author: ronald kongi
"""
import os
import math
import copy
import time


class Point():
    '''Point Class with three proprieties'''
    def __init__(self, x, y, num):
        self.long = x # x coordinate
        self.lat = y # y coordinate
        self.id = num # For string representation as a number
    def __repr__(self):
        return str(self.id)
        
def readfile_tsp(tspfile:str):
    ''' Read a tsp file return a array of Points'''
    points = list()
    file = open(tspfile, "r")
    count = 0
    for line in (file.readlines())[7:]:
        city = Vertice(float(line.split()[1]), float(line.split()[2]), int(line.split()[0]))
        points.append(city)
        count += 1
    return points

class Vertice(Point):
    def __init__(self,x,y,num):
        super().__init__(x,y, num)
        self.isVisited = False
        self.isEncountered = False
        self.preVisit = False
        self.postVisit = False
        self.dist = 0
        self.child = list()

class Edge:
    def __init__(self, v1, v2):
        self.start = v1
        self.end = v2
    def __repr__(self):
        return "<" + str(self.start) + "," + str(self.end) + ">"
    def distance():
        return math.sqrt((start.long - end.long)**2 + (start.lat - end.long)**2)

class Graph():
    def __init__(self):
        self.vertices = list()
        self.edges = list()
    def addVertice(self, v):
        self.vertices.append(v)
    def addEdge(self, v1, v2):
        self.edges.append(Edge(v1, v2))

    def getNeighbor(self, vertex):
        neighbor = list()
        for vector in self.edges:
            if vector.start == vertex:
                neighbor.append(vector.end)
        return neighbor

    def __repr__(self):
        return "Vertices: " + str(self.vertices) + "\nEdges: " + str(self.edges)

def extracttsp():
    '''Extract all tsp files in the current directory returns an array of filenames'''
    files = list()
    for file in os.listdir():
        if(".tsp" in file):
            files.append(file)
    return files

def distance(arr):
    '''This function find the dtotal distance from the first element
    in the array to the last
    @params an array of Points
    return a float rounded'''
    total = 0
    for i in range(len(arr) - 1):
        total += math.sqrt((arr[i].lat - arr[i+1].lat)**2 + (arr[i].long - arr[i+1].long)**2)
    return round(total, 0)


def breadthFirstSearch(graph_n):
    '''
    BFS algorithm implementation
    @params a Graph Object
    @retun graph and bfs time of the first encounter of the target
    '''
    
    bfs_start = time.perf_counter_ns()
    bfs_stop = time.perf_counter_ns()
    state = False
    my_graph = dict()
    queue = list()
    graph_n.vertices[0].isEncountered = True
    queue.insert(0, graph_n.vertices[0])
    while len(queue) != 0:
        w = queue.pop()
        w.isVisited = True
        w.child = graph_n.getNeighbor(w)
        if(len(w.child) != 0):
            my_graph.update({w:w.child})
        for vertex in graph_n.getNeighbor(w):
            if not(vertex.isEncountered):
                vertex.isEncountered = True
                if vertex == graph_n.vertices[len(graph_n.vertices) -1] and state == False:
                    bfs_stop = time.perf_counter_ns() - bfs_start
                    state = True
                vertex.dist = w.dist + 1
                queue.insert(0, vertex)
    return my_graph,bfs_stop

def DepthFirstSearch(graph_n):
    '''
    DFS algorithm implementation
    @params a Graph Object
    @Print path and dfs time of the first encounter of the target
    '''
    vertex =graph_n.vertices[0]
    dfs_start = time.perf_counter_ns()
    RecursiveDFS(vertex, graph_n, dfs_start )

def RecursiveDFS(vertex, graph_n, time_e, arr=[], path=[]):
    time_e = time_e
    vertex.isEncountered = True
    vertex.preVisit = True
    if vertex != graph_n.vertices[len(graph_n.vertices) -1]:
        arr.append(vertex)
        for neighbor in graph_n.getNeighbor(vertex):
            if (neighbor.isEncountered) == False:
                RecursiveDFS(neighbor, graph_n, time_e)
    else:
        arr.append(vertex)
        path = arr[::]
        print("Using DFS:")
        print("Time Elapsed to find Target City '", graph_n.vertices[len(graph_n.vertices) -1], "': ", time.perf_counter_ns() - time_e, "nanoseconds")
        print("\tPath: ", path,"\n\tDistance (Number of edges): ", len(path) -1, "\n\tDistance (Weights): ", distance(path))

    vertex.postVisit = True

def findAllPaths(graph:dict, start:Vertice, end:Vertice, path=[]):
    path = path + [start]
    if start == end:
        return path
    if  not (start in  graph.keys()):
        return []
    paths =[]
    for node in graph[start]:
        if node not in path:
            newpaths = findAllPaths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def splitPaths(paths:list, lastPoint:Vertice):
    ind_paths = list()
    temp = list()
    for ver in paths:
        if(ver == lastPoint):
            temp.append(ver)
            ind_paths.append(temp)
            temp = list()
        else:
            temp.append(ver)
    return ind_paths

def shortestPathsBFS(paths: list):
    shortest_paths = list()
    shortest_dist = len(paths[0])
    for path in paths:
        dist = len(path) - 1
        if dist < shortest_dist:
            shortest_paths.clear()
            shortest_paths.append(path)
            shortest_dist = dist
        elif dist == shortest_dist:
            shortest_paths.append(path)
    return shortest_paths, shortest_dist

def shortestPathInPaths(paths:list):
    '''
    @params a list of vertices
    @return the shortest paths and distance
    '''
    shortest_paths = list()
    shortest_dist = distance(paths[0])
    for path in paths:
        dist = distance(path)
        if dist < shortest_dist:
            shortest_paths.clear()
            shortest_paths.append(path)
            shortest_dist = dist
        elif dist == shortest_dist:
            shortest_paths.append(path)
    return shortest_paths, shortest_dist


def main():
    graph = Graph()
    dir_files = extracttsp() #extract all the tsp file in the current directory
    for file in dir_files:
        print("In ",file, ": ")
        vertices = readfile_tsp(file)
        for vertice in vertices:
            graph.addVertice(vertice)
    #Defining connection betweens vertices
    graph.addEdge(graph.vertices[0], graph.vertices[1])
    graph.addEdge(graph.vertices[0], graph.vertices[2])
    graph.addEdge(graph.vertices[0], graph.vertices[3])
    graph.addEdge(graph.vertices[1], graph.vertices[3])
    graph.addEdge(graph.vertices[2], graph.vertices[3])
    graph.addEdge(graph.vertices[2], graph.vertices[4])
    graph.addEdge(graph.vertices[3], graph.vertices[4])
    graph.addEdge(graph.vertices[3], graph.vertices[5])
    graph.addEdge(graph.vertices[3], graph.vertices[6])
    graph.addEdge(graph.vertices[4], graph.vertices[6])
    graph.addEdge(graph.vertices[4], graph.vertices[7])
    graph.addEdge(graph.vertices[5], graph.vertices[7])
    graph.addEdge(graph.vertices[6], graph.vertices[8])
    graph.addEdge(graph.vertices[6], graph.vertices[9])
    graph.addEdge(graph.vertices[7], graph.vertices[8])
    graph.addEdge(graph.vertices[7], graph.vertices[9])
    graph.addEdge(graph.vertices[7], graph.vertices[10])
    graph.addEdge(graph.vertices[8], graph.vertices[10])
    graph.addEdge(graph.vertices[9], graph.vertices[10])

    #Copy of the graph to test on DFS
    graph2 = copy.deepcopy(graph)

    #Displaying Results
    test, time_bfs = breadthFirstSearch(graph)
    all_paths = findAllPaths(test, graph.vertices[0], graph.vertices[10])
    co_paths = splitPaths(all_paths, graph.vertices[10])
    print("Using BFS, Possible Path(s) with the shortest number of connections(edges):")
    print("Time Elapsed To Find Target City '11': ",time_bfs, "nanoseconds")
    s_paths, s_dist = shortestPathsBFS(co_paths)
    for s_path in s_paths:
        print("\tShortest Paths: ", s_path, "\n\tDistance (number of edges): ", s_dist, "\n\tDistance (Weight): ", distance(s_path))
    
    n_paths, n_dist =shortestPathInPaths(co_paths)

    DepthFirstSearch(graph2)
    print("By generating all possible paths the shortest one in term of euclidian distance between points (Weights) ")
    print("\tThe Shortest Path: ", n_paths,"\n\tDistance (Number of edges): ", len(n_paths), "\n\tDistance (Weights): ", n_dist)

    

if __name__ == "__main__":
    main()
