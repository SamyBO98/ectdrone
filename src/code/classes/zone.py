#!/usr/bin/python
# coding: utf8
class Zone:
    '''
    @summary: Représente une zone (longueur, largeur)
    '''

    ##################################################################################
    #######################         CLASS CONSTRUCTOR          #######################

    def __init__(self, height, width):
        '''
        @summary: Création d'une zone
        @param height: Longueur de la zone
        @type height: float
        @param width: Largeur de la zone
        @type width: float
        '''
        self.height = height + 0.0
        self.width = width + 0.0


    ##################################################################################
    #######################              GETTERS               #######################

    def getHeight(self):
        '''
        @summary: Retourne la longueur de la zone
        @return: float
        '''
        return self.height

    def getWidth(self):
        '''
        @summary: Retourne la largeur de la zone
        @return: float
        '''
        return self.width


    ##################################################################################
    #######################              SETTERS               #######################

    def setHeight(self, height):
        '''
        @summary: Définit la longueur de la zone
        @param height: Longueur de la zone
        @type height: float
        '''
        self.height = height + 0.0

    def setWidth(self, width):
        '''
        @summary: Définit la largeur de la zone
        @param width: Largeur de la zone
        @type width: float
        '''
        self.width = width + 0.0


    ##################################################################################
    #######################       CLASS STRING FOR DEBUG       #######################

    def toString(self):
        '''
        @summary: Fonction retournant les informations globales de la classe
        @return: str
        '''
        return 'Zone:', [self.height, self.width]