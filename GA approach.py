from short1 import GA2
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
        self.paramsListGA2 = ["crossover", "mutate", "select", "numGeneration2", "crossroads", "numIndividuals2", "timeStep", "fitnessGA2", "simulator", "densities", "population", "minLim", "maxLim"]
        self.paramsGA2 = dict((k, params[k]) for k in self.paramsListGA2 if k in params)
        
    def run2(self):
        self.params["simulator"].clear()
        fitness = 0
        for timeStep in range(self.params["timeSteps"]):
            print("Timtestep: " + str(timeStep))
            self.paramsGA2["densities"] = None
            self.paramsGA2["population"] = None
            ga2 = GA2(self.paramsGA2)
            best, improvement, population = ga2.run()
            fitness+=best
            self.params["simulator"].setState(population)
            print(fitness)
        self.params["simulator"].clear()
        return 0

NUM_INDIVIDUALS = 100
LOW = -60
UP = 60

params = {"crossover": {"operator": tools.cxOnePoint},
          "mutate": {"operator": tools.mutUniformInt, "indpb": 0.01, "low": LOW, "up": UP},
          "select": {"operator": tools.selBest, "k": int(math.sqrt(NUM_INDIVIDUALS//2))},
          "numGeneration1": 1,
          "numGeneration2": 5,
          "crossroads": 37,
          "timeSteps": 1,
          "numIndividuals1": 300,
          "numIndividuals2": NUM_INDIVIDUALS,
          "simulator": Simulator(240, 120),
          "fitnessGA1": "1",
          "fitnessGA2": "1",
          "minLim": LOW,
          "maxLim": UP}
controller = Controller(params)
print(controller.run2())

params = {"crossover": {"operator": tools.cxOnePoint},
          "mutate": {"operator": tools.mutUniformInt, "indpb": 0.01, "low": LOW, "up": UP},
          "select": {"operator": tools.selBest, "k": int(math.sqrt(NUM_INDIVIDUALS//2))},
          "numGeneration1": 1,
          "numGeneration2": 5,
          "crossroads": 37,
          "timeSteps": 1,
          "numIndividuals1": 300,
          "numIndividuals2": NUM_INDIVIDUALS,
          "simulator": Simulator(480, 120),
          "fitnessGA1": "1",
          "fitnessGA2": "1",
          "minLim": LOW,
          "maxLim": UP}
controller = Controller(params)
print(controller.run2())

params = {"crossover": {"operator": tools.cxOnePoint},
          "mutate": {"operator": tools.mutUniformInt, "indpb": 0.01, "low": LOW, "up": UP},
          "select": {"operator": tools.selBest, "k": int(math.sqrt(NUM_INDIVIDUALS//2))},
          "numGeneration1": 1,
          "numGeneration2": 10,
          "crossroads": 37,
          "timeSteps": 1,
          "numIndividuals1": 300,
          "numIndividuals2": NUM_INDIVIDUALS,
          "simulator": Simulator(480, 120),
          "fitnessGA1": "1",
          "fitnessGA2": "1",
          "minLim": LOW,
          "maxLim": UP}
controller = Controller(params)
print(controller.run2())

params = {"crossover": {"operator": tools.cxOnePoint},
          "mutate": {"operator": tools.mutUniformInt, "indpb": 0.01, "low": LOW, "up": UP},
          "select": {"operator": tools.selBest, "k": int(math.sqrt(NUM_INDIVIDUALS//2))},
          "numGeneration1": 1,
          "numGeneration2": 10,
          "crossroads": 37,
          "timeSteps": 1,
          "numIndividuals1": 300,
          "numIndividuals2": NUM_INDIVIDUALS,
          "simulator": Simulator(480, 120),
          "fitnessGA1": "1",
          "fitnessGA2": "1",
          "minLim": LOW,
          "maxLim": UP}
controller = Controller(params)
print(controller.run2())

params = {"crossover": {"operator": tools.cxOnePoint},
          "mutate": {"operator": tools.mutUniformInt, "indpb": 0.01, "low": LOW, "up": UP},
          "select": {"operator": tools.selBest, "k": int(math.sqrt(NUM_INDIVIDUALS//2))},
          "numGeneration1": 1,
          "numGeneration2": 10,
          "crossroads": 37,
          "timeSteps": 1,
          "numIndividuals1": 300,
          "numIndividuals2": NUM_INDIVIDUALS,
          "simulator": Simulator(480, 120),
          "fitnessGA1": "1",
          "fitnessGA2": "1",
          "minLim": LOW,
          "maxLim": UP}
controller = Controller(params)
print(controller.run2())
