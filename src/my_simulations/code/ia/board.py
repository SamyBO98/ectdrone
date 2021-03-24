#!/usr/bin/python
import math
import case as Case
import coordinates as Coordinates
class Board:

    ##################################################################################
    #######################   EXPLANATIONS ABOUT THIS CLASS    #######################

    ## Here are explanations


    ##################################################################################
    #######################         CLASS CONSTRUCTOR          #######################

    def __init__(self, captureZone, droneZone):
        self.captureZone = captureZone
        self.droneZone = droneZone
        self.lines = int(math.ceil(self.captureZone.getWidth() / self.droneZone.getWidth()))
        self.columns = int(math.ceil(self.captureZone.getHeight() / self.droneZone.getHeight()))

        self.board = [[0 for x in range(self.columns)] for y in range(self.lines)]
        for x in range(self.lines):
            for y in range(self.columns):
                coX = (x * droneZone.getHeight()) + (droneZone.getHeight() / 2)
                coY = (y * droneZone.getWidth()) + (droneZone.getWidth() / 2)
                coordinate = Coordinates.Coordinates(coX, coY)
                self.board[x][y] = Case.Case(coordinate, droneZone)
        

    ##################################################################################
    #######################              GETTERS               #######################

    # Get Capture Zone (Zone class)
    def getCaptureZone(self):
        return self.captureZone

    # Get Capture Zone (Zone class)
    def getDroneZone(self):
        return self.droneZone

    # Get Capture Zone (int)
    def getLines(self):
        return self.lines

    # Get Capture Zone (int)
    def getColumns(self):
        return self.columns

    # Get Capture Zone (2D Array of Case Class)
    def getBoard(self):
        return self.board


    ##################################################################################
    #######################              SETTERS               #######################

    # Set Capture Zone (Zone class)
    def getCaptureZone(self, captureZone):
        self.captureZone = captureZone

    # Set Capture Zone (Zone class)
    def getDroneZone(self, droneZone):
        self.droneZone = droneZone

    # Set Capture Zone (int)
    def getLines(self, lines):
        self.lines = lines

    # Set Capture Zone (int)
    def getColumns(self, columns):
        self.columns = columns

    # Set Capture Zone (2D Array of Case Class)
    def getBoard(self, board):
        self.board = board


    ##################################################################################
    #######################       CLASS STRING FOR DEBUG       #######################

    def toString(self):
        for x in range(self.lines):
            for y in range(self.columns):
                print('Case', [x, y], self.board[x][y].toString())

    def idString(self):
        for x in range(self.lines):
            line = ""
            for y in range(self.columns):
                line = line + self.board[x][y].idString() + " "
            print(line)


    ##################################################################################
    #######################             FUNCTIONS              #######################

    # give number of cases for each drone
    def shareCasesForEachDrone(self, drones):
        nbCases = self.lines * self.columns
        casesForEachDrone = nbCases / drones.getNbDrones()
        for i in range(drones.getNbDrones()):
            drones.getDrone(i).setNbCases(casesForEachDrone)

        for i in range(nbCases % drones.getNbDrones()):
            drones.getDrone(i).setNbCases(drones.getDrone(i).getNbCases() + 1)


