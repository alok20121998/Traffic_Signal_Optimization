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
        newPopulation1 = [bestIndividual.copy() for i in range(self.crossroads)]
        newPopulation2 = [bestIndividual.copy() for i in range(self.crossroads)]
        for i in range(self.crossroads):
            if newPopulation1[i][i]+incrementSize<=self.maxLim:
                newPopulation1[i][i]+=incrementSize
            else:
                newPopulation1[i][i] = self.maxLim
            if newPopulation2[i][i]-incrementSize>=self.minLim:
                newPopulation2[i][i]-=incrementSize
            else:
                newPopulation2[i][i] = self.minLim
        fitnessesUp = self.fitnessFunction(newPopulation1)
        fitnessesDown = self.fitnessFunction(newPopulation2)
        descented = bestIndividual
        fitnesses = fitnessesUp+fitnessesDown
        print(fitnesses)
        sortedFitnesses = fitnesses.copy()
        sortedFitnesses.sort()
        b = bestFitness
        for i in range(self.n_steps):
            nxt = fitnesses.index((sortedFitnesses[i][0], ))
            if nxt<self.crossroads:
                temp = descented[nxt]
                descented[nxt]+=incrementSize
                if descented[nxt]>self.maxLim:
                    descented[nxt] = self.maxLim
                f = self.fitnessFunction([descented])
                if f[0][0]>=b:
                    print("failed")
                    print(b, f[0][0], i)
                    descented[nxt] = temp
                else:
                    print(b, f, i)
                    b = f[0][0]
            elif nxt>=self.crossroads:
                temp = descented[nxt-self.crossroads]
                descented[nxt-self.crossroads]-=incrementSize
                if descented[nxt-self.crossroads]<self.minLim:
                    descented[nxt-self.crossroads] = self.minLim
                f = self.fitnessFunction([descented])
                if f[0][0]>=b:
                    print("failed")
                    print(b, f[0][0], i)
                    descented[nxt-self.crossroads] = temp
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
        individual = [-43, -36, 16, -6, 48, 5, -14, -60, -42, 36, 57, -58, 4, 26, 32, -35, 26, -22, 47, 3, 33, 18, 15, 33, -37, 60, -8, -13, -19, 39, -40, 14, 33, -53, 26, -60, 35]
        bestFitness = 121534
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
