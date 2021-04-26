from __future__ import print_function
import time
import socket
import exceptions
import math
import argparse
from pymavlink import mavutil
from threading import Thread
from dronekit import connect, VehicleMode, LocationGlobalRelative
import inspect
from ia import coordinates as Coordinates
from ia import zone as Zone
from ia import case as Case
from ia import board as Board
from ia import drones as Drones
from ia import drone as Drone
from ia import tree4 as Tree
from ia import movement as EnumMovement

speed = 10 # meters / s

def travel_vehicle_all_coordinates(vehicle, coordinates, indice):
    """
        Travel a drone for each coordinates he needs to travel
        (Next step: for each case reached, calculate range between drone and final position with battery to determinate if the drone continues)
    """
    for c in coordinates.getCoordinatesToReach():
        
        #droneCoordinates = Coordinates.Coordinates(vehicle.location.global_relative_frame.lon, vehicle.location.global_relative_frame.lat)
        #range = c.getVector(droneCoordinates)
        #timePause = range / speed
        #print("Drone", indice, "lui faut", timePause, "secondes pour atteindre", c.toString(),"Actuellement", droneCoordinates.toString(),"Lancement...")

        goto_position_target_global_int(vehicle, LocationGlobalRelative(c.getX(), c.getY(), vehicle.location.global_relative_frame.alt))
        #point = LocationGlobalRelative(c.getX(), c.getY(), vehicle.location.global_relative_frame.alt)
        #vehicle.simple_goto(point)
        #print("Velocity:", vehicle.velocity)
        while c.isReached(Coordinates.Coordinates(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon)) == False:
            #print("Drone", indice, "aux coordonnees", Coordinates.Coordinates(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon).toString(), "pour aller en", c.toString())
            time.sleep(0.1)

        print("Drone", indice, "a atteint les coordonnees, NEXT...")
        
        #time.sleep(30)
    
    """
    # just testing
    for c in coordinates:
        print("Drone", indice, "se dirige aux coordonnees", c, "pour", seconds, "secondes.")
        goto_position_target_global_int(vehicle, LocationGlobalRelative(c[0], c[1], aTargetAltitude))
        time.sleep(seconds)
        print("Drone", indice, "est arrive aux coordonnees", vehicle.location.global_relative_frame)
    """

    print("Drone", indice, "a termine sa mission.")
    vehicle.mode = VehicleMode("RTL")

    # Close vehicle object before exiting script
    print("Fermeture du drone", indice)
    vehicle.close()
        


