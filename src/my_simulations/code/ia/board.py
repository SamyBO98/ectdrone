#!/usr/bin/python
import math
import case as Case
import coordinates as Coordinates
import movement as EnumMovement
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

    # give first coordinates for each drone
    def firstCoordinatesForEachDrone(self, drones):
        for i in range(drones.getNbDrones()):
            bestCoordinates = [0, 0]
            bestVector = drones.getDrone(i).getCoordinates().getVector(self.board[0][0].getCenter())
            for x in range(self.lines):
                for y in range(self.columns):
                    vector = drones.getDrone(i).getCoordinates().getVector(self.board[x][y].getCenter())
                    #print("Drone", i, "- vector:", vector, "- best:", bestVector)
                    if (vector < bestVector) and (self.board[x][y].getIdDrone() == -1):
                        bestVector = vector
                        bestCoordinates = [x, y]
            # we supposed that the drone have his best coordinates
            #print("[FINAL] Drone", i, "- best:", bestVector, "- coordinates:", bestCoordinates)
            #print(self.board[bestCoordinates[0]][bestCoordinates[1]].getCenter().toString())
            drones.getDrone(i).addCoordinatesToReach(self.board[bestCoordinates[0]][bestCoordinates[1]].getCenter())
            drones.getDrone(i).addIndexToReach([bestCoordinates[0], bestCoordinates[1]])
            drones.getDrone(i).addCaseReached()
            self.board[bestCoordinates[0]][bestCoordinates[1]].setIdDrone(i)

    # says if it's possible to move on a way: if yes, edit it
    def moveDroneOnANotherWayIfPossible(self, indexDrone, idDrone, drone, nbMovement, movement, basicMovement):
        if movement == EnumMovement.Movement.LEFT:
            if self.columns > 0 and self.board[indexDrone[0]][indexDrone[1] - 1].getIdDrone() == -1:
                self.board[indexDrone[0]][indexDrone[1] - 1].setIdDrone(idDrone)
                drone.addCaseReached()
                if movement != basicMovement:
                    nbMovement = nbMovement + 1
                    drone.addCoordinatesToReach(self.board[indexDrone[0]][indexDrone[1] - 1].getCenter())
                    drone.addIndexToReach([indexDrone[0], indexDrone[1] - 1])
                else:
                    drone.updateLastCoordinateReached(self.board[indexDrone[0]][indexDrone[1] - 1].getCenter())
                    drone.updateLastIndexReached([indexDrone[0], indexDrone[1] - 1])
                return True

        elif movement == EnumMovement.Movement.RIGHT:
            if self.columns > indexDrone[1] and self.board[indexDrone[0]][indexDrone[1] + 1].getIdDrone() == -1:
                self.board[indexDrone[0]][indexDrone[1] + 1].setIdDrone(idDrone)
                drone.addCaseReached()
                if movement != basicMovement:
                    nbMovement = nbMovement + 1
                    drone.addCoordinatesToReach(self.board[indexDrone[0]][indexDrone[1] + 1].getCenter())
                    drone.addIndexToReach([indexDrone[0], indexDrone[1] + 1])
                else:
                    drone.updateLastCoordinateReached(self.board[indexDrone[0]][indexDrone[1] + 1].getCenter())
                    drone.updateLastIndexReached([indexDrone[0], indexDrone[1] + 1])
                return True

        elif movement == EnumMovement.Movement.UP:
            if self.lines > 0 and self.board[indexDrone[0] - 1][indexDrone[1]].getIdDrone() == -1:
                self.board[indexDrone[0] - 1][indexDrone[1]].setIdDrone(idDrone)
                drone.addCaseReached()
                if movement != basicMovement:
                    nbMovement = nbMovement + 1
                    drone.addCoordinatesToReach(self.board[indexDrone[0] - 1][indexDrone[1]].getCenter())
                    drone.addIndexToReach([indexDrone[0] - 1, indexDrone[1]])
                else:
                    drone.updateLastCoordinateReached(self.board[indexDrone[0] - 1][indexDrone[1]].getCenter())
                    drone.updateLastIndexReached([indexDrone[0] - 1, indexDrone[1]])
                return True

        elif movement == EnumMovement.Movement.DOWN:
            if self.lines > indexDrone[0] and self.board[indexDrone[0] + 1][indexDrone[1]].getIdDrone() == -1:
                self.board[indexDrone[0] + 1][indexDrone[1]].setIdDrone(idDrone)
                drone.addCaseReached()
                if movement != basicMovement:
                    nbMovement = nbMovement + 1
                    drone.addCoordinatesToReach(self.board[indexDrone[0] + 1][indexDrone[1]].getCenter())
                    drone.addIndexToReach([indexDrone[0] + 1, indexDrone[1]])
                else:
                    drone.updateLastCoordinateReached(self.board[indexDrone[0] + 1][indexDrone[1]].getCenter())
                    drone.updateLastIndexReached([indexDrone[0] + 1, indexDrone[1]])
                return True
        return False





