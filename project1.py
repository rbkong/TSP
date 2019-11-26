# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 12:59:52 2019

@author: ronald kongi
"""
import os
import math


class Point():
    '''Point Class with three proprieties'''
    def __init__(self, x, y, num):
        self.long = x # x coordinate
        self.lat = y # y coordinate
        self.id = num # For string representation as a number
    def __repr__(self):
        return str(self.id)
        
def readfile_tsp(tspfile):
    ''' Read a tsp file return a array of Points'''
    points = list()
    file = open(tspfile, "r")
    count = 0
    for line in (file.readlines())[7:]:
        city = Point(float(line.split()[1]), float(line.split()[2]), int(line.split()[0]))
        points.append(city)
        count += 1
    return points

def distance(arr):
    '''This function find the dtotal distance from the first element
    in the array to the last
    @params an array of Points
    return a float rounded'''
    total = 0
    for i in range(len(arr) - 1):
        total += math.sqrt((arr[i].lat - arr[i+1].lat)**2 + (arr[i].long - arr[i+1].long)**2)
    return round(total, 0)

def extracttsp():
    '''Extract all tsp files in the current directory returns an array of filenames'''
    files = list()
    for file in os.listdir():
        if(".tsp" in file):
            files.append(file)
    return files[::-1]


def permutate(set_points, length):
    '''Generates all the permutations of an array of points
    and find the shortest path. 
    @params array of points and its size. Then returns shirtest path and 
    the distance'''  
    shortest_path = list()
    c = list()
    for i in range(length):
        c.append(0)
    
    initial_set = set_points[:]
    initial_set.append(initial_set[0])
    shortest_path.append(initial_set)
    dist = distance(initial_set)

    countOps = 1
    i = 0
    while i < length:
        if c[i] < i:
            if (i % 2) == 0:
                temp = set_points[i]
                set_points[i] = set_points[0]
                set_points[0] = temp
                
            else:
                temp = set_points[c[i]]
                set_points[c[i]] = set_points[i]
                set_points[i] = temp

            temp_s = set_points[:]
            temp_s.append(temp_s[0])
            if(distance(temp_s) < dist):
                shortest_path = list()
                shortest_path.append(temp_s)
                dist = distance(temp_s)

            elif(distance(temp_s) == dist):
                shortest_path.append(temp_s)

            countOps += 1
            c[i] += 1
            i = 0
        else:
            c[i] = 0
            i += 1
    return shortest_path, dist, countOps



#Main function
def main():
    dir_files = extracttsp() #extract all the tsp file in the current directory
    for file in dir_files:
        print(file, ": ")
        cities = readfile_tsp(file)
        shrtpath, dist, countingOps = permutate(cities, len(cities))
        print("Tours(", len(shrtpath),"): ", shrtpath, "\nHas ", len(cities), " edges with a combined length of ", 
        int(round(dist)) , ". Number of ops: ", countingOps, "." ) # Result output

if __name__ == '__main__':
    main()
        
            
            
            
            