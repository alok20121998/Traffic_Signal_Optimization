from joblib import Parallel, delayed
import time
import numpy as np
import time
import random
import os, sys
tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
sys.path.append(tools)
import traci
import math

class Simulator:
    def __init__(self, intervalSize, phaseSum):
        self.intervalSize = intervalSize
        self.phaseSum = phaseSum
        self.jobs = 4
        self.fitnesses = None
        self.population = None
        self.saveState = None
        self.timings = np.ndarray((4, 954))

    def clear(self):
        if os.path.exists("save"):
            os.remove("save")

    def setState(self, individual):
        self.getFitness1(np.array([individual]), True)

    def requestMany(self, population, saveState):
        fitnesses_list = list([(0,)]*population.shape[0])
        fitnesses = (Parallel(n_jobs=self.jobs)(delayed(self.evaluate)(population[i], saveState, i) for i in range(len(population))))
        for fitness in fitnesses:
            fitnesses_list[fitness[1]] = fitness[0]
        return fitnesses_list

    def getFitness1(self, population, saveState = False):
        fitnesses = self.requestMany(np.array(population), saveState)
        return fitnesses

    def evaluate(self, genotype, saveState, index):
        genotype = genotype.tolist()
        sumoBinary = "C:/Program Files (x86)/Eclipse/Sumo/bin/sumo"
        if saveState and os.path.isfile("save"):
            sumoCmd = [sumoBinary, "--net-file", "test.net.xml", "--route-files", "test.rou.xml", "--load-state", "save", "--save-state.times", str(self.intervalSize), "--save-state.files", "save", "--begin", "0", "--waiting-time-memory", "99999", "--end", str(self.intervalSize)]
        elif saveState and not os.path.isfile("save"):
            sumoCmd = [sumoBinary, "--net-file", "test.net.xml", "--route-files", "test.rou.xml", "--save-state.times", str(self.intervalSize), "--save-state.files", "save", "--begin", "0", "--waiting-time-memory", "99999", "--end", str(self.intervalSize)]
        elif not saveState and os.path.isfile("save"):
            sumoCmd = [sumoBinary, "--net-file", "test.net.xml", "--route-files", "test.rou.xml", "--load-state", "save", "--begin", "0", "--waiting-time-memory", "99999", "--end", str(self.intervalSize)]
        elif not saveState and not os.path.isfile("save"):
            sumoCmd = [sumoBinary, "--net-file", "test.net.xml", "--route-files", "test.rou.xml", "--begin", "0", "--waiting-time-memory", "99999", "--end", str(self.intervalSize)]
        traci.start(sumoCmd, label = "sim_"+str(index))
        connection = traci.getConnection("sim_"+str(index))
        step = 0
        accumulatedWaitingTimes = dict()
        timings = dict()
        tls = connection.trafficlight.getIDList()
        for light in tls:
            phases = connection.trafficlight.getCompleteRedYellowGreenDefinition(light)[0].phases
            if len(phases)>=4:
                timings[light] = []
                for i in range(len(phases)):
                    maxDuration = max([phase.duration for phase in phases])
                    flag = True
                    if phases[i].duration>0.9*maxDuration and flag:
                        timings[light].append((self.phaseSum+(genotype[0]))//2)
                        flag = False
                    elif phases[i].duration>0.9*maxDuration and not flag:
                        timings[light].append(math.ceil((self.phaseSum-(genotype[0]))/2))
                    else:
                        timings[light].append(phases[i].duration)
                del genotype[0]
        for light in timings:
            connection.trafficlight.setPhaseDuration(light, timings[light][connection.trafficlight.getPhase(light)])
        while step < self.intervalSize+1:
            tls = connection.trafficlight.getIDList()
            for light in timings:
                intendedDuration = timings[light]
                currentPhase = connection.trafficlight.getPhase(light)
                remainingTime = connection.trafficlight.getNextSwitch(light)-connection.simulation.getTime()
                if remainingTime==0:
                    connection.trafficlight.setPhase(light, (int(currentPhase)+1)%len(connection.trafficlight.getCompleteRedYellowGreenDefinition(light)[0].phases))
                    connection.trafficlight.setPhaseDuration(light, intendedDuration[connection.trafficlight.getPhase(light)])
            connection.simulationStep()
            
            cars = connection.vehicle.getIDList()
            for car in cars:
                accumulatedWaitingTimes[int(car)] = connection.vehicle.getAccumulatedWaitingTime(car)
            step += 1
        traci.close()
        del genotype
        return (sum(accumulatedWaitingTimes.values()), ), index

##a = Simulator(360, 120)
##a.getFitness1(np.array([[-2, -23, -52, -5, 41, -35, 3, 13, -24, -1, 60, 5, -55, 45, -28, -22, 21, -7, -8, -21, -50, -10, 8, 4, 16, -26, -7], [9, -21, -54, 45, 26, -18, -54, -57, -30, 39, 21, -38, -10, 53, 57, -26, -9, -10, -20, -20, -29, 40, -48, 50, 41, 17, 20], [40, -41, 19, -52, -32, -2, -15, 18, 47, -24, -38, -43, 9, -11, 45, 1, -26, 57, 5, 51, 35, -23, 11, 52, 14, 34, 32], [-36, -11, 1, -49, -14, 3, 0, -24, -29, 11, -52, 55, 24, 14, -11, -12, 49, -54, 49, 12, 12, 53, 14, 55, 10, 56, 35]]))