def arm_and_takeoff(vehicle, coordinates, indice, aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        #print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")

            ###############################################################
            #### FONCTION QUI PARCOURT TOUTES LES COORDONNEES DU DRONE ####
            ###############################################################
            travel_vehicle_all_coordinates(vehicle, coordinates, indice)

            break
        time.sleep(1)

def goto_position_target_global_int(vehicle, aLocation):
    """
    Send SET_POSITION_TARGET_GLOBAL_INT command to request the vehicle fly to a specified location.
    """
    msg = vehicle.message_factory.set_position_target_global_int_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # frame
        0b0000111111111000, # type_mask (only speeds enabled)
        aLocation.lat*1e7, # lat_int - X Position in WGS84 frame in 1e7 * meters
        aLocation.lon*1e7, # lon_int - Y Position in WGS84 frame in 1e7 * meters
        aLocation.alt, # alt - Altitude in meters in AMSL altitude, not WGS84 if absolute or relative, above terrain if GLOBAL_TERRAIN_ALT_INT
        0, # X velocity in NED frame in m/s
        0, # Y velocity in NED frame in m/s
        0, # Z velocity in NED frame in m/s
        0, 0, 0, # afx, afy, afz acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    # send command to vehicle
    vehicle.send_mavlink(msg)

if __name__ == "__main__":

    """
        Main
        -> Connect vehicles
        -> Get best way for each drones
        -> Launch threads: starts the travel
    """

    # Drone 1
    print("Connect drone 1")
    connection_string1 = '127.0.0.1:14550'
    vehicle1 = connect(connection_string1,wait_ready=True)
    vehicle1.airspeed = speed
    vehicle1.airspeed = speed

    # Drone 2
    print("Connect drone 2")
    connection_string2 = '127.0.0.1:14560'
    vehicle2 = connect(connection_string2,wait_ready=True)
    vehicle2.groundspeed = speed
    vehicle2.groundspeed = speed

    # Create drones array
    dronesFromGazebo = Drones.Drones()

    # Add drones
    print("Coordinates from drone 1: (test)", vehicle1.location.global_relative_frame)
    print("Coordinates from drone 2: (test)", vehicle2.location.global_relative_frame)
    #drone1 = Drone.Drone(Coordinates.Coordinates(vehicle1.location.global_relative_frame.lon, vehicle1.location.global_relative_frame.lat))
    #drone2 = Drone.Drone(Coordinates.Coordinates(vehicle2.location.global_relative_frame.lon, vehicle2.location.global_relative_frame.lat))
    drone1 = Drone.Drone(Coordinates.Coordinates(-35.3632621, 149.1647968))
    drone2 = Drone.Drone(Coordinates.Coordinates(-35.3632621, 149.1656779))

    dronesFromGazebo.addDrone(drone1)
    dronesFromGazebo.addDrone(drone2)

    # Create board
    boardDrone = Board.Board(Coordinates.Coordinates(-35.363040, 149.164960), Coordinates.Coordinates(-35.363484, 149.165520), Zone.Zone(0.00012, 0.00012))
    boardDrone.idString()
    boardDrone.toString()
    #boardDrone.idString()

    # Get for each drone number of cases to travel
    print("Share cases for each drone")
    boardDrone.shareCasesForEachDrone(dronesFromGazebo)
    #dronesFromGazebo.toString()

    # Determinate where each drone will start his travel
    print("Give coordinates for each drone")
    boardDrone.firstCoordinatesForEachDrone(dronesFromGazebo)
    boardDrone.idString()

    # Starting to create a way for each drone to capture the zone
    print("Creating tree...")
    tree = Tree.QuartenaireTree(boardDrone, dronesFromGazebo, EnumMovement.Movement.NONE, 0)
    tree.generateTree()
    #boardDrone.idString()

    # Get the best way for drones and prints it
    print("Get the best way...")
    bestWay = tree.getBestWay()
    drone1 = bestWay[1].getDrone(0)
    drone2 = bestWay[1].getDrone(1)
    bestWay[0].idString()
    bestWay[1].toString()
    print("Number of movements:", bestWay[2])
    

    # Launch threads
    f1 = Thread(target=arm_and_takeoff,args=(vehicle1, drone1, 0, 20))
    f1.daemon = True 
    f1.start()

    f2 = Thread(target=arm_and_takeoff,args=(vehicle2, drone2, 1, 20))
    f2.daemon = True 
    f2.start()
    
    """
    arm_and_takeoff(vehicle1, [], 0, 5)
    print("Drone 1 coordinates:", vehicle1.location.global_relative_frame)
    goto_position_target_global_int(vehicle1, LocationGlobalRelative(-35.3632619, 149.1652000, 6))
    """

    try:
        #ctrl C to end script and print Fini
        while True:
            time.sleep(5.0)
    except KeyboardInterrupt:
        pass


"""

arm_and_takeoff(10)

# Print location information for `vehicle` in all frames (default printer)
#print("Global Location: %s" % vehicle.location.global_frame)
#print("Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
#print("Local Location: %s" % vehicle.location.local_frame)    #NED

print("Set default/target airspeed to 3")
vehicle.airspeed = 3

print("Going towards first point for 30 seconds ...")
point1 = LocationGlobalRelative(0, 0, 25)
vehicle.simple_goto(point1)

# sleep so we can see the change in map
time.sleep(30)

print("Going towards second point for 30 seconds (groundspeed set to 10 m/s) ...")
point2 = LocationGlobalRelative(50, 0, 50)
vehicle.simple_goto(point2, groundspeed=10)

# sleep so we can see the change in map
time.sleep(30)

print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")

# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()

# Shut down simulator if it was started.
if sitl:
    sitl.stop()
"""