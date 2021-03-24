#!/usr/bin/python
class Drone:

    ##################################################################################
    #######################   EXPLANATIONS ABOUT THIS CLASS    #######################

    ## Here are explanations


    ##################################################################################
    #######################         CLASS CONSTRUCTOR          #######################

    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.nbCases = 0
        self.casesReached = 0
        self.coordinatesToReach = []


    ##################################################################################
    #######################              GETTERS               #######################

    def getCoordinates(self):
        return self.coordinates

    def getNbCases(self):
        return self.nbCases

    def getCasesReach(self):
        return self.casesReached

    def coordinatesToReach(self):
        return self.coordinatesToReach


    ##################################################################################
    #######################              SETTERS               #######################

    def setCoordinates(self, coordinates):
        self.coordinates = coordinates

    def setNbCases(self, nbCases):
        self.nbCases = nbCases


    ##################################################################################
    #######################       CLASS STRING FOR DEBUG       #######################

    def toString(self):
        print("Number of cases: ", self.nbCases)


    ##################################################################################
    #######################             FUNCTIONS              #######################

    def addCaseReached(self):
        self.casesReached = self.casesReached + 1

    def isReached(self):
        return self.nbCases == self.casesReached

    def addCoordinatesToReach(self, coordinates):
        self.coordinatesToReach.append(coordinates)