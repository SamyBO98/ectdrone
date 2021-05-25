#!/usr/bin/python
# coding: utf8
import math
import case as Case
import coordinates as Coordinates
import movement as EnumMovement
import decimal
class Board:
    '''
    @summary: Tableau de cases représentant la zone à explorer découpée selon la zone que les caméras peuvent capturer
    '''

    ##################################################################################
    #######################         CLASS CONSTRUCTOR          #######################

    def __init__(self, coordinate1, coordinate2, droneZone):
        '''
        @summary: Création d'un tableau de cases représentant la zone à explorer basé sur 2 coordonnées formant un rectangle et d'une zone de capture des drones
        @param coordinate1: Coordonnée représentant un coin de la zone à explorer
        @type coordinate1: <Class> Coordinates
        @param coordinate2: Coordonnée représentant un coin opposé de la première coordonnée donnée
        @type coordinate2: <Class> Coordinates
        @param droneZone: Zone que les caméras des drones peuvent capturer (enregistrer)
        @type droneZone: <Class> Zone
        '''
        self.droneZone = droneZone
        width = abs(coordinate1.getX() - coordinate2.getX())
        height = abs(coordinate1.getY() - coordinate2.getY())
        self.lines = int(math.ceil(width / self.droneZone.getWidth()))
        self.columns = int(math.ceil(height / self.droneZone.getHeight()))

        self.board = [[0 for x in range(self.columns)] for y in range(self.lines)]
        for x in range(self.lines):
            for y in range(self.columns):
                if (coordinate1.getX() > coordinate2.getX()):
                    coX = coordinate1.getX() - (x * droneZone.getHeight()) - (droneZone.getHeight() / 2)
                else:
                    coX = coordinate1.getX() + (x * droneZone.getHeight()) + (droneZone.getHeight() / 2)

                if (coordinate1.getY() > coordinate2.getY()):
                    coY = coordinate1.getY() - (y * droneZone.getWidth()) - (droneZone.getWidth() / 2)
                else:
                    coY = coordinate1.getY() + (y * droneZone.getWidth()) + (droneZone.getWidth() / 2)

                coordinate = Coordinates.Coordinates(coX, coY)
                self.board[x][y] = Case.Case(coordinate, droneZone)
        

    ##################################################################################
    #######################              GETTERS               #######################

    def getDroneZone(self):
        '''
        @summary: Retourne la zone à explorer
        @return: <Class> Zone
        '''
        return self.droneZone

    def getLines(self):
        '''
        @summary: Retourne le nombre de lignes du tableau de cases
        @return: int
        '''
        return self.lines

    def getColumns(self):
        '''
        @summary: Retourne le nombre de colonnes du tableau de cases
        @return: int
        '''
        return self.columns

    def getBoard(self):
        '''
        @summary: Retourne le tableau de cases
        @return: [array 2D] <Class> Case
        '''
        return self.board


    ##################################################################################
    #######################       CLASS STRING FOR DEBUG       #######################

    def toString(self):
        '''
        @summary: Fonction retournant les informations globales de la classe
        '''
        for x in range(self.lines):
            for y in range(self.columns):
                print('Case', [x, y], self.board[x][y].toString())

    def idString(self):
        '''
        @summary: Fonction retournant, pour chaque case, l'id du drone qui a visité la zone
        '''
        for x in range(self.lines):
            line = ""
            for y in range(self.columns):
                line = line + self.board[x][y].idString() + " "
            print(line)


    ##################################################################################
    #######################             FUNCTIONS              #######################

    def shareCasesForEachDrone(self, drones):
        '''
        @summary: Répartie, pour chaque drone, le nombre de cases du tableau à explorer
        @param drones: Tableau de drones
        @type drones: <Class> Drones
        '''
        nbCases = self.lines * self.columns
        casesForEachDrone = nbCases / drones.getNbDrones()
        for i in range(drones.getNbDrones()):
            drones.getDrone(i).setNbCases(casesForEachDrone)

        for i in range(nbCases % drones.getNbDrones()):
            drones.getDrone(i).setNbCases(drones.getDrone(i).getNbCases() + 1)

    def firstCoordinatesForEachDrone(self, drones):
        '''
        @summary: Détermine, pour chaque drone, la première case à explorer (point de départ de l'exploration)
        @param drones: Tableau de drones
        @type drones: <Class> Drones
        '''
        for i in range(drones.getNbDrones()):
            bestCoordinates = [0, 0]
            bestVector = drones.getDrone(i).getCoordinates().getVector(self.board[0][0].getCenter())
            for x in range(self.lines):
                for y in range(self.columns):
                    vector = drones.getDrone(i).getCoordinates().getVector(self.board[x][y].getCenter())
                    if (vector < bestVector) and (self.board[x][y].getIdDrone() == -1):
                        bestVector = vector
                        bestCoordinates = [x, y]

            drones.getDrone(i).addCoordinatesToReach(self.board[bestCoordinates[0]][bestCoordinates[1]].getCenter())
            drones.getDrone(i).addIndexToReach([bestCoordinates[0], bestCoordinates[1]])
            drones.getDrone(i).addCaseReached()

            self.board[bestCoordinates[0]][bestCoordinates[1]].setIdDrone(i)

    def getCoordinatesForNextMove(self, drone, movement):
        '''
        @summary: Retourne les coordonnées de la prochaine zone à visiter (case voisine)
        @param drone: Drone concerné
        @type drone: <Class> Drone
        @param movement: Prochaine direction
        @type movement: <Class Enum> Movement
        @return 
        '''
        # left
        if movement == EnumMovement.Movement.LEFT:
            x = drone.getLastIndexReached()[0] - 1
            y = drone.getLastIndexReached()[1]
        # right
        elif movement == EnumMovement.Movement.RIGHT:
            x = drone.getLastIndexReached()[0] + 1
            y = drone.getLastIndexReached()[1]
        # up
        elif movement == EnumMovement.Movement.UP:
            x = drone.getLastIndexReached()[0]
            y = drone.getLastIndexReached()[1] + 1
        # down
        elif movement == EnumMovement.Movement.DOWN:
            x = drone.getLastIndexReached()[0]
            y = drone.getLastIndexReached()[1] - 1
        else:
            return None
        return [x, y]
        
    def possibleToMove(self, drone, movement):
        '''
        @summary: Vérifie s'il est possible pour le drone de se déplacer à une case voisine selon la prochaine direction indiquée
        @param drone: Drone concerné
        @type drone: <Class> Drone
        @param movement: Prochaine direction
        @type movement: <Class Enum> Movement
        @return: bool
        '''
        cos = self.getCoordinatesForNextMove(drone, movement)
        if cos == None:
            return False
        
        x = cos[0]
        y = cos[1]
            
        # check if possible to move on the next case
        # -> next case not visited
        # -> coordinates not out of range
        
        if x < self.lines and y >= 0 and y < self.columns and x >= 0:
            if self.board[x][y].getIdDrone() == -1:
                return True
        return False

    def moveDroneOnBoard(self, drone, movement, lastMovement, indexDrone):
        '''
        @summary: Met à jour la prochaine coordonnée, si possible, du drone selon la direction indiquée
        @param drone: Drone concerné
        @type drone: <Class> Drone
        @param movement: Prochaine direction
        @type movement: <Class Enum> Movement
        @param lastMovement: Dernier mouvement du drone: si la direction change, on ajoute la coordonnée, sinon on modifie la dernière ajoutée
        @type lastMovement: <Class Enum> Movement
        @param indexDrone: id du drone
        @type indexDrone: int
        '''
        cos = self.getCoordinatesForNextMove(drone, movement)
        if cos == None:
            return 
        
        x = cos[0]
        y = cos[1]

        self.board[x][y].setIdDrone(indexDrone)
        # update drone
        # -> increase nb cases reached
        # -> update coordinates and index reached (by compare movement and last movement)
        drone.addCaseReached()
        if movement == lastMovement:
            drone.updateLastCoordinateReached(self.board[x][y].getCenter())
            drone.updateLastIndexReached(cos)
        else:
            drone.addCoordinatesToReach(self.board[x][y].getCenter())
            drone.addIndexToReach(cos)