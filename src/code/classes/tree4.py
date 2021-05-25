#!/usr/bin/python
# coding: utf8
import movement as EnumMovement
import copy
from operator import attrgetter, itemgetter
globalFound = [-1]

class QuartenaireTree:
    '''
    @summary: Générateur de chemins basé sur un arbre à 4 fils indiquant à chaque fils une direction possible: NORD, SUD, EST, OUEST
    '''

    ##################################################################################
    #######################         CLASS CONSTRUCTOR          #######################

    def __init__(self, board, drones, movement, nbMovement):
        '''
        @summary: Récupère les informations utiles pour la génération des chemins possibles. le tableau de cases, les drones, la direction actuelle (nulle par défaut) et le nombre de rotations (nulle par défaut)
        @param board: Tableau de cases
        @type board: <Class> Board
        @param drones: Liste de drones
        @type drones: <Class> Drones
        @param movement: Direction actuelle
        @type movement: <Class Enum> Movement
        @param nbMovement: Nombre de rotations
        @type nbMovement: int
        '''
        self.board = board
        self.drones = drones
        self.movement = movement
        self.nbMovement = nbMovement
        # nodes
        self.nodeUp = None
        self.nodeDown = None
        self.nodeLeft = None
        self.nodeRight = None

    def __repr__(self):
        '''
        @summary: Représentation de cette classe
        @return: (<Class> Board, <Class> Drones, nombre de rotations totaux)
        '''
        return repr((self.board, self.drones, self.nbMovement))

    ##################################################################################
    #######################              GETTERS               #######################

    def getBoard(self):
        '''
        @summary: Retourne le tableau de cases
        @return: <Class> Board
        '''
        return self.board

    def getDrones(self):
        '''
        @summary: Retourne la liste de drones
        @return: <Class> Drones
        '''
        return self.drones

    def getMovement(self):
        '''
        @summary: Retourne la direction actuelle
        @return: <Class Enum> Movement
        '''
        return self.movement

    def getNbMovement(self):
        '''
        @summary: Retourne le nombre de rotations totaux
        @return: int
        '''
        return self.nbMovement

    def getNodeUp(self):
        '''
        @summary: Retourne le fils indiquant le NORD
        @return: <Class> QuartenaireTree
        '''
        return self.nodeUp

    def getNodeDown(self):
        '''
        @summary: Retourne le fils indiquant le SUD
        @return: <Class> QuartenaireTree
        '''
        return self.nodeDown

    def getNodeLeft(self):
        '''
        @summary: Retourne le fils indiquant l'EST
        @return: <Class> QuartenaireTree
        '''
        return self.nodeLeft

    def getNodeRight(self):
        '''
        @summary: Retourne le fils indiquant l'OUEST
        @return: <Class> QuartenaireTree
        '''
        return self.nodeRight

    ##################################################################################
    #######################       CLASS STRING FOR DEBUG       #######################

    def toString(self):
        '''
        @summary: Fonction retournant les informations globales de la classe
        '''
        self.board.idString()
        print("Total amount of movements:", self.nbMovement())

    ##################################################################################
    #######################             FUNCTIONS              #######################

    def generateTree(self):
        '''
        @summary: Génère la liste des chemins possibles
        '''
        # check if all drones have their ways (-1 means OK, a number between 0 and number of drones - 1 means NOT OK)
        indexDrone = self.drones.haveTheirWays()
        #print("Generate tree function")
        if (globalFound[0] == -1 or (globalFound[0] != -1 and self.nbMovement < globalFound[0])):
            if (indexDrone != -1):
                # check if it's possible to move on this way
                # if it's possible, compare movements (if same, keep the same number of movements, it will helps later)
                # if it's possible, check if this is the last movement from the drone: if yes, reset movement type
                # LEFT
                #indexDrone = 2
                if self.board.possibleToMove(self.drones.getDrone(indexDrone), EnumMovement.Movement.LEFT):
                    #print("Node left created")
                    localBoard = copy.deepcopy(self.board)
                    #localBoard.idString()
                    localDrones = copy.deepcopy(self.drones)
                    localNbMovement = copy.deepcopy(self.nbMovement)
                    localMovement = copy.deepcopy(self.movement)
                    localCurrentMovement = EnumMovement.Movement.LEFT
                    # update board
                    localBoard.moveDroneOnBoard(localDrones.getDrone(
                        indexDrone), EnumMovement.Movement.LEFT, localMovement, indexDrone)
                    # check if not the same movement: increase number of moves done
                    if localMovement != EnumMovement.Movement.LEFT:
                        #print("NOT SAME MOVEMENT:", localMovement, "<->", localCurrentMovement)
                        localNbMovement = localNbMovement + 1
                    # reset movement if that was last move
                    if localDrones.getDrone(indexDrone).isReached():
                        localCurrentMovement = EnumMovement.Movement.NONE
                    # create node
                    self.nodeLeft = QuartenaireTree(
                        localBoard, localDrones, localCurrentMovement, localNbMovement)
                    #localBoard.idString()
                    #print("NUMBER OF MOVEMENTS:", localNbMovement)
                    self.nodeLeft.generateTree()

                # RIGHT
                if self.board.possibleToMove(self.drones.getDrone(indexDrone), EnumMovement.Movement.RIGHT):
                    #print("Node right created")
                    localBoard = copy.deepcopy(self.board)
                    #localBoard.idString()
                    localDrones = copy.deepcopy(self.drones)
                    localNbMovement = copy.deepcopy(self.nbMovement)
                    localMovement = copy.deepcopy(self.movement)
                    localCurrentMovement = EnumMovement.Movement.RIGHT
                    # update board
                    localBoard.moveDroneOnBoard(localDrones.getDrone(
                        indexDrone), localCurrentMovement, localMovement, indexDrone)
                    # check if same movement: increase number of moves done
                    if localMovement != localCurrentMovement:
                        #print("NOT SAME MOVEMENT:", localMovement, "<->", localCurrentMovement)
                        localNbMovement = localNbMovement + 1
                    # reset movement if that was last move
                    if localDrones.getDrone(indexDrone).isReached():
                        localCurrentMovement = EnumMovement.Movement.NONE
                    # create node
                    self.nodeRight = QuartenaireTree(
                        localBoard, localDrones, localCurrentMovement, localNbMovement)
                    #localBoard.idString()
                    #print("NUMBER OF MOVEMENTS:", localNbMovement)
                    self.nodeRight.generateTree()
                    

                # UP
                if self.board.possibleToMove(self.drones.getDrone(indexDrone), EnumMovement.Movement.UP):
                    #print("Node up created")
                    localBoard = copy.deepcopy(self.board)
                    #localBoard.idString()
                    localDrones = copy.deepcopy(self.drones)
                    localNbMovement = copy.deepcopy(self.nbMovement)
                    localMovement = copy.deepcopy(self.movement)
                    localCurrentMovement = EnumMovement.Movement.UP
                    # update board
                    localBoard.moveDroneOnBoard(localDrones.getDrone(
                        indexDrone), localCurrentMovement, localMovement, indexDrone)
                    # check if same movement: increase number of moves done
                    if localMovement != localCurrentMovement:
                        #print("NOT SAME MOVEMENT:", localMovement, "<->", localCurrentMovement)
                        localNbMovement = localNbMovement + 1
                    # reset movement if that was last move
                    if localDrones.getDrone(indexDrone).isReached():
                        localCurrentMovement = EnumMovement.Movement.NONE
                    # create node
                    self.nodeUp = QuartenaireTree(
                        localBoard, localDrones, localCurrentMovement, localNbMovement)
                    #localBoard.idString()
                    #print("NUMBER OF MOVEMENTS:", localNbMovement)
                    self.nodeUp.generateTree()
                    

                # DOWN
                if self.board.possibleToMove(self.drones.getDrone(indexDrone), EnumMovement.Movement.DOWN):
                    #print("Node down created")
                    localBoard = copy.deepcopy(self.board)
                    #localBoard.idString()
                    localDrones = copy.deepcopy(self.drones)
                    localNbMovement = copy.deepcopy(self.nbMovement)
                    localMovement = copy.deepcopy(self.movement)
                    localCurrentMovement = EnumMovement.Movement.DOWN
                    # update board
                    localBoard.moveDroneOnBoard(localDrones.getDrone(
                        indexDrone), localCurrentMovement, localMovement, indexDrone)
                    # check if same movement: increase number of moves done
                    if localMovement != localCurrentMovement:
                        #print("NOT SAME MOVEMENT:", localMovement, "<->", localCurrentMovement)
                        localNbMovement = localNbMovement + 1
                    # reset movement if that was last move
                    if localDrones.getDrone(indexDrone).isReached():
                        localCurrentMovement = EnumMovement.Movement.NONE
                    # create node
                    self.nodeDown = QuartenaireTree(
                        localBoard, localDrones, localCurrentMovement, localNbMovement)
                    #localBoard.idString()
                    #print("NUMBER OF MOVEMENTS:", localNbMovement)
                    self.nodeDown.generateTree()
                    
            else:
                globalFound[0] = self.nbMovement
                self.board.idString()
                print("NUMBER OF MOVEMENTS:", self.nbMovement)
                print("MEILLEUR CHEMIN:", globalFound[0])

    def getBestWay(self):
        '''
        @summary: Récupère le meilleur chemin selon ces critères: le nombre de rotations totaux le plus faible possible
        '''
        # if -1: means that it's a way: returns it
        if self.drones.haveTheirWays() == -1:
            return (self.board, self.drones, self.nbMovement)
        else:
            # we took the best way for each node
            bestWayLeft = None
            bestWayRight = None
            bestWayUp = None
            bestWayDown = None
            ways = []
            if self.nodeLeft != None:
                bestWayLeft = self.nodeLeft.getBestWay()
                if bestWayLeft != None:
                    ways.append((bestWayLeft[0], bestWayLeft[1], bestWayLeft[2]))
            if self.nodeRight != None:
                bestWayRight = self.nodeRight.getBestWay()
                if bestWayRight != None:
                    ways.append((bestWayRight[0], bestWayRight[1], bestWayRight[2]))
            if self.nodeUp != None:
                bestWayUp = self.nodeUp.getBestWay()
                if bestWayUp != None:
                    ways.append((bestWayUp[0], bestWayUp[1], bestWayUp[2]))
            if self.nodeDown != None:
                bestWayDown = self.nodeDown.getBestWay()
                if bestWayDown != None:
                    ways.append((bestWayDown[0], bestWayDown[1], bestWayDown[2]))

            #print(ways)

            # we affect to bestWay the way with less movements
            if ways == []:
                return None
            else:
                return sorted(ways, key=lambda way: way[2])[0]
