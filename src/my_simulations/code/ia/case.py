#!/usr/bin/python
class Case:

    ##################################################################################
    #######################   EXPLANATIONS ABOUT THIS CLASS    #######################

    ## Here are explanations


    ##################################################################################
    #######################         CLASS CONSTRUCTOR          #######################

    def __init__(self, coordinate, zone):
        self.center = coordinate
        self.zone = zone
        self.idDrone = -1


    ##################################################################################
    #######################              GETTERS               #######################

    # Get Coordinates (Coordinate class)
    def getCenter(self):
        return self.center
    
    # Get Zone (Zone class)
    def getZone(self):
        return self.zone

    # Get id drone (int)
    def getIdDrone(self):
        return self.idDrone


    ##################################################################################
    #######################              SETTERS               #######################

    # Set Center (Coordinate class)
    def setCenter(self, coordinate):
        self.center = coordinate
    
    # Set Zone (float)
    def setZone(self, zone):
        self.zone = zone

    # Set id drone (int)
    def setIdDrone(self, idDrone):
        self.idDrone = idDrone


    ##################################################################################
    #######################       CLASS STRING FOR DEBUG       #######################

    def toString(self):
        return self.center.toString(), self.zone.toString(), str(self.idDrone)

    def idString(self):
        if self.idDrone == -1:
            return '-'
        else:
            return str(self.idDrone)


    ##################################################################################
    #######################             FUNCTIONS              #######################