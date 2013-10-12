#!/usr/bin/env python

import sys, random

try:
    import pylab
    import matplotlib.pyplot as plot
except Exception, e:
    print "***Error: either pylab or matplotlib not installed"
    print "sudo apt-get install python-numpy python-scipy python-matplotlib"
    exit(0)

GROUPS   = [2,2,2,2]
MUTATION = [-1,-1,-1,-1]
MARK     = [ ["o","b"], [".", "g"], ["x","r"], ["*", "y"] ]

def calFrac(population, size, index):
    fracX = []
    global GROUPS
    for i in range(GROUPS[index]) :
        fracX.append(population.count(i)*1.0/size)
    return fracX

def randomAlle(oldPopulation, size, index):
    length     = len(oldPopulation)
    population = []

    if length==0:
        fracX  = [0.5, 0.5]
    else :
        fracX  = calFrac(oldPopulation, size, index)

    for i in range(size):
        randNo = 0; prev = 0; flag = 0
        while(randNo==0):
            randNo = random.random()
        for j in range(GROUPS[index]):
            if randNo >= prev and randNo < prev + fracX[j] :
                flag = 1
                population.append(j)
                break
            prev += fracX[j]

        if flag==0:
            i -= 1
    return population

def mutate(population, size, typeX, index):
    global GROUPS
    for i in range(size/10):
        num = random.randint(0,size-1)
        if population[num]==typeX:
            population[num] = GROUPS[index]-1
        else:
            i-=1

    #GROUPS += 1
    return population

def checkMutation(population, size, index):
    global MUTATION
    flag = 0; newPopulation = []

    if MUTATION[index]==-1:
        for i in range(GROUPS[index]):
            #fracX =  population.count(i)*1.0/size
            fracX =  population.count(0)*1.0/size
            if fracX > 0.85:
                flag            = 1
                #MUTATION[index] = i
                MUTATION[index] = 0
                GROUPS[index]  += 1
                newPopulation   = mutate(population, size, i, index)
                break

    elif MUTATION[index]!=-1:
        pass
        #mutFrac = population.count(MUTATION[index])*1.0/size
        #if mutFrac > 0.85:
            #flag          = 1
            #newPopulation = mutate(population, size, MUTATION[index], index)

    if flag == 0:
        return population
    else :
        return newPopulation

def simulateGeneration(population):
    totA=0; totB=0
    for i in range(len(population)):
        population[i] = randomAlle(population[i], len(population[i]), i)
        population[i] = checkMutation(population[i], len(population[i]), i)
        print "Allel frequency ",i, " :",
        for j in range( GROUPS[i] ):
            print population[i].count(j),
        print ""

def plotGraph(points, x, clr):
    global MARK
    for i in range(len(points)):
        pylab.plot( points[i][0], points[i][1], x, color = clr )

def main():
    if len(sys.argv) < 3:
        print "Usage : python prob2.py <#population size> <#number of generations>"
        exit(0)

    pop_size   = int(sys.argv[1])
    N          = pop_size/4
    iterarions = int(sys.argv[2])
    print "Population Size : ", pop_size
    initPopulation = randomAlle([], pop_size, 0)
    population = [ initPopulation[i:i+N] for i in range(0, len(initPopulation), N)]
    #print population, initPopulation.count(0), initPopulation.count(1)
    points = [[],[],[],[]]
    #for j in range(4):
    #    points[j].append( [0, population[j].count(0)] )

    for i in range(iterarions):
        print "Generation no : ", i
        simulateGeneration(population)
        for j in range(3):
            sumX = 0
            for k in range(4):
                sumX +=  population[k].count(j)
            points[j].append( [i+1, sumX ] )

    # ploting graph
    for i in range(3):
        plotGraph(points[i], MARK[i][0], MARK[i][1] )
    plot.show()

if __name__ == '__main__':
    main()
