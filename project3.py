# -*- coding: utf-8 -*-
"""
Created on Tue Sept 17 09:48:52 2019

@author: ronald kongi
"""
import os
import math
import matplotlib.pyplot as plt


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
        city = Point(float(line.split()[1]), float(line.split()[2]), int(line.split()[0]))
        points.append(city)
        count += 1
    return points

class Edge:
    '''Edge object with two point as extremity'''
    def __init__(self, v1, v2):
        self.start = v1
        self.end = v2
    def __repr__(self):
        return "<" + str(self.start) + "," + str(self.end) + ">"
    def distance(self):
        return math.sqrt((self.start.long - self.end.long)**2 + (self.start.lat - self.end.long)**2)


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

def distanceP(point1, point2):
    '''This function find the dtotal distance from the first element
    in the array to the last
    @params an array of Points
    return a float rounded'''
    total = math.sqrt((point1.lat - point2.lat)**2 + (point1.long - point2.long)**2)
    return round(total, 0)

def dist_point_line(edge:Edge, point: Point):
    '''
    Compute and return the distance between from a point to a segment of line
    @input an edge and a point
    @retun a float, the distance
    '''
    num = abs(((edge.end.long - edge.start.long) * (edge.start.lat - point.lat))-((edge.start.long - point.lat) * (edge.end.lat - edge.start.lat)))
    den = math.sqrt((edge.end.long - edge.start.long)**2 + (edge.end.lat - edge.start.lat)**2)
    return num / den

def get3closestPoint(points:list):
    '''extract tree object point from the list and returns it as a new list'''
    point1 = points.pop()
    point2 = Point(0,0,0)
    point3 = Point(0,0,0)
    s_dist = 0
    for p in points:
        dist = distanceP(p, point1)
        if s_dist == 0:
            s_dist = dist
            point2 = p
        elif dist < s_dist :
            s_dist = dist
            point2 = p
    for city in points:
                if city.lat == point2.lat and city.long == point2.long:
                    points.remove(city)
    s_dist = 0
    for p in points:
        dist = distanceP(p, point2)
        if s_dist == 0:
            s_dist = dist
            point3 = p
        elif dist < s_dist :
            s_dist = dist
            point3 = p
        else:
            pass
    for city in points:
                if city.lat == point3.lat and city.long == point3.long:
                    points.remove(city)
    return [point1, point2, point3]

def ploting(edges:list(), points:list()):
    '''Display points and edges'''
    for point in points:
        plt.plot(point.long, point.lat, 'o')
        plt.text(point.long, point.lat, str(point.id))
        plt.axis('off')
    for edge in edges:
        plt.plot([edge.start.long, edge.end.long], [edge.start.lat, edge.end.lat], marker='o')
    plt.show()

def main():
    dir_files = extracttsp() #extract all the tsp file in the current directory
    for file in dir_files:
        print(file, ": ")
        cities = readfile_tsp(file)
        cities.reverse()
        points = get3closestPoint(cities) #Inittial 3 points
        print("Initial 3 cities ", points)
        edges = [Edge(points[0], points[1]), Edge(points[0], points[2]), Edge(points[1], points[2])] #Initial 3 edges
        while(len(cities) > 0): # itterate until cities list is empty
            vert = Point(0,0,0)
            ed = Edge(vert, vert)
            shortest = 0.0
            ref = points[-1]
            for citie in cities:
                for edge in edges:
                    dist = dist_point_line(edge, citie)
                    if shortest == 0.0:
                        shortest = dist
                        vert = citie
                        ed = edge
                    elif dist < shortest:
                        shortest = dist
                        vert = citie
                        ed = edge
                    else:
                        pass
            
            points.append(vert)
            #print("Inside City queue: ", cities)
            edge1 = Edge(vert, ed.start)
            edge2 = Edge(vert, ed.end)
            edges.append(edge1)
            edges.append(edge2)
            for edge in edges:
                if edge.start.long == ed.start.long and edge.start.lat == ed.start.lat and edge.end.long == ed.end.long and edge.end.lat == ed.end.lat:
                    edges.remove(edge)
            print("Adding Point ", vert, " Removing Edge ", ed, " Adding Edges: ", edge1, " and ", edge2)
            for city in cities:
                if city.lat == vert.lat and city.long == vert.long:
                    cities.remove(city)
            print("Tour: ", points)
        print("Combined Length using Greedy Heurestic Approach: ", distance(points))
        print("E: ", edges)
        print("P:", points)
        points.append(points[0])
        ploting(edges, points)

        

if __name__ == '__main__':
    main()