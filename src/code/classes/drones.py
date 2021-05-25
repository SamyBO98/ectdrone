#!/usr/bin/python
# coding: utf8
class Drones:
    '''
    @summary: Représente une liste de drones
    '''

    ##################################################################################
    #######################         CLASS CONSTRUCTOR          #######################

    def __init__(self):
        '''
        @summary: Création d'un tableau de drones (vide par défaut)
        '''
        self.drones = []
        self.nbDrones = 0


    ##################################################################################
    #######################              GETTERS               #######################

    def getDrones(self):
        '''
        @summary: Retourne la liste de drones
        @return: [array] <Class> Drone
        '''
        return self.drones

    def getDrone(self, i):
        '''
        @summary: Retourne un drone dans la liste de drones
        @param i: Index du drone
        @type i: int
        @return: <Class> Drone
        '''
        return self.drones[i]

    def getNbDrones(self):
        '''
        @summary: Retourne le nombre de drones existants
        @return: int
        '''
        return self.nbDrones


    ##################################################################################
    #######################       CLASS STRING FOR DEBUG       #######################

    def toString(self):
        '''
        @summary: Fonction retournant les informations globales de la classe
        '''
        for i in range(self.nbDrones):
            print(self.drones[i].toString())

    def coordinatesString(self):
        '''
        @summary: Fonction retournant les informations globales sur la liste de coordonnées à explorer pour chaque drone existant
        '''
        for i in range(self.nbDrones):
            print("Drone", i, ": ", self.drones[i].coordinatesString(0))

    def indexString(self):
        '''
        @summary: Fonction retournant les informations globales sur la liste d'index des coordonnées à explorer pour chaque drone existant
        '''
        for i in range(self.nbDrones):
            print("Drone", i, ": ", self.drones[i].indexString(0))


    ##################################################################################
    #######################             FUNCTIONS              #######################

    def addDrone(self, drone):
        '''
        @summary: Ajoute un drone à la liste de drones
        @param drone: Nouveau drone
        @type drone: <Class> Drone
        '''
        self.drones.append(drone)
        self.nbDrones = self.nbDrones + 1

    def haveTheirWays(self):
        '''
        @summary: Retourne l'indice du drone qui n'a pas encore terminé toutes ses cases à explorer pendant la génération de l'algorithme
        @return: index du drone (par défaut -1)
        '''
        for i in range(self.nbDrones):
            if (self.drones[i].getNbCases() != self.drones[i].getCasesReach()):
                return i
        return -1

    def isLastMove(self, index):
        '''
        @summary: Vérifie si le drone specifié est sur le point de finaliser son exploration (dernière coordonnée à franchir)
        @param index: Index du drone
        @type index: int
        @return: bool
        '''
        return self.drones[index].getCasesReach() == self.drones[index].getNbCases() - 1