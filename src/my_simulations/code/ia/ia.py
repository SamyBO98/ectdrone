#!/usr/bin/python
################################################################
####################     IMPORT CLASSES     ####################
################################################################
import inspect
import coordinates as Coordinates
import zone as Zone
import case as Case
import board as Board

################################################################
######################     MAIN CLASS     ######################
################################################################
if __name__ == "__main__":
    boardDrone = Board.Board(Zone.Zone(501, 500), Zone.Zone(100, 100))
    boardDrone.toString()