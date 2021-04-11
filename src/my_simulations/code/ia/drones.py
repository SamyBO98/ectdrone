#!/usr/bin/python
class Drones:

    ##################################################################################
    #######################   EXPLANATIONS ABOUT THIS CLASS    #######################

    ## Here are explanations


    ##################################################################################
    #######################         CLASS CONSTRUCTOR          #######################

    def __init__(self):
        self.drones = []
        self.nbDrones = 0


    ##################################################################################
    #######################              GETTERS               #######################

    def getDrones(self):
        return self.drones

    def getDrone(self, i):
        return self.drones[i]

    def getNbDrones(self):
        return self.nbDrones


    ##################################################################################
    #######################              SETTERS               #######################

    #


    ##################################################################################
    #######################       CLASS STRING FOR DEBUG       #######################

    def toString(self):
        for i in range(self.nbDrones):
            print(self.drones[i].toString())

    def coordinatesString(self):
        for i in range(self.nbDrones):
            print("Drone", i, ": ", self.drones[i].coordinatesString(0))

    def indexString(self):
        for i in range(self.nbDrones):
            print("Drone", i, ": ", self.drones[i].indexString(0))


    ##################################################################################
    #######################             FUNCTIONS              #######################

    def addDrone(self, drone):
        self.drones.append(drone)
        self.nbDrones = self.nbDrones + 1

    def haveTheirWays(self):
        for i in range(self.nbDrones):
            #print(self.drones[i].getNbCases(), "versus", self.drones[i].getCasesReach())
            if (self.drones[i].getNbCases() != self.drones[i].getCasesReach()):
                #print("Drone", i)
                return i
        return -1

    def isLastMove(self, index):
        return self.drones[index].getCasesReach() == self.drones[index].getNbCases() - 1