

"""
Author: Joanna Wojcik
file:
"""

import sys

from Individual import *


class BasicTSP:
    def __init__(self, _fName, _popSize, _mutationRate, _maxIterations):
        """
        Parameters and general variables
        """

        self.population     = []
        self.matingPool     = []
        self.best           = None
        self.popSize        = _popSize
        self.genSize        = None
        self.mutationRate   = _mutationRate
        self.maxIterations  = _maxIterations
        self.iteration      = 0
        self.fName          = _fName
        self.data           = {}

        self.readInstance()
        self.initPopulation()


    def readInstance(self):
        """
        Reading an instance from fName
        """
        file = open(self.fName, 'r')
        self.genSize = int(file.readline())
        self.data = {}
        for line in file:
            (id, x, y) = line.split()
            self.data[int(id)] = (int(x), int(y))
        file.close()

    def initPopulation(self):
        """
        Creating random individuals in the population
        """
        for i in range(0, self.popSize):
            individual = Individual(self.genSize, self.data)
            individual.computeFitness()
            self.population.append(individual)

        self.best = self.population[0].copy()
        for ind_i in self.population:
            if self.best.getFitness() > ind_i.getFitness():
                self.best = ind_i.copy()
        print ("Best initial sol: ",self.best.getFitness())

    def updateBest(self, candidate):
        if self.best == None or candidate.getFitness() < self.best.getFitness():
            self.best = candidate.copy()
            print ("iteration: ",self.iteration, "best: ",self.best.getFitness())

    def randomSelection(self):
        """
        Random (uniform) selection of two individuals
        """
        indA = self.matingPool[ random.randint(0, self.popSize-1) ]
        indB = self.matingPool[ random.randint(0, self.popSize-1) ]
        return [indA, indB]

    def rouletteWheel(self):
        """
        Your Roulette Wheel Selection Implementation
        """
        pass

    def uniformCrossover(self, indA, indB):
        """
        Your Uniform Crossover Implementation
        """


        keepGenesA = self.pickGenesToKeep(indA, 50)
        keepGenesB = self.pickGenesToKeep(indB, 50)

        print("indA genes are: {0} ".format(indA.genes))
        print("keep genes A is: {0} ".format(keepGenesA))

    def pickGenesToKeep(self, genesList, chanceToKeep):
        """
        Randomly picks genes, to be retained in the list. The probability of keeping the gene is mutable. Genes

        :param genesList: list of genes to be filtered
        :param chanceToKeep: the probability required to keep the gene
        :return: list of retained genes
        """
        keepGenes = []
        for i in range(0, self.genSize):
            #    print(indA.genes[i])
            if random.randint(0, 100) > chanceToKeep:
                keepGenes.append(genesList.genes[i])
            else:
                keepGenes.append(None)

        return keepGenes

    def cycleCrossover(self, indA, indB):
        """
        Your Cycle Crossover Implementation
        """
        pass

    def reciprocalExchangeMutation(self, ind):
        """
         Mutate an individual by swapping two cities with certain probability (i.e., mutation rate)
         """
        if random.random() > self.mutationRate:
            return
        indexA = random.randint(0, self.genSize-1)
        indexB = random.randint(0, self.genSize-1)

        tmp = ind.genes[indexA]
        ind.genes[indexA] = ind.genes[indexB]
        ind.genes[indexB] = tmp

        ind.computeFitness()
        self.updateBest(ind)

    def scrambleMutation(self, ind):
        """
        Mutate an individual by shuffling the genes between selected locations
        """
        if random.random() > self.mutationRate:
            return

        indexA = random.randint(0, self.genSize-2)
        # need to ensure that the end index of the mutation range is greater than the start one
        indexB = random.randint(indexA + 1, self.genSize-1)
        toBeShuffled = ind.genes[indexA:indexB]

        random.shuffle(toBeShuffled)
        ind.genes[indexA:indexB] = toBeShuffled

        ind.computeFitness()
        self.updateBest(ind)

    def crossover(self, indA, indB):
        """
        Executes a 1 order crossover and returns a new individual
        """
        child = []
        tmp = {}

        indexA = random.randint(0, self.genSize-1)
        indexB = random.randint(0, self.genSize-1)

        for i in range(0, self.genSize):
            if i >= min(indexA, indexB) and i <= max(indexA, indexB):
                tmp[indA.genes[i]] = False
            else:
                tmp[indA.genes[i]] = True
        aux = []
        for i in range(0, self.genSize):
            if not tmp[indB.genes[i]]:
                child.append(indB.genes[i])
            else:
                aux.append(indB.genes[i])
        child += aux
        return child

    # def mutation(self, ind):
    #     """
    #     Mutate an individual by swaping two cities with certain probability (i.e., mutation rate)
    #     """
    #     if random.random() > self.mutationRate:
    #         return
    #     indexA = random.randint(0, self.genSize-1)
    #     indexB = random.randint(0, self.genSize-1)
    #
    #     tmp = ind.genes[indexA]
    #     ind.genes[indexA] = ind.genes[indexB]
    #     ind.genes[indexB] = tmp
    #
    #     ind.computeFitness()
    #     self.updateBest(ind)

    def updateMatingPool(self):
        """
        Updating the mating pool before creating a new generation
        """
        self.matingPool = []
        for ind_i in self.population:
            self.matingPool.append( ind_i.copy() )

    def newGeneration(self):
        """
        Creating a new generation
        1. Selection
        2. Crossover
        3. Mutation
        """
        for i in range(0, len(self.population)):
            """
            Depending of your experiment you need to use the most suitable algorithms for:
            1. Select two candidates
            2. Apply Crossover
            3. Apply Mutation
            """
            [ind1, ind2] = self.randomSelection()
            child = self.uniformCrossover(ind1, ind2)
            self.population[i].setGene(child)
            self.scrambleMutation(self.population[i])

    def GAStep(self):
        """
        One step in the GA main algorithm
        1. Updating mating pool with current population
        2. Creating a new Generation
        """

        self.updateMatingPool()
        self.newGeneration()

    def search(self):
        """
        General search template.
        Iterates for a given number of steps
        """
        self.iteration = 0
        while self.iteration < self.maxIterations:
            self.GAStep()
            self.iteration += 1

        print ("Total iterations: ",self.iteration)
        print ("Best Solution: ", self.best.getFitness())

if len(sys.argv) < 2:
    print ("Error - Incorrect input")
    print ("Expecting python BasicTSP.py [instance] ")
    sys.exit(0)


problem_file = sys.argv[1]

ga = BasicTSP(sys.argv[1], 100, 0.1, 300)
ga.search()