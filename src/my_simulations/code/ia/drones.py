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
            self.drones[i].toString()


    ##################################################################################
    #######################             FUNCTIONS              #######################

    def addDrone(self, drone):
        self.drones.append(drone)
        self.nbDrones = self.nbDrones + 1