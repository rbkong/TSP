# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 17:15:21 2019

@author: rk9ro
"""
import os
import math, random, operator, time
import matplotlib.pyplot as plt

class Point():
    '''Point Class with three proprieties'''
    def __init__(self, x, y, num):
        self.long = x # x coordinate
        self.lat = y # y coordinate
        self.id = num # For string representation as a number
        self.conn = 0
    def __repr__(self):
        return str(self.id)
    
class Edge:
    def __init__(self, v1, v2):
        self.start = v1
        self.end = v2
    def __repr__(self):
        return "<" + str(self.start) + "," + str(self.end) + ">"
    def distance(self):
        return math.sqrt((self.start.long - self.end.long)**2 + 
                         (self.start.lat - self.end.long)**2)
        
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
    
    def isEdgeIn(self, edge):
        if edge in self.edges:
            return True
        elif Edge(edge.end, edge.start) in self.edges:
            return True
        else:
            return False

    def __repr__(self):
        return "Vertices: " + str(self.vertices) + "\nEdges: "  + str(self.edges)
    
def readfile_tsp(tspfile: str):
    ''' Read a tsp file return a array of Points'''
    points = list()
    file = open(tspfile, "r")
    count = 0
    for line in (file.readlines())[7:]:
        city = Point(float(line.split()[1]), float(line.split()[2]),
                     int(line.split()[0]))
        points.append(city)
        count += 1
    return points

def extracttsp():
    '''Extract all tsp files in the current directory returns an array of 
    filenames
    '''
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
        total += math.sqrt((arr[i].lat - arr[i+1].lat)**2 + 
                           (arr[i].long - arr[i+1].long)**2)
    return round(total, 0)

def distanceP(point1, point2):
    '''This function find the dtotal distance from the first element
    in the array to the last
    @params an array of Points
    return a float rounded'''
    total = math.sqrt((point1.lat - point2.lat)**2 + (point1.long - point2.long)**2)
    return round(total, 0)

def notinList(point, points:list):
    if len(points) == 0:
        return True
    for p in points:
        if (p.id - point.id) == 0:
            return False
    return True

def generationInitial(cities : list(), initialSize:int):
    '''
    @descrip:Randomly generates a population of N members from a list of Points
    @input: list of Points of size L, number of desired size of the population
    @output: a list of  N paths(set of points of equal size L)
    '''
    pathsPop =  list()
    for i in range(initialSize):
        rawList = cities[:]
        newList = list()
        for j in range(len(cities)):
            point = rawList.pop(random.randint(0,len(rawList) - 1))
            newList.append(point)
        pathsPop.append(newList)
    return pathsPop

def crossover(path1:list, path2:list):
    '''Cross Over two paths to generate a pair of path
    '''
    offset = len(path1) // 5
    off2 = offset * 2
    off3 = off2 + offset 
    off4 = off3 + offset 
    kid1, kid2 = list(), list()
    pathBlocks = [path1[:offset], path1[offset:off2], path1[off2:off3], path1[off3:off4],
                  path1[off4:]]
    block1 = distance(path1[:offset])
    block2 = distance(path1[offset:off2])
    block3 = distance(path1[off2:off3])
    block4 = distance(path1[off3:off4])
    block5 = distance(path1[off4:])
    distBlocks = [block1, block2, block3,  block4, block5]
    tup_block = list()
    for i in range(5):
        temp  = distBlocks[i]
        ind_num = 4
        for j in range(5):
            if temp < distBlocks[j]:
                ind_num -= 1
        tup_block.append((temp, ind_num))

    for i in range(5):
        if tup_block[i][1] < 3:
            kid1 += pathBlocks[i]
        else:
            count = 0
            for point in path2:
                if count < 1:
                    break
                if point not in kid1:
                    kid1.append(point)    
                    count -=1
                    
    pathBlocks2 = [path2[:offset], path2[offset:off2], path2[off2:off3], path2[off3:off4],
                  path2[off4:]]
    block21 = distance(path2[:offset])
    block22 = distance(path2[offset:off2])
    block23 = distance(path2[off2:off3])
    block24 = distance(path2[off3:off4])
    block25 = distance(path2[off4:])
    distBlocks2 = [block21, block22, block23,  block24, block25]
    tup_block2 = list()
    for i in range(5):
        temp  = distBlocks2[i]
        ind_num = 4
        for j in range(5):
            if temp < distBlocks2[j]:
                ind_num -= 1
        tup_block2.append((temp, ind_num))

    for i in range(5):
        if tup_block2[i][1] < 3:
            kid2 += pathBlocks2[i]
        else:
            count = 0
            for point in path1:
                if count < 1:
                    break
                if point not in kid2:
                    kid2.append(point)    
                    count -=1
    
    
    kid1 = list(dict.fromkeys(kid1))
    kid2 = list(dict.fromkeys(kid2))
    
    if len(kid1) < len(path1):
        for e in path1:
            if notinList(e, kid1):
                kid1.append(e)
    
    if len(kid2) < len(path2):
        for e in path2:
            if notinList(e, kid2):
                kid2.append(e)
    
    return kid1, kid2 
                    
                        

def ga(initial_pop:list, pCross:float, pmut:float):
    prob_cross = int((pCross * len(initial_pop))/2)
    actualgen = initial_pop[:]
    ittr = 0
    paths = list()
    while ittr < (len(initial_pop) / 2):
        actualgen = sorted(actualgen, key=distance)
        ittr += 1
        newgen =list()
        temp = actualgen[:len(actualgen) - (prob_cross * 2)]
        paths.append(actualgen[0])
        for i in range(prob_cross):
            kid1, kid2 = crossover(actualgen.pop(0), actualgen.pop(0))
            newgen.append(kid1)
            newgen.append(kid2)
        
        actualgen = list()
        actualgen += newgen
        actualgen += temp            
        
    return paths
    

def convertToPoint(num:int, points:list):
    for point in points:
        if point.id == num:
            return point

def woC(cities:list, segment, init, expert_p:float, pCross, pMut):
    prob_cross = int(pCross * segment)
    expert = list()
    for i in range(segment):
        initial  = generationInitial(cities, init)
        shortest_path = ga( initial, pCross, pMut)
        expert.append(shortest_path[-1])
                
    expert = sorted(expert, key=distance)
    print("Done 1")
    return expert[:prob_cross]

def aggregate(solutions: list):
    matrix = list()
    
    #matrix initialization
    for i in range(len(solutions[0])):
        row = list()
        for i in range(len(solutions[0])):
            row.append(0)
        matrix.append(row)
    for solution in solutions:
        for index in range(len(solution) -2):
            element = solution[index]
            next_element = solution[index + 1]
            matrix[element.id - 1][next_element.id - 1] += 1
            matrix[next_element.id - 1][element.id - 1] += 1
    
    count = 1
    couples = list()
    for row in matrix:
        index, value = max(enumerate(row), key=operator.itemgetter(1))
        #print(count, " -> ", index + 1 )
        edge = Edge(convertToPoint(count, solutions[0]), convertToPoint(
                index + 1, solutions[0]))
        couples.append(edge)
        count += 1

    return combiningEdges(couples)

def combiningEdges(edges:list):
    #print(edges)
    grph = Graph()
    for edge in edges:
        if  not isEdgeIn(grph.edges, edge):
            grph.addEdge(edge.start, edge.end)
    
    couple = edges.pop(0)
    left = couple.start
    right = couple.end
    
    path = [left, right]
    while len(edges) > 0:
        dist = 1000000000000
        point1 = Point(0,0,0)
        point2 = Point(0,0,0)
        edge_s = Edge(point1, point2)
        side = False

        for edge in edges:
            tempL1 = 10000000000000
            tempL2 = 10000000000000
            tempR1 = 10000000000000
            tempR2 = 10000000000000
            try:
                if left.id != edge.start.id:
                    tempL1 = distanceP(left, edge.start)    
                if left.id != edge.end.id:
                    tempL2 = distanceP(left, edge.end)    
                if right.id != edge.start.id:
                    tempR1 = distanceP(right, edge.start)    
                if right.id != edge.end.id:
                    tempR2 = distanceP(right, edge.end)  
            except:
                pass
            
            current = min([tempL1, tempL2, tempR1, tempR2])
            
            if current == tempL1:
                if current < dist:
                    point1 = edge.end
                    point2 = edge.start
                    dist = current
                    edge_s = edge
                    side = False
                    
            elif current == tempL2:
                if current < dist:
                    point1 = edge.start
                    point2 = edge.end
                    dist = current
                    edge_s = edge
                    side = False
                    
            elif current == tempR1:
                if current < dist:
                    point1 = edge.start
                    point2 = edge.end
                    dist = current
                    edge_s = edge
                    side = True
                    
            elif current == tempR2:
                if current < dist:
                    point1 = edge.end
                    point2 = edge.start
                    dist = current
                    edge_s = edge
                    side = True
        
        if side:
            path.append(point1)
            path.append(point2)
            right = point2
        else:
            path.insert(0, point2)
            path.insert(0, point1)
            left = point1
        edges.remove(edge_s)
                
        
    path = list(dict.fromkeys(path))
    return path


def canAddPoint(edges:list, v1):
    #print(edges)
    count = 0
    for edge in edges:
        if (v1.id == edge.start.id) or (v1.id == edge.end.id):
            count += 1
    if count > 1:
        return False
    else:
        return True
def isEdgeIn(edges, e1):
    try:
        for edge in edges:
            if (e1.start.id == edge.start.id) and (e1.end.id == edge.end.id):
                return True
            elif (e1.end.id == edge.start.id) and (e1.start.id == edge.end.id):
                return True
        return False
    except:
        return True
    
def ploting(points:list(), name:str):
    '''Display points and edges'''
    for point in points:
        plt.plot(point.long, point.lat, 'o')
        plt.text(point.long, point.lat, str(point.id))
        plt.axis('off')
    for i in range(len(points)):
        if i == len(points) - 1:
            pass
        else:
            plt.plot([points[i].long, points[i+1].long], [points[i].lat, points[i+1].lat], marker='o')
    plt.savefig( "img/" + name + ".jpg")
    plt.clf()

def main():
    populations= [10,100,1000]
    segments = [10, 50, 100]
    dir_files = extracttsp() #extract all the tsp file in the current directory
    for file in dir_files:
        dataset = open("data/" + file[:-3] + "txt", "w")
        for population in populations:
            for segment in segments:
                dataset.writelines("starting..."  + file + " with segment " + 
                                   str(segment))
                print("starting..."  , file , " with segment " , 
                                   str(segment))
                cities = readfile_tsp(file)
                ga_timing = time.time()
                ga_gen = ga(generationInitial(cities, population), 0.8, 0.1)
                ga_timing = time.time() - ga_timing
                dataset.writelines("GA :\n" + "Path: " + str(ga_gen[-1]) + "\nDistance: "
                                   + str(distance(ga_gen[-1])) + "\nTiming: " + str(ga_timing))
                #print("GA :\n" , "Path: " , str(ga_gen[-1]) , "\nDistance: "
                                   #+ str(distance(ga_gen[-1])) , "\nTiming: " , str(ga_timing))
                woc_timing = time.time()
                woc_gen = woC(cities, segment, population, 0.8, 0.8, 0.1) 
                agg_gen = aggregate(woc_gen)
                woc_timing = time.time() - woc_timing
                dataset.writelines("Best GA In Woc input: "+ str(woc_gen[0]) + 
                                   "\nDistance: " + str(distance(woc_gen[0])))
                #print("Best GA In Woc input: ", str(woc_gen[0]) , 
                                #   "\nDistance: " , str(distance(woc_gen[0])))
                dataset.writelines("WoC: \n" + "Path: " + str(agg_gen) +
                      "\nDistance: " + str(distance(agg_gen)) + "\nTiming: " + 
                      str(woc_timing))
                #print("WoC: \n" , "Path: " , str(agg_gen) ,
                     # "\nDistance: " , str(distance(agg_gen)) , "\nTiming: " , 
                    #  str(woc_timing))
                ploting(ga_gen[-1], "ga-f" + file[:-4] + "-p" + str(population) + "-s" + str(segment))
                ploting(woc_gen[0], "gab-f" + file[:-4] + "-p" + str(population) + "-s" + str(segment))
                ploting(agg_gen, "woc-f" + file[:-4] + "-p" + str(population) + "-s" + str(segment))
        dataset.close()
            

    
    print("Job done!")

if __name__ == '__main__':
    main()

    
