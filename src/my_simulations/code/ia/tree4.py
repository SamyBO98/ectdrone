#!/usr/bin/python
class QuartenaireTree:

    ##################################################################################
    #######################   EXPLANATIONS ABOUT THIS CLASS    #######################

    ## Here are explanations
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
            if drones.isLastMove(indexDrone):
                # reset movement type
            else:
                #TODO: THESE FUNCTIONS
                # LEFT
                insertLeft(self)
                # RIGHT
                insertRight(self)
                # UP
                insertUp(self)
                # DOWN
                insertDown(self)
