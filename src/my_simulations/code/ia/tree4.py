#!/usr/bin/python
import movement as EnumMovement
import copy

class QuartenaireTree:

    ##################################################################################
    #######################   EXPLANATIONS ABOUT THIS CLASS    #######################

    # Here are explanations
    # Board
    # Nodes (UP, DOWN, LEFT, RIGHT)
    # Drones

    ##################################################################################
    #######################         CLASS CONSTRUCTOR          #######################

    def __init__(self, board, drones, movement, nbMovement):
        self.board = board
        self.drones = drones
        self.movement = movement
        self.nbMovement = nbMovement
        # best way
        self.bestWay = None
        # nodes
        self.nodeUp = None
        self.nodeDown = None
        self.nodeLeft = None
        self.nodeRight = None

    ##################################################################################
    #######################              GETTERS               #######################

    def getBoard(self):
        return self.board

    def getDrones(self):
        return self.drones

    def getMovement(self):
        return self.movement

    def getNbMovement(self):
        return self.nbMovement

    def getNodeUp(self):
        return self.nodeUp

    def getNodeDown(self):
        return self.nodeDown

    def getNodeLeft(self):
        return self.nodeLeft

    def getNodeRight(self):
        return self.nodeRight

    ##################################################################################
    #######################              SETTERS               #######################

    def setMovement(self):
        return self.movement

    ##################################################################################
    #######################       CLASS STRING FOR DEBUG       #######################

    def toString(self):
        return False

    ##################################################################################
    #######################             FUNCTIONS              #######################

    # biggest function

    def generateTree(self):
        # check if all drones have their ways (-1 means OK, a number between 0 and number of drones - 1 means NOT OK)
        indexDrone = self.drones.haveTheirWays()
        if (indexDrone != -1):
            # check if it's possible to move on this way
            # if it's possible, compare movements (if same, keep the same number of movements, it will helps later)
            # if it's possible, check if this is the last movement from the drone: if yes, reset movement type
            # LEFT
            #indexDrone = 2
            if self.board.possibleToMove(self.drones.getDrone(indexDrone), EnumMovement.Movement.LEFT):
                #print("Node left created")
                localBoard = copy.deepcopy(self.board)
                localDrones = copy.deepcopy(self.drones)
                localNbMovement = copy.deepcopy(self.nbMovement)
                localMovement = copy.deepcopy(self.movement)
                localCurrentMovement = EnumMovement.Movement.LEFT
                # update board
                localBoard.moveDroneOnBoard(localDrones.getDrone(
                    indexDrone), EnumMovement.Movement.LEFT, localMovement, indexDrone)
                # check if not the same movement: increase number of moves done
                if localMovement != EnumMovement.Movement.LEFT:
                    localNbMovement = localNbMovement + 1
                # reset movement if that was last move
                if localDrones.getDrone(indexDrone).isReached():
                    localMovement = EnumMovement.Movement.NONE
                # create node
                self.nodeLeft = QuartenaireTree(
                    localBoard, localDrones, localMovement, localNbMovement)
                #localBoard.idString()
                self.nodeLeft.generateTree()

            # RIGHT
            if self.board.possibleToMove(self.drones.getDrone(indexDrone), EnumMovement.Movement.RIGHT):
                #print("Node right created")
                localBoard = copy.deepcopy(self.board)
                localDrones = copy.deepcopy(self.drones)
                localNbMovement = copy.deepcopy(self.nbMovement)
                localMovement = copy.deepcopy(self.movement)
                localCurrentMovement = EnumMovement.Movement.RIGHT
                # update board
                localBoard.moveDroneOnBoard(localDrones.getDrone(
                    indexDrone), localCurrentMovement, localMovement, indexDrone)
                # check if same movement: increase number of moves done
                if localMovement != localCurrentMovement:
                    localNbMovement = localNbMovement + 1
                # reset movement if that was last move
                if localDrones.getDrone(indexDrone).isReached():
                    localMovement = EnumMovement.Movement.NONE
                # create node
                self.nodeRight = QuartenaireTree(
                    localBoard, localDrones, localMovement, localNbMovement)
                #localBoard.idString()
                self.nodeRight.generateTree()
                

            # UP
            if self.board.possibleToMove(self.drones.getDrone(indexDrone), EnumMovement.Movement.UP):
                #print("Node up created")
                localBoard = copy.deepcopy(self.board)
                localDrones = copy.deepcopy(self.drones)
                localNbMovement = copy.deepcopy(self.nbMovement)
                localMovement = copy.deepcopy(self.movement)
                localCurrentMovement = EnumMovement.Movement.UP
                # update board
                localBoard.moveDroneOnBoard(localDrones.getDrone(
                    indexDrone), localCurrentMovement, localMovement, indexDrone)
                # check if same movement: increase number of moves done
                if localMovement != localCurrentMovement:
                    localNbMovement = localNbMovement + 1
                # reset movement if that was last move
                if localDrones.getDrone(indexDrone).isReached():
                    localMovement = EnumMovement.Movement.NONE
                # create node
                self.nodeUp = QuartenaireTree(
                    localBoard, localDrones, localMovement, localNbMovement)
                #localBoard.idString()
                self.nodeUp.generateTree()
                

            # DOWN
            if self.board.possibleToMove(self.drones.getDrone(indexDrone), EnumMovement.Movement.DOWN):
                #print("Node down created")
                localBoard = copy.deepcopy(self.board)
                localDrones = copy.deepcopy(self.drones)
                localNbMovement = copy.deepcopy(self.nbMovement)
                localMovement = copy.deepcopy(self.movement)
                localCurrentMovement = EnumMovement.Movement.DOWN
                # update board
                localBoard.moveDroneOnBoard(localDrones.getDrone(
                    indexDrone), localCurrentMovement, localMovement, indexDrone)
                # check if same movement: increase number of moves done
                if localMovement != localCurrentMovement:
                    localNbMovement = localNbMovement + 1
                # reset movement if that was last move
                if localDrones.getDrone(indexDrone).isReached():
                    localMovement = EnumMovement.Movement.NONE
                # create node
                self.nodeDown = QuartenaireTree(
                    localBoard, localDrones, localMovement, localNbMovement)
                #localBoard.idString()
                self.nodeDown.generateTree()
                
        else:
            self.board.idString()
            print("NUMBER OF MOVEMENTS:", self.nbMovement)
