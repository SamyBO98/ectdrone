#!/usr/bin/python
class Zone:

    ##################################################################################
    #######################   EXPLANATIONS ABOUT THIS CLASS    #######################

    ## Here are explanations


    ##################################################################################
    #######################         CLASS CONSTRUCTOR          #######################

    def __init__(self, height, width):
        self.height = height + 0.0
        self.width = width + 0.0


    ##################################################################################
    #######################              GETTERS               #######################

    # Get Height (float)
    def getHeight(self):
        return self.height

    # Get Width (float)
    def getWidth(self):
        return self.width


    ##################################################################################
    #######################              SETTERS               #######################

    # Set Height (float)
    def setHeight(self, height):
        self.height = height + 0.0

    # Set Width (float)
    def setWidth(self, width):
        self.width = width + 0.0


    ##################################################################################
    #######################       CLASS STRING FOR DEBUG       #######################

    def toString(self):
        return 'Zone:', [self.height, self.width]


    ##################################################################################
    #######################             FUNCTIONS              #######################