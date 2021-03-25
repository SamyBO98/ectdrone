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
import tree4 as Tree
import movement as EnumMovement

################################################################
######################     MAIN CLASS     ######################
################################################################
if __name__ == "__main__":

    # drones  
    dronesFromGazebo = Drones.Drones()

    # add drones
    drone1 = Drone.Drone(Coordinates.Coordinates(687, 890))
    drone2 = Drone.Drone(Coordinates.Coordinates(500, 500))
    drone3 = Drone.Drone(Coordinates.Coordinates(-15, -32))
    drone4 = Drone.Drone(Coordinates.Coordinates(140, 467))
    drone5 = Drone.Drone(Coordinates.Coordinates(390, 0))
    drone6 = Drone.Drone(Coordinates.Coordinates(-190, 267))

    dronesFromGazebo.addDrone(drone1)
    dronesFromGazebo.addDrone(drone2)
    dronesFromGazebo.addDrone(drone3)
    #dronesFromGazebo.addDrone(drone4)
    #dronesFromGazebo.addDrone(drone5)
    #dronesFromGazebo.addDrone(drone6)

    boardDrone = Board.Board(Zone.Zone(500, 500), Zone.Zone(100, 100))
    boardDrone.idString()

    # get for each drone number of cases
    boardDrone.shareCasesForEachDrone(dronesFromGazebo)
    dronesFromGazebo.toString()

    # determinate where each drone will start his travel
    boardDrone.firstCoordinatesForEachDrone(dronesFromGazebo)
    boardDrone.idString()
    dronesFromGazebo.coordinatesString()

    # starting to create a way for each drone to capture the zone
    tree = Tree.QuartenaireTree(boardDrone, dronesFromGazebo, EnumMovement.Movement.NONE, 0)
    tree.generateTree()
    #boardDrone.idString()

    bestWay = tree.getBestWay()
    print("==============================")
    bestWay[0].idString()
    bestWay[1].toString()
    print("Number of movements:", bestWay[2])
    print("==============================")