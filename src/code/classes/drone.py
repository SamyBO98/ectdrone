#!/usr/bin/python
# coding: utf8
class Drone:
    '''
    @summary: Drone qui contient plusieurs informations: ses coordonnées initiales, un nombre de cases du tableau à franchir, un nombre de cases franchis, une liste de coordonnées à explorer et sa liste d'index du tableau associée
    '''

    ##################################################################################
    #######################         CLASS CONSTRUCTOR          #######################

    def __init__(self, coordinates):
        '''
        @summary: Initialise les informations utiles au bon fonctionnement du drone
        @param coordinates: Coordonnées initiales du drone
        @type coordinates: <Class> Coordinates
        '''
        self.coordinates = coordinates
        self.nbCases = 0
        self.casesReached = 0
        self.coordinatesToReach = []
        self.indexBoardToReach = []


    ##################################################################################
    #######################              GETTERS               #######################

    def getCoordinates(self):
        '''
        @summary: Retourne les coordonnées initiales
        @return: <Class> Coordinates
        '''
        return self.coordinates

    def getNbCases(self):
        '''
        @summary: Retourne le nombre de cases à explorer
        @return: int
        '''
        return self.nbCases

    def getCasesReach(self):
        '''
        @summary: Retourne le nombre de cases restantes à explorer
        @return: int
        '''
        return self.casesReached

    def getCoordinatesToReach(self):
        '''
        @summary: Retourne la liste de coordonnées à explorer
        @return: [array] <Class> Coordinates
        '''
        return self.coordinatesToReach

    def getIndexBoardToReach(self):
        '''
        @summary: Retourne la liste d'index des coordonnées à explorer
        @return: [array] [array] int
        '''
        return self.indexBoardToReach


    ##################################################################################
    #######################              SETTERS               #######################

    def setCoordinates(self, coordinates):
        '''
        @summary: Définit les coordonnées initiales
        @param coordinates: Nouvelles coordonnées initiales
        @type coordinates: <Class> Coordinates
        '''
        self.coordinates = coordinates

    def setNbCases(self, nbCases):
        '''
        @summary: Définit le nombre de cases à explorer
        @param nbCases: Nombre de cases à explorer
        @type nbCases: int
        '''
        self.nbCases = nbCases


    ##################################################################################
    #######################       CLASS STRING FOR DEBUG       #######################

    def toString(self):
        '''
        @summary: Fonction retournant les informations globales de la classe
        @return: str
        '''
        resCoordinates = ""
        resIndex = ""
        for i in range(len(self.coordinatesToReach)):
            resCoordinates = resCoordinates, i, self.coordinatesToReach[i].toString()
            resIndex = resIndex, i, self.indexBoardToReach[i]
        return 'Cases affected:', self.nbCases,"- coordinates:", resCoordinates, "- indexes:", resIndex 

    def coordinatesString(self, i):
        '''
        @summary: Fonction retournant les informations sur la liste de coordonnées à explorer selon l'indice donné
        @param i: Indice
        @type i: int
        @return: <Class> Coordinates
        '''
        return self.coordinatesToReach[i].toString()

    def indexString(self, i):
        '''
        @summary: Fonction retournant les informations sur la liste d'index des coordonnées à explorer selon l'indice donné
        @param i: Indice
        @type i: int
        @return: [int, int]
        '''
        return self.indexBoardToReach[i]


    ##################################################################################
    #######################             FUNCTIONS              #######################

    def addCaseReached(self):
        '''
        @summary: Ajoute une nouvelle case franchie pendant la génération de tout les chemins possibles
        '''
        self.casesReached = self.casesReached + 1

    def isReached(self):
        '''
        @summary: Vérifie si le drone à exploré toutes les cases
        @return: bool
        '''
        return self.nbCases == self.casesReached

    def addCoordinatesToReach(self, coordinates):
        '''
        @summary: Ajoute une nouvelle coordonnée à la liste de coordonnées à explorer
        @param coordinates: Indice
        @type coordinates: int
        '''
        self.coordinatesToReach.append(coordinates)

    def sizeCoordinatesToReach(self):
        '''
        @summary: Retourne la taille de la liste de coordonnées à explorer
        @return: int
        '''
        return len(self.coordinatesToReach)

    def getLastCoordinateReached(self):
        '''
        @summary: Retourne la dernière coordonnée de la liste de coordonnées à explorer
        @return: <Class> Coordinates
        '''
        return self.coordinatesToReach[-1]

    def updateLastCoordinateReached(self, coordinates):
        '''
        @summary: Met à jour la dernière coordonnée de la liste de coordonnées à explorer
        @param coordinates: Nouvelle coordonnée
        @type coordinates: <Class> Coordinates
        '''
        self.coordinatesToReach[-1] = coordinates

    def addIndexToReach(self, index):
        '''
        @summary: Ajoute un nouvel index à la liste d'index des coordonnées à explorer
        @param index: Index du tableau de cases
        @type index: [int, int]
        '''
        self.indexBoardToReach.append(index)

    def sizeIndexToReach(self):
        '''
        @summary: Retourne la taille de la liste d'index des coordonnées à explorer
        @return: int
        '''
        return len(self.indexBoardToReach)

    def getLastIndexReached(self):
        '''
        @summary: Retourne le dernier index de la liste d'index des coordonnées à explorer
        @return: [int, int]
        '''
        return self.indexBoardToReach[-1]

    def updateLastIndexReached(self, index):
        '''
        @summary: Met à jour le dernier index de la liste d'index des coordonnées à explorer
        @param index: Nouvel index du tableau de cases
        @type index: [int, int]
        '''
        self.indexBoardToReach[-1] = index