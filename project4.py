# -*- coding: utf-8 -*-
"""
Created on Tue Sept 17 09:48:52 2019
@title: TSP - Genetic Algorithm
@description: Find the shortest path using genetic algorithm on a TSP
@author: ronald kongi
"""
import os
import math, random, time
import matplotlib.pyplot as plt
import numpy as np



class Point():
    '''Point Class with three proprieties'''
    def __init__(self, x, y, num):
        self.long = x # x coordinate
        self.lat = y # y coordinate
        self.id = num # For string representation as a number
    def __repr__(self):
        return str(self.id)
        
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

def notinList(point:Point, points:list):
    if len(points) == 0:
        return True
    for p in points:
        if point.id == p.id:
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
        for j in range(100):
            point = rawList.pop(random.randint(0,len(rawList) - 1))
            newList.append(point)
        pathsPop.append(newList)
    return pathsPop


def crossover(path1:list, path2:list, type:int):
    '''Cross Over two paths to generate a pair of path
    '''
    if type == 1:
        newkid1, newkid2 = list(), list()
        pathBlocks = [path1[:20], path1[20:40], path1[40:60], path1[60:80], path1[80:100]]
        for i in range(5):
            if (i % 2) == 0:
                 newkid1 += pathBlocks[i]
            else:
                count = 0
                for point in path2:
                    if count == 20:
                        break
                    if point not in newkid1:
                        newkid1.append(point)
                        count += 1
        pathBlocks2 = [path2[:20], path2[20:40], path2[40:60], path2[60:80], path2[80:100]]
        for i in range(5):
            if (i % 2) == 0:
                 newkid2 += pathBlocks2[i]
            else:
                count = 0
                for point in path1:
                    if count == 20:
                        break
                    if point not in newkid2:
                        newkid2.append(point)
                        count += 1
        return newkid1, newkid2
    else:
        kid = list()
        pathBlocks = [path1[:20], path1[20:40], path1[40:60], path1[60:80], path1[80:100]]
        block1 = distance(path1[:20])
        block2 = distance(path1[20:40])
        block3 = distance(path1[40:60])
        block4 = distance(path1[60:80])
        block5 = distance(path1[80:100])
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
                kid += pathBlocks[i]
            else:
                count = 0
                for point in path2:
                    if count == 20:
                        break
                    if point not in kid:
                        kid.append(point)    
                        count +=1
                    
        kid2 = list()
        pathBlocks2 = [path2[:20], path2[20:40], path2[40:60], path2[60:80], path2[80:100]]
        block12 = distance(path2[:20])
        block22 = distance(path2[20:40])
        block32 = distance(path2[40:60])
        block42 = distance(path2[60:80])
        block52 = distance(path2[80:100])
        distBlocks2 = [block12, block22, block32,  block42, block52]
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
                    if count == 20:
                        break
                    
                    if point not in kid2:
                        kid2.append(point)    
                        count +=1
        return kid, kid2
                    
                        
    

    
def mutation(path:list, type:int):
    '''Flip value in path depending of the probability of
    mutation
    '''
    newpath = list()
    if type == 1:
        index_1 = random.randint(0, len(path) -1)
        index_2 = random.randint(0, len(path) -1)
        temp1 = path[index_1]
        temp2 = path[index_2]
        newpath = path[:]
        newpath[index_2] = temp1
        newpath[index_1] = temp2
        return path
    else:
        index_1 = len(path) // 2
        index_2 = (len(path) // 2) + 1
        temp1 = path[index_1]
        temp2 = path[index_2]
        newpath = path[:]
        newpath[index_2] = temp1
        newpath[index_1] = temp2
        return newpath
        
def ploting(points:list()):
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
    #plt.savefig("data/" + path +name + ".jpg")
    plt.show()
    
def improv_curves(maxV:list, minV:list, path:str):
    
    labels = list()
    for i in range(len(maxV)):
        labels.append("G" + str(i + 1))
    
    max_means = maxV
    min_means = minV

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, max_means, width, label='Shortest')
    rects2 = ax.bar(x + width/2, min_means, width, label='Longest')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Distance')
    ax.set_title('Improvovement Curves')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()


    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')


    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()
    #plt.savefig("data/"+ path +"/curves.jpg")
    plt.show()
        
    
def ga(initial_pop:list, pCross:float, pmut:float, cross:int, mut:int):
    start_time = time.time()
    prob_cross = int((pCross * len(initial_pop))/2)
    prob_mut = int((pmut * len(initial_pop))/2)
    actualgen = initial_pop[:]
    ittr = 0
    max_values = list()
    paths = list()
    min_values = list()
    mut_switch = False
    while ittr < len(initial_pop):
        actualgen = sorted(actualgen, key=distance)
        ittr = actualgen.count(actualgen[0])
        newgen =list()
        temp = actualgen[:len(actualgen) - (prob_cross * 2)]
        paths.append(actualgen[0])
        max_values.append(distance(actualgen[0]))
        min_values.append(distance(actualgen[-1]))
        for i in range(prob_cross):
            kid1, kid2 = crossover(actualgen.pop(0), actualgen.pop(0), cross)
            newgen.append(kid1)
            newgen.append(kid2)
        
        actualgen = list()
        actualgen += newgen
        actualgen += temp
        for i in range(prob_mut):
            if mut_switch:
                choice = random.randint(0, len(actualgen) - 1)
                actualgen[choice] = mutation(actualgen[choice],mut)
        mut_switch = not mut_switch
            
        
    return max_values, min_values, paths, time.time() - start_time

def main():
     dir_files = extracttsp() #extract all the tsp file in the current directory
     for file in dir_files:
        print("starting...")
        cities = readfile_tsp(file)
        initial = generationInitial(cities, 100000)
        initial2 = generationInitial(cities, 100000)
        for i in range(1,3):
            print("\t\tDataSet " + str(i) + "\n\n")
            max_vls, min_vls, path_vls, exec_time = ga(initial, 0.8, 0.1, 1, i)
            for path in path_vls:
                ploting(path, "","")
            improv_curves(max_vls, min_vls, "")
            print(str(max_vls) + "\n")
            print(str(min_vls) + "\n")
            print(str(path_vls) + "\n")
            print(str(exec_time) + " seconds\n")

        for i in range(1,3):
            print("\t\tDataSet " + str(i + 2) + "\n\n")
            max_vls, min_vls, path_vls, exec_time = ga(initial2, 0.8, 0.1, 2, i)
            for path in path_vls:
                ploting(path,"","")
            improv_curves(max_vls, min_vls,"")
            print(str(max_vls) + "\n")
            print(str(min_vls) + "\n")
            print(str(path_vls) + "\n")
            print(str(exec_time) + " seconds\n")

if __name__ == '__main__':
    main()
