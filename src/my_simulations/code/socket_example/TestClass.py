#!/usr/bin/python
from math import *
class TestClass:

    ##################################################################################
    #######################   EXPLANATIONS ABOUT THIS CLASS    #######################

    ## Here are explanations


    ##################################################################################
    #######################         CLASS CONSTRUCTOR          #######################

    def __init__(self, x, y):
        self.x = x + 0.0
        self.y = y + 0.0


    ##################################################################################
    #######################              GETTERS               #######################

    # Get X coordinates (float)
    def getX(self):
        return self.x
    
    # Get Y coordinates (float)
    def getY(self):
        return self.y


    ##################################################################################
    #######################              SETTERS               #######################

    # Set Y coordinates (float)
    def setX(self, x):
        self.x = x + 0.0

    # Set X coordinates (float)
    def setY(self, y):
        self.y = y + 0.0


    ##################################################################################
    #######################       CLASS STRING FOR DEBUG       #######################

    def toString(self):
        return 'Coordinates:', [self.x, self.y]


    ##################################################################################
    #######################             FUNCTIONS              #######################

    def getVector(self, coordinates):
        return sqrt((coordinates.getX() - self.x)**2 + (coordinates.getY() - self.y)**2)

    def isReached(self, coordinates):
        return self.getVector(coordinates) < 0.00001
        #return coordinates.getX() <= self.x + 0.00001 and coordinates.getX() >= self.x - 0.00001 and coordinates.getY() <= self.y + 0.00001 and coordinates.getY() <= self.y + 0.00001