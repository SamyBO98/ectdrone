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

    # create board
    boardDrone = Board.Board(Coordinates.Coordinates(-35.363041, 149.164961), Coordinates.Coordinates(-35.363484, 149.165521), Zone.Zone(0.00012, 0.00012))
    boardDrone.idString()
    boardDrone.toString()

    # drones  
    dronesFromGazebo = Drones.Drones()

    # add drones
    drone1 = Drone.Drone(Coordinates.Coordinates(-35.3632621, 149.1647968))
    drone2 = Drone.Drone(Coordinates.Coordinates(-35.3632621, 149.1656779))

    dronesFromGazebo.addDrone(drone1)
    dronesFromGazebo.addDrone(drone2)

    
    # get for each drone number of cases
    boardDrone.shareCasesForEachDrone(dronesFromGazebo)
    dronesFromGazebo.toString()

    # determinate where each drone will start his travel
    boardDrone.firstCoordinatesForEachDrone(dronesFromGazebo)
    boardDrone.idString()
    dronesFromGazebo.coordinatesString()

    raw_input("Enter to continue...")

    # starting to create a way for each drone to capture the zone
    tree = Tree.QuartenaireTree(boardDrone, dronesFromGazebo, EnumMovement.Movement.NONE, 0)
    tree.generateTree()
    #boardDrone.idString()

    raw_input("Enter to continue...")

    # get the best way for drones and prints it
    bestWay = tree.getBestWay()
    print("==============================")
    if bestWay == None:
        print("None...")
    else:
        bestWay[0].idString() # map
        print(bestWay[1].getDrone(0).toString()) # all coordinates (and cases)
        print(bestWay[1].getDrone(1).toString()) # all coordinates (and cases)
        print("Number of movements:", bestWay[2]) # movements count
    print("==============================")