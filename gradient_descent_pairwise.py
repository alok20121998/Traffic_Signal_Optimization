import array
import random
import numpy
import math
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
import copy

class GA2:
    def __init__(self, params):
        self.crossover = copy.deepcopy(params["crossover"])
        self.mutate = copy.deepcopy(params["mutate"])
        self.select = copy.deepcopy(params["select"])
        self.numGeneration = params["numGeneration2"]
        self.crossroads = params["crossroads"]
        self.minLim = params["minLim"]
        self.maxLim = params["maxLim"]
        self.gdIterations = params["gdIterations"]
        self.incrementSize = params["incrementSize"]
        self.n_steps = params["n_steps"]
        self.numIndividuals = params["numIndividuals2"]
        self.simulator = params["simulator"]
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", array.array, typecode='b', fitness=creator.FitnessMin)

        self.toolbox = base.Toolbox()

        # Attribute generator
        self.toolbox.register("random", random.randint, self.minLim, self.maxLim)

        # Structure initializers
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.random, self.crossroads)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", self.fitnessFunction)
        self.toolbox.register("mate", self.crossover["operator"])
        del self.crossover["operator"]
        self.toolbox.register("mutate", self.mutate["operator"])
        del self.mutate["operator"]
        self.toolbox.register("select", self.select["operator"])
        del self.select["operator"]

    def fitnessFunction(self, population):
        fitnesses = [(3, )]*self.numIndividuals
        signals = numpy.ndarray((len(population), self.crossroads))
        for individual in range(len(population)):
            timings = population[individual]
            signals[individual] = timings
        fitnesses = self.simulator.getFitness1(signals)
        return fitnesses

    def gradientDescent(self, bestIndividual, bestFitness, incrementSize):
        dependencies = [[0, 4], [1, 27], [2, 29], [3, 28], [5, 8], [6, 28], [7, 5], [8, 34], [9, 1], [10, 34], [11, 12], [13, 14], [14, 18], [15, 12], [16, 17], [19, 18], [20, 21], [22, 23], [24, 29], [25, 35], [26, 36], [30, 31], [32, 33]]
        newPopulation1 = [bestIndividual.copy() for i in range(len(dependencies))]
        newPopulation2 = [bestIndividual.copy() for i in range(len(dependencies))]
        for i in range(len(dependencies)):
            if newPopulation1[i][dependencies[i][0]]+incrementSize<=self.maxLim:
                newPopulation1[i][dependencies[i][0]]+=incrementSize
            else:
                newPopulation1[i][dependencies[i][0]] = self.maxLim
            if newPopulation1[i][dependencies[i][1]]-incrementSize>=self.minLim:
                newPopulation1[i][dependencies[i][1]]-=incrementSize
            else:
                newPopulation1[i][dependencies[i][1]] = self.minLim
            if newPopulation2[i][dependencies[i][0]]-incrementSize>=self.minLim:
                newPopulation2[i][dependencies[i][0]]-=incrementSize
            else:
                newPopulation2[i][dependencies[i][0]] = self.minLim
            if newPopulation2[i][dependencies[i][1]]+incrementSize<=self.maxLim:
                newPopulation2[i][dependencies[i][1]]+=incrementSize
            else:
                newPopulation2[i][dependencies[i][1]] = self.maxLim
        fitnessesUp = self.fitnessFunction(newPopulation1)
        fitnessesDown = self.fitnessFunction(newPopulation2)
        descented = bestIndividual
        fitnesses = fitnessesUp+fitnessesDown
        sortedFitnesses = fitnesses.copy()
        sortedFitnesses.sort()
        b = bestFitness
        for i in range(self.n_steps):
            nxt = fitnesses.index((sortedFitnesses[i][0], ))
            if nxt<len(dependencies):
                l1 = descented[dependencies[nxt][0]]
                l2 = descented[dependencies[nxt][1]]
                descented[dependencies[nxt][0]]+=incrementSize
                descented[dependencies[nxt][1]]-=incrementSize
                if descented[dependencies[nxt][0]]>self.maxLim:
                    descented[dependencies[nxt][0]] = self.maxLim
                if descented[dependencies[nxt][1]]<self.minLim:
                    descented[dependencies[nxt][1]] = self.minLim
                f = self.fitnessFunction([descented])
                if f[0][0]>=b:
                    print("failed")
                    print(b, f[0][0], i)
                    descented[dependencies[nxt][0]] = l1
                    descented[dependencies[nxt][1]] = l2
                else:
                    print(b, f, i)
                    b = f[0][0]
            elif nxt>=len(dependencies):
                l1 = descented[dependencies[nxt-len(dependencies)][0]]
                l2 = descented[dependencies[nxt-len(dependencies)][1]]
                descented[dependencies[nxt-len(dependencies)][0]]-=incrementSize
                descented[dependencies[nxt-len(dependencies)][1]]+=incrementSize
                if descented[dependencies[nxt-len(dependencies)][0]]<self.minLim:
                    descented[dependencies[nxt-len(dependencies)][0]] = self.minLim
                if descented[dependencies[nxt-len(dependencies)][1]]>self.maxLim:
                    descented[dependencies[nxt-len(dependencies)][1]] = self.maxLim
                f = self.fitnessFunction([descented])
                if f[0][0]>=b:
                    print("failed")
                    print(b, f[0][0], i)
                    descented[dependencies[nxt-len(dependencies)][0]] = l1
                    descented[dependencies[nxt-len(dependencies)][1]] = l2
                else:
                    print(b, f, i)
                    b = f[0][0]
        return descented, b

    def run(self):
##        pop = self.toolbox.population(n=1)
##        fitnesses = self.fitnessFunction(pop)
##        for ind, fit in zip(pop, fitnesses):
##            print(ind, fit)
##            ind.fitness.values = fit
##
##        bestFitness = min([ind.fitness.values[0] for ind in pop])
##        startingFitness = bestFitness
##        bestIndividual = pop[0]
##        individual = []
##        for i in bestIndividual:
##            individual.append(i)
##        print("Starting point: ")
##        print(bestIndividual)
##        print(startingFitness)
        incrementSize = 30
        individual = [-51, 5, -3, 22, 58, 28, 19, -56, 18, -4, -21, -6, 20, 50, -23, 46, 39, 52, -29, 16, -46, -36, 48, -16, 42, 11, 29, -33, -46, 23, -49, 9, 1, 20, -53, -27, 13]
        bestFitness = 100089
        startingFitness = bestFitness
        for i in range(self.gdIterations):
            individual, bestFitness = self.gradientDescent(individual, bestFitness, int(self.incrementSize/(i+1)))
            print("-"*30)
            print("Gradient Descent %s statistics" % str(i+1))
            print("          Min: %s" % bestFitness)
##            print("  Improvement: %s" % ((worst - bestFitness)*100/worst))
            print(individual)
            print("-"*30)
        
        return bestFitness, None, individual
