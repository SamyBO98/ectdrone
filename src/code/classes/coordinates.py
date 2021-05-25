#!/usr/bin/python
# coding: utf8
from math import *
class Coordinates:
    '''
    @summary: Utilisé pour définir une coordonnée GPS: la latitude et la longitude (respectivement X et Y)
    '''

    ##################################################################################
    #######################         CLASS CONSTRUCTOR          #######################

    def __init__(self, x, y):
        '''
        @summary: Création d'une coordonnée
        @param x: Latitude de la coordonnée
        @type x: float
        @param y: Longitude de la coordonnée
        @type y: float
        '''
        self.x = x + 0.0
        self.y = y + 0.0


    ##################################################################################
    #######################              GETTERS               #######################

    def getX(self):
        '''
        @summary: Retourne la latitude (X)
        @return: float
        '''
        return self.x
    
    def getY(self):
        '''
        @summary: Retourne la longitude (Y)
        @return: float
        '''
        return self.y


    ##################################################################################
    #######################              SETTERS               #######################

    def setX(self, x):
        '''
        @summary: Définit la latitude (X)
        @param x: Latitude de la coordonnée
        @type x: float
        '''
        self.x = x + 0.0

    def setY(self, y):
        '''
        @summary: Définit la longitude (Y)
        @param y: Longitude de la coordonnée
        @type y: float
        '''
        self.y = y + 0.0


    ##################################################################################
    #######################       CLASS STRING FOR DEBUG       #######################

    def toString(self):
        '''
        @summary: Fonction retournant les informations globales de la classe
        @return: str
        '''
        return 'Coordinates:', [self.x, self.y]


    ##################################################################################
    #######################             FUNCTIONS              #######################

    def getVector(self, coordinates):
        '''
        @summary: Calcule la distance à une autre coordonnée
        @param coordinates: Coordonnée
        @type coordinates: <Class> Coordinates
        @return: float
        '''
        return sqrt((coordinates.getX() - self.x)**2 + (coordinates.getY() - self.y)**2)

    def isReached(self, coordinates):
        '''
        @summary: Vérifie si cette coordonnée est proche d'une autre coordonnée
        @param coordinates: Coordonnée
        @type coordinates: <Class> Coordinates
        @return: bool
        '''
        return self.getVector(coordinates) < 0.00001