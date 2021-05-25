#!/usr/bin/python
# coding: utf8
class Case:
    '''
    @summary: Utilisé pour l’algorithme de recherche. Il contient une zone, la coordonnée (centrée sur la zone donnée) et l’id du drone qui a visité cette case
    '''

    ##################################################################################
    #######################         CLASS CONSTRUCTOR          #######################

    def __init__(self, coordinate, zone):
        '''
        @summary: Création d'une case. Contient une zone, sa coordonnée centrée et l'id du drone qui a visité cette zone
        @param coordinate: Centre de la zone
        @type coordinate: <Class> Coordinates
        @param zone: Zone
        @type zone: <Class> Zone
        '''
        self.center = coordinate
        self.zone = zone
        self.idDrone = -1


    ##################################################################################
    #######################              GETTERS               #######################

    def getCenter(self):
        '''
        @summary: Retourne la coordonnée centrée sur la zone
        @return: <Class> Coordinates
        '''
        return self.center
    
    def getZone(self):
        '''
        @summary: Retourne la zone
        @return: <Class> Zone
        '''
        return self.zone

    def getIdDrone(self):
        '''
        @summary: Retourne l'id du drone qui a visité la zone (par défaut: -1 pour non visitée)
        @return: int
        '''
        return self.idDrone


    ##################################################################################
    #######################              SETTERS               #######################

    def setCenter(self, coordinate):
        '''
        @summary: Définit une coordonnée
        @param coordinate: Coordonnée centrée de la zone
        @type coordinate: <Class> Coordinates
        '''
        self.center = coordinate

    def setZone(self, zone):
        '''
        @summary: Définit une zone
        @param idDrone: Zone
        @type idDrone: <Class> Zone
        '''
        self.zone = zone

    def setIdDrone(self, idDrone):
        '''
        @summary: Définit à la case l'id du drone qui aura visité cette zone
        @param idDrone: id du drone
        @type idDrone: int
        '''
        self.idDrone = idDrone


    ##################################################################################
    #######################       CLASS STRING FOR DEBUG       #######################

    def toString(self):
        '''
        @summary: Fonction retournant les informations globales de la classe
        @return: str
        '''
        return self.center.toString(), self.zone.toString(), str(self.idDrone)

    def idString(self):
        '''
        @summary: Fonction retournant l'id du drone qui a visité la zone
        @return: str ('-' par défaut)
        '''
        if self.idDrone == -1:
            return '-'
        else:
            return str(self.idDrone)