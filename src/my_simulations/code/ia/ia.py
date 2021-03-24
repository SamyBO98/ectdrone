#!/usr/bin/python
################################################################
####################     IMPORT CLASSES     ####################
################################################################
import inspect
import coordinates as Coordinates
import zone as Zone
import case as Case
import board as Board
import drones as Drones
import drone as Drone

################################################################
######################     MAIN CLASS     ######################
################################################################
if __name__ == "__main__":

    # drones  
    dronesFromGazebo = Drones.Drones()

    # add drones
    drone1 = Drone.Drone(Coordinates.Coordinates(0, 0))
    drone2 = Drone.Drone(Coordinates.Coordinates(10, 0))
    drone3 = Drone.Drone(Coordinates.Coordinates(0, 10))

    dronesFromGazebo.addDrone(drone1)
    dronesFromGazebo.addDrone(drone2)
    dronesFromGazebo.addDrone(drone3)

    boardDrone = Board.Board(Zone.Zone(500, 500), Zone.Zone(100, 100))
    boardDrone.idString()

    # get for each drone number of cases
    boardDrone.shareCasesForEachDrone(dronesFromGazebo)
    dronesFromGazebo.toString()