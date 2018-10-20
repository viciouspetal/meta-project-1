

"""
Author: Alejandro Arbelaez (Alejandro.Arbelaez@cit.ie)
Basic TSP Example
file: Individual.py
"""

import random
import math


class Individual:
    def __init__(self, _size, _data):
        """
        Parameters and general variables
        """
        self.fitness    = 0
        self.genes      = []
        self.genSize    = _size
        self.data       = _data
        self.selectionWeight = 0

        self.genes = list(self.data.keys())

        for i in range(0, self.genSize):
            n1 = random.randint(0, self.genSize-1)
            n2 = random.randint(0, self.genSize-1)
            tmp = self.genes[n2]
            self.genes[n2] = self.genes[n1]
            self.genes[n1] = tmp

    def setSelectionWeight(self, weight):
        self.selectionWeight = weight

    def setGene(self, genes):
        """
        Updating current choromosome
        """
        self.genes = []
        for gene_i in genes:
            self.genes.append(gene_i)

    def copy(self):
        """
        Creating a new individual
        """
        ind = Individual(self.genSize, self.data)
        for i in range(0, self.genSize):
            ind.genes[i] = self.genes[i]
        ind.fitness = self.getFitness()
        return ind

    def euclideanDistance(self, c1, c2):
        """
        Distance between two cities
        """
        d1 = self.data[c1]
        d2 = self.data[c2]
        return math.sqrt( (d1[0]-d2[0])**2 + (d1[1]-d2[1])**2 )

    def getFitness(self):
        return self.fitness

    def computeFitness(self):
        """
        Computing the cost or fitness of the individual
        """
        self.fitness = self.euclideanDistance(self.genes[0], self.genes[len(self.genes)-1])
        for i in range(0, self.genSize-1):
            self.fitness += self.euclideanDistance(self.genes[i], self.genes[i+1])

    def computeFitness2(ind):
        """
        Computing the cost or fitness of the individual
        """
        fitness = Individual.euclideanDistance2(ind, ind.genes[0], ind.genes[len(ind.genes)-1])
        for i in range(0, ind.genSize-1):
            fitness += Individual.euclideanDistance2(ind, ind.genes[i], ind.genes[i+1])
        return fitness

    def euclideanDistance2(ind, c1, c2):
        """
        Distance between two cities
        """
        #print('C1: {0}, C2: {1}'. format(c1, c2))

        d1 = ind.data[c1]
        d2 = ind.data[c2]
        #print('d1: {0}, d2: {1}'. format(d1, d2))
        return math.sqrt( (d1[0]-d2[0])**2 + (d1[1]-d2[1])**2 )