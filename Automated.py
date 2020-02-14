from gradient_descent import GA2
from simulator import Simulator
import time
from deap import tools
import math
import copy
import os.path
import pickle
import numpy as np

class Controller:
    def __init__(self, params):
        self.params = params
        self.timeSteps = params["timeSteps"]
        
    def run2(self):
        self.params["simulator"].clear()
        fitness = 0
        for timeStep in range(self.params["timeSteps"]):
            print("Timtestep: " + str(timeStep))
            ga2 = GA2(self.params)
            best, improvement, population = ga2.run()
            print(population)
            fitness+=best
            self.params["simulator"].setState(population)
        print(fitness)
        self.params["simulator"].clear()
        return 0

NUM_INDIVIDUALS = 84
LOW = -60
UP = 60



params = {"crossover": {"operator": tools.cxTwoPoint},
          "mutate": {"operator": tools.mutShuffleIndexes, "indpb": 0.1},
          "select": {"operator": tools.selBest, "k": int(math.sqrt(NUM_INDIVIDUALS//2))},
          "numGeneration1": 1,
          "numGeneration2": 5,
          "cutoff": 3,
          "crossroads": 37,
          "timeSteps": 1,
          "numIndividuals1": 20,
          "numIndividuals2": NUM_INDIVIDUALS,
          "simulator": Simulator(480, 120),
          "fitnessGA1": "1",
          "fitnessGA2": "1",
          "minLim": LOW,
          "maxLim": UP,
          "incrementSize": 30,
          "gdIterations": 2,
          "n_steps": 10}
controller = Controller(params)
print(controller.run2())

params = {"crossover": {"operator": tools.cxTwoPoint},
          "mutate": {"operator": tools.mutShuffleIndexes, "indpb": 0.1},
          "select": {"operator": tools.selBest, "k": int(math.sqrt(NUM_INDIVIDUALS//2))},
          "numGeneration1": 1,
          "numGeneration2": 5,
          "cutoff": 3,
          "crossroads": 37,
          "timeSteps": 1,
          "numIndividuals1": 20,
          "numIndividuals2": NUM_INDIVIDUALS,
          "simulator": Simulator(480, 120),
          "fitnessGA1": "1",
          "fitnessGA2": "1",
          "minLim": LOW,
          "maxLim": UP,
          "incrementSize": 30,
          "gdIterations": 2,
          "n_steps": 10}
controller = Controller(params)
print(controller.run2())

params = {"crossover": {"operator": tools.cxTwoPoint},
          "mutate": {"operator": tools.mutShuffleIndexes, "indpb": 0.1},
          "select": {"operator": tools.selBest, "k": int(math.sqrt(NUM_INDIVIDUALS//2))},
          "numGeneration1": 1,
          "numGeneration2": 5,
          "cutoff": 3,
          "crossroads": 37,
          "timeSteps": 1,
          "numIndividuals1": 20,
          "numIndividuals2": NUM_INDIVIDUALS,
          "simulator": Simulator(480, 120),
          "fitnessGA1": "1",
          "fitnessGA2": "1",
          "minLim": LOW,
          "maxLim": UP,
          "incrementSize": 30,
          "gdIterations": 2,
          "n_steps": 10}
controller = Controller(params)
print(controller.run2())

params = {"crossover": {"operator": tools.cxTwoPoint},
          "mutate": {"operator": tools.mutShuffleIndexes, "indpb": 0.1},
          "select": {"operator": tools.selBest, "k": int(math.sqrt(NUM_INDIVIDUALS//2))},
          "numGeneration1": 1,
          "numGeneration2": 5,
          "cutoff": 3,
          "crossroads": 37,
          "timeSteps": 1,
          "numIndividuals1": 20,
          "numIndividuals2": NUM_INDIVIDUALS,
          "simulator": Simulator(480, 120),
          "fitnessGA1": "1",
          "fitnessGA2": "1",
          "minLim": LOW,
          "maxLim": UP,
          "incrementSize": 30,
          "gdIterations": 2,
          "n_steps": 10}
controller = Controller(params)
print(controller.run2())



params = {"crossover": {"operator": tools.cxTwoPoint},
          "mutate": {"operator": tools.mutShuffleIndexes, "indpb": 0.1},
          "select": {"operator": tools.selBest, "k": int(math.sqrt(NUM_INDIVIDUALS//2))},
          "numGeneration1": 1,
          "numGeneration2": 5,
          "cutoff": 3,
          "crossroads": 37,
          "timeSteps": 1,
          "numIndividuals1": 20,
          "numIndividuals2": NUM_INDIVIDUALS,
          "simulator": Simulator(480, 120),
          "fitnessGA1": "1",
          "fitnessGA2": "1",
          "minLim": LOW,
          "maxLim": UP,
          "incrementSize": 30,
          "gdIterations": 2,
          "n_steps": 10}
controller = Controller(params)
print(controller.run2())

