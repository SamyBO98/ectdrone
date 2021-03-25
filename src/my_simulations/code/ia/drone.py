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
        self.indexBoardToReach = []


    ##################################################################################
    #######################              GETTERS               #######################

    def getCoordinates(self):
        return self.coordinates

    def getNbCases(self):
        return self.nbCases

    def getCasesReach(self):
        return self.casesReached

    def getCoordinatesToReach(self):
        return self.coordinatesToReach

    def getIndexBoardToReach(self):
        return self.indexBoardToReach


    ##################################################################################
    #######################              SETTERS               #######################

    def setCoordinates(self, coordinates):
        self.coordinates = coordinates

    def setNbCases(self, nbCases):
        self.nbCases = nbCases


    ##################################################################################
    #######################       CLASS STRING FOR DEBUG       #######################

    def toString(self):
        resCoordinates = ""
        resIndex = ""
        for i in range(len(self.coordinatesToReach)):
            resCoordinates = resCoordinates, i, self.coordinatesToReach[i].toString()
            resIndex = resIndex, i, self.indexBoardToReach[i]
        return 'Cases affected:', self.nbCases,"- coordinates:", resCoordinates, "- indexes:", resIndex 

    def coordinatesString(self, i):
        return self.coordinatesToReach[i].toString()

    def indexString(self, i):
        return self.indexBoardToReach[i]


    ##################################################################################
    #######################             FUNCTIONS              #######################

    def addCaseReached(self):
        self.casesReached = self.casesReached + 1

    def isReached(self):
        return self.nbCases == self.casesReached

    def addCoordinatesToReach(self, coordinates):
        self.coordinatesToReach.append(coordinates)

    def sizeCoordinatesToReach(self):
        return len(self.coordinatesToReach)

    def getLastCoordinateReached(self):
        return self.coordinatesToReach[-1]

    def updateLastCoordinateReached(self, coordinates):
        self.coordinatesToReach[-1] = coordinates

    def addIndexToReach(self, index):
        self.indexBoardToReach.append(index)

    def sizeIndexToReach(self):
        return len(self.indexBoardToReach)

    def getLastIndexReached(self):
        return self.indexBoardToReach[-1]

    def updateLastIndexReached(self, index):
        self.indexBoardToReach[-1] = index