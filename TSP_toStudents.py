"""
Author: Joanna Wojcik
file:
"""

import sys

from Individual import *

PARENT_B_KEY = 'parentB'
PARENT_A_KEY = 'parentA'
POSITION_KEY = 'position'


class BasicTSP:
    def __init__(self, _fName, _popSize, _mutationRate, _maxIterations):
        """
        Parameters and general variables
        """

        self.population = []
        self.matingPool = []
        self.best = None
        self.popSize = _popSize
        self.genSize = None
        self.mutationRate = _mutationRate
        self.maxIterations = _maxIterations
        self.iteration = 0
        self.fName = _fName
        self.data = {}

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
        print("Best initial sol: ", self.best.getFitness())

    def updateBest(self, candidate):
        if self.best == None or candidate.getFitness() < self.best.getFitness():
            self.best = candidate.copy()
            print("iteration: ", self.iteration, "best: ", self.best.getFitness())

    def randomSelection(self):
        """
        Random (uniform) selection of two individuals
        """
        indA = self.matingPool[random.randint(0, self.popSize - 1)]
        indB = self.matingPool[random.randint(0, self.popSize - 1)]

        return [indA, indB]

    def rouletteWheel(self):
        """
        Constructs roulette wheel selection process. Enables selecting 2 best candidates for mating
        :return: 2 best candidates
        """
        totalFitness = self.computeTotalFitness()

        rouletteWheel = self.constructTheRouletteWheel()

        return self.spinRouletteWheel(rouletteWheel, totalFitness)

    def spinRouletteWheel(self, weightedSelectionSpace, endOfSelectionSpace):
        """
        Simulates spinning of a roulette wheel in order to select 2 best candidates.

        :param weightedSelectionSpace: roulette wheel with weights of the selection probability applied
        :param endOfSelectionSpace: sum of the individual fitness parameters. Marks the end of the selection space
        :return: 2 best candidates
        """
        spin1 = random.uniform(0, endOfSelectionSpace)
        spin2 = random.uniform(0, endOfSelectionSpace)

        indA = None
        indB = None

        for i in weightedSelectionSpace:
            if spin1 >= weightedSelectionSpace[i]["begin"] and spin1 < weightedSelectionSpace[i]["end"]:
                indA = self.matingPool[weightedSelectionSpace[i]["position"]]
            if spin2 >= weightedSelectionSpace[i]["begin"] and spin2 < weightedSelectionSpace[i]["end"]:
                indB = self.matingPool[weightedSelectionSpace[i]["position"]]

        return [indA, indB]

    def getFitnessRank(self):
        """
        Assigns ranks to the individuals in the population.
        First the population is sorted according to its fitness, with the individual with the highest fitness
        acquiring the highest rank. Then, each individual is assigned a rank from highest to lowest, with highest rank
        being equal to the size of the population.

        :return: list of ranked individuals from highest rank to lowest
        """
        # sorting of the population by fitness from highest to lowest
        ranks = sorted(self.matingPool, key=lambda x:x.fitness, reverse=True)

        # computing and assigning rank values
        for i in range(0, len(ranks)):
            ranks[i].setSelectionRank(self.popSize-i)
            # print('Fitness for element of {0} is {1}, rank: {2}'.format(ranks[i], ranks[i].fitness, ranks[i].selectionRank))

        return ranks[0], ranks[1]

    def computeTotalFitness(self):
        """
        Since the objective is to minimize the cost function, which is the distance between cities in the final solution
        the fitness value needs to be transformed to promote the candidates with the smallest distance between the cities.

        Additionally the total value of fitness will be computed.

        :return: total fitness value for the population
        """
        totalFitness = 0
        for i in range(0, len(self.matingPool)):
            transformedFitness = 1 / self.matingPool[i].fitness
            self.matingPool[i].setSelectionWeight(transformedFitness)
            totalFitness += transformedFitness
            # print('selection weight {0}'.format(self.matingPool[i].selectionWeight))
        return totalFitness

    def constructTheRouletteWheel(self):
        """
        Computes the roulette wheel with individuals assigned a weight, determining the probability of them being
        selected. The larger the weight the greater the chance of the individual being selected.

        :return: constructed wheel
        """
        runningTotal = 0
        wheel = {}
        for i in range(0, len(self.matingPool)):
            end = self.matingPool[i].selectionWeight + runningTotal
            wheel[i] = {"position": i, "begin": runningTotal, "end": end}
            runningTotal = end
        return wheel

    def uniformCrossover(self, indA, indB):
        """
        Randomly selects genes of an individual that will not change. The remaining positions are filled with the copy
        from the alternative parent in order of appearance. Genes from alternative parent that are already present in
        the candidate individual will not be copied.

        :param indA: parent individual A
        :param indB: parent individual A
        :return: new individual
        """

        newIndBasedOnParentA = self.pickGenesToKeep(indA, 50)

        # check if there is an intersection of values between parent B and new individual (based off of parent A)
        # if there is those are the values that will NOT be moved to the new individual

        for i in range(0, self.genSize):
            if not indB.genes[i] in newIndBasedOnParentA:
                nextFreeSlot = next(i for i, v in enumerate(newIndBasedOnParentA) if v == -1)
                newIndBasedOnParentA[nextFreeSlot] = indB.genes[i]

        return newIndBasedOnParentA

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
                keepGenes.append(-1)

        return keepGenes

    def cycleCrossover(self, indA, indB):
        """
        The Cycle Crossover implementation.

        The Cycle Crossover operator identifies a number of so-called cycles between two parents.
        Then, to form Child 1, cycle 1 is copied from parent 1, cycle 2 from parent 2, cycle 3 from parent 1, and so on.

        :param indA: parent individual 1
        :param indB: parent individual 2
        :return: an offspring object
        """

        # later on used to determine in the cycle calculation if a given gene position is free to be filled by a
        # gene from a parent or not.
        isPositionFilled = []

        # offspring objects
        child1 = []
        child2 = []

        # initialize position availability list, child1 and child2 objects
        for i in range(0, self.genSize):
            isPositionFilled.append(False)
            child1.append(None)
            child2.append(None)

        # For the benefit of performance, need to rely on hash table, or in python terms dictionary
        # for fast lookup of index values of each gene
        geneLookup = self.generate_cx_parent_lookup(indA.genes, indB.genes)

        # Compute all the cycles
        cycleTable = self.generate_all_cycles(geneLookup, indA.genes, isPositionFilled)

        # Alternate cycles to populate the offspring/child objects
        counter = 0
        for cycle in cycleTable:
            for pair in cycle:
                if counter % 2 == 0:
                    child1[pair[POSITION_KEY]] = pair[PARENT_A_KEY]
                    child2[pair[POSITION_KEY]] = pair[PARENT_B_KEY]
                else:
                    child1[pair[POSITION_KEY]] = pair[PARENT_B_KEY]
                    child2[pair[POSITION_KEY]] = pair[PARENT_A_KEY]
            counter += 1

        return child1

    def generate_all_cycles(self, geneLookup, indAGenes, isPositionFilled):
        cycleTable = []
        for i in range(0, self.genSize):
            temporaryCycle = []

            # Making sure that given value is not already in another cycle
            if not isPositionFilled[i]:
                cycleStart = indAGenes[i]
                temporaryPair = geneLookup[indAGenes[i]]
                temporaryCycle.append(temporaryPair)
                isPositionFilled[temporaryPair[POSITION_KEY]] = True

                # appending temporary pair B to the temp cycle
                while not temporaryPair[PARENT_B_KEY] == cycleStart:
                    temporaryPair = geneLookup[temporaryPair[PARENT_B_KEY]]
                    isPositionFilled[temporaryPair[POSITION_KEY]] = True
                    temporaryCycle.append(temporaryPair)

                cycleTable.append(temporaryCycle)
        return cycleTable

    def generate_cx_parent_lookup(self, ind_a_genes, ind_b_genes):
        geneLookup = {}
        for i in range(0, self.genSize):
            geneLookup[ind_a_genes[i]] = {PARENT_A_KEY: ind_a_genes[i], PARENT_B_KEY: ind_b_genes[i], POSITION_KEY: i}
            # print('lookup {0}'. format(geneLookup[ind_a_genes[i]]))
        return geneLookup

    def reciprocalExchangeMutation(self, ind):
        """
         Mutate an individual by swapping two cities with certain probability (i.e., mutation rate)
         """
        if random.random() > self.mutationRate:
            return
        indexA = random.randint(0, self.genSize - 1)
        indexB = random.randint(0, self.genSize - 1)

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

        indexA = random.randint(0, self.genSize - 2)
        # need to ensure that the end index of the mutation range is greater than the start one
        indexB = random.randint(indexA + 1, self.genSize - 1)
        toBeShuffled = ind.genes[indexA:indexB]

        random.shuffle(toBeShuffled)
        ind.genes[indexA:indexB] = toBeShuffled

        # print('scramble mutation. ind genes {0}'.format(ind.genes))
        ind.computeFitness()
        self.updateBest(ind)

    def crossover(self, indA, indB):
        """
        Executes a 1 order crossover and returns a new individual
        """
        child = []
        tmp = {}

        indexA = random.randint(0, self.genSize - 1)
        indexB = random.randint(0, self.genSize - 1)

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

    def updateMatingPool(self):
        """
        Updating the mating pool before creating a new generation
        """
        self.matingPool = []
        for ind_i in self.population:
            self.matingPool.append(ind_i.copy())

    def newGeneration(self):
        """
        Creating a new generation by applying the following operations, in order:
        1. Selection
        2. Crossover
        3. Mutation
        """
        for i in range(0, len(self.population)):
            """
            Depending menu choice of preset configurations, set up the experiment with appropriate:
            1. Candidate selection method
            2. Crossover method
            3. Mutation method
            """

            # select appropriate candidates
            [ind1, ind2] = self.applySelection(BasicTSP.menuChoice)

            # apply crossover mechanism
            child = self.applyCrossover(BasicTSP.menuChoice, ind1, ind2)

            self.population[i].setGene(child)

            # apply mutation
            self.applyMutation(BasicTSP.menuChoice, self.population[i])

    def applySelection(self, menuChoice):
        """
        Based on configuration choice indicated in menu, select 2 individuals for future operations
        :param menuChoice: number indicating which of the preset configurations was selected
        :return: 2 selected individuals
        """
        inds = None
        if menuChoice == 1 or menuChoice == 2:
            inds = self.randomSelection()
        elif menuChoice == 3 or menuChoice == 4 or menuChoice == 5:
            inds = self.rouletteWheel()
        else:
            inds = self.getFitnessRank()  # TODO need to get the best and 2nd best candidate selection
        return [inds[0], inds[1]]

    def applyCrossover(self, menuChoice, ind1, ind2):
        """
        Applies the appropriate crossover operator according to menu selection
        :param menuChoice: number indicating which of the preset configurations was selected
        :param ind1: parent to be crossed over
        :param ind2: parent to be crossed over
        :return: child individual after applied crossover operator
        """
        child = None
        if menuChoice == 1 or menuChoice == 3 or menuChoice == 6:
            child = self.uniformCrossover(ind1, ind2)
        else:
            child = self.cycleCrossover(ind1, ind2)
        return child

    def applyMutation(self, menuChoice, individual):
        """
        Applies the appropriate mutation according to menu selection
        :param menuChoice: number indicating which of the preset configurations was selected
        :param individual: individual to be mutated
        """
        if menuChoice == 1 or menuChoice == 3 or menuChoice == 4:
            self.reciprocalExchangeMutation(individual)
        else:
            self.scrambleMutation(individual)

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

        print("Total iterations: ", self.iteration)
        print("Best Solution: ", self.best.getFitness())


def menu():
    initialSolution = 'Random'
    uCrossover = 'Uniform Crossover'
    cCrossover = 'Cycle Crossover'
    recMutation = 'Reciprocal Exchange'
    scrambleMutation = 'Scramble Mutation'
    randSel = 'Random Selection'
    rouletteSel = 'Roulette Wheel'
    bestAndSecondBest = 'Best and second best candidates'

    item1 = '1 -> Initial Solution: {0};\t Crossover: {1};\t Mutation: {2};\t Selection: {3}'.format(initialSolution,
                                                                                                     uCrossover,
                                                                                                     recMutation,
                                                                                                     randSel)
    item2 = '2 -> Initial Solution: {0};\t Crossover: {1};\t Mutation: {2};\t Selection: {3}'.format(initialSolution,
                                                                                                     cCrossover,
                                                                                                     scrambleMutation,
                                                                                                     randSel)
    item3 = '3 -> Initial Solution: {0};\t Crossover: {1};\t Mutation: {2};\t Selection: {3}'.format(initialSolution,
                                                                                                     uCrossover,
                                                                                                     recMutation,
                                                                                                     rouletteSel)
    item4 = '4 -> Initial Solution: {0};\t Crossover: {1};\t Mutation: {2};\t Selection: {3}'.format(initialSolution,
                                                                                                     cCrossover,
                                                                                                     recMutation,
                                                                                                     rouletteSel)
    item5 = '5 -> Initial Solution: {0};\t Crossover: {1};\t Mutation: {2};\t Selection: {3}'.format(initialSolution,
                                                                                                     cCrossover,
                                                                                                     scrambleMutation,
                                                                                                     rouletteSel)
    item6 = '6 -> Initial Solution: {0};\t Crossover: {1};\t Mutation: {2};\t Selection: {3}'.format(initialSolution,
                                                                                                     uCrossover,
                                                                                                     scrambleMutation,
                                                                                                     bestAndSecondBest)
    menuItems = ['Please select from preset configurations [1-6]:\n', item1, item2, item3, item4, item5, item6]

    for i in range(0, len(menuItems)):
        print(menuItems[i])
    BasicTSP.menuChoice = int(input("Configuration to be run: "))

    if BasicTSP.menuChoice < 1 or BasicTSP.menuChoice > 6:
        print('Invalid menu selection. Please select a valid configuration number between 1 and 6')
        menu()
    return BasicTSP.menuChoice


menuChoice = 0

if len(sys.argv) < 2:
    print("Error - Incorrect input")
    print("Expecting python BasicTSP.py [instance] ")
    sys.exit(0)

if __name__ == '__main__':
    menu()

    problem_file = sys.argv[1]
    ga = BasicTSP(sys.argv[1], 100, 0.1, 300)
    ga.search()
