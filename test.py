import os, sys
tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
sys.path.append(tools)
import traci
import time
import math
from joblib import Parallel, delayed

def setState():
    getFitness1(population)

def getFitness1(population, intervalSize, saveState = False):
    self.fitnesses = [(0,)]*population.shape[0]
    for i in range(population.shape[0]):
        fitnesses[i] = evaluate(population[i], intervalSize, saveState)
    return fitnesses

def requestMany(population):
    fitnesses = (Parallel(n_jobs=4)(delayed(evaluate)(population[i], 360, False, 120, i) for i in range(len(population))))
    for fitness in fitnesses:
        print(fitness)

def evaluate(genotype, intervalSize, saveState, phaseSum, index):
    print(len(genotype))
    sumoBinary = "C:/Program Files (x86)/Eclipse/Sumo/bin/sumo-gui"
    if saveState and os.path.isfile("save"):
        sumoCmd = [sumoBinary, "--net-file", "test.net.xml", "--route-files", "test.rou.xml", "--load-state", "save", "--save-state.times", str(intervalSize), "--save-state.files", "save", "--begin", "0", "--waiting-time-memory", "99999", "--end", str(intervalSize)]
    elif saveState and not os.path.isfile("save"):
        sumoCmd = [sumoBinary, "--net-file", "test.net.xml", "--route-files", "test.rou.xml", "--save-state.times", str(intervalSize), "--save-state.files", "save", "--begin", "0", "--waiting-time-memory", "99999", "--end", str(intervalSize)]
    elif not saveState and os.path.isfile("save"):
        sumoCmd = [sumoBinary, "--net-file", "test.net.xml", "--route-files", "test.rou.xml", "--load-state", "save", "--begin", "0", "--waiting-time-memory", "99999", "--end", str(intervalSize)]
    elif not saveState and not os.path.isfile("save"):
        sumoCmd = [sumoBinary, "--net-file", "test.net.xml", "--route-files", "test.rou.xml", "--begin", "0", "--waiting-time-memory", "99999", "--end", str(intervalSize)]
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
                    timings[light].append((phaseSum+(genotype[0]))//2)
                    flag = False
                elif phases[i].duration>0.9*maxDuration and not flag:
                    timings[light].append(math.ceil((phaseSum-(genotype[0]))/2))
                else:
                    timings[light].append(phases[i].duration)
            del genotype[0]
    for light in timings:
        connection.trafficlight.setPhaseDuration(light, timings[light][connection.trafficlight.getPhase(light)])
    while step < intervalSize+1:
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
    print(len(genotype))
    del genotype
    return (sum(accumulatedWaitingTimes.values()), ), index
##requestMany([[-2, -23, -52, -5, 41, -35, 3, 13, -24, -1, 60, 5, -55, 45, -28, -22, 21, -7, -8, -21, -50, -10, 8, 4, 16, -26, -7], [9, -21, -54, 45, 26, -18, -54, -57, -30, 39, 21, -38, -10, 53, 57, -26, -9, -10, -20, -20, -29, 40, -48, 50, 41, 17, 20], [40, -41, 19, -52, -32, -2, -15, 18, 47, -24, -38, -43, 9, -11, 45, 1, -26, 57, 5, 51, 35, -23, 11, 52, 14, 34, 32], [-36, -11, 1, -49, -14, 3, 0, -24, -29, 11, -52, 55, 24, 14, -11, -12, 49, -54, 49, 12, 12, 53, 14, 55, 10, 56, 35]])
a = [-39, 25, -8, -4, 3, -34, 61, 69, -40, -39, 61, -47, 93, -42, 57, 66, 57, 33, -1, -66, -30, -53, -34, -4, 46, 25, 37, 53, -102, -39, -117, 61, 20, 96, 94, 20, 66]
print(evaluate(a, 240, True, 120, 0))
