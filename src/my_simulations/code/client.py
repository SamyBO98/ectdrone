import socket
import pickle
import sys
import argparse
from _thread import *
import time
from pymavlink import mavutil
from dronekit import connect, VehicleMode, LocationGlobalRelative
from ia import coordinates as Coordinates

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233
speed = 10 # meters / s
final_message = False # dernier message du serveur

def travel_vehicle_all_coordinates(vehicle, coordinates):
    """
        Travel a drone for each coordinates he needs to travel
        (Next step: for each case reached, calculate range between drone and final position with battery to determinate if the drone continues)
    """
    for c in coordinates.getCoordinatesToReach():
        currentCoDrone = Coordinates.Coordinates(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon)
        #print("[CLIENT] >> Le drone est actuellement a", currentCoDrone.toString(), "pour", c.toString())
        
        #droneCoordinates = Coordinates.Coordinates(vehicle.location.global_relative_frame.lon, vehicle.location.global_relative_frame.lat)
        #range = c.getVector(droneCoordinates)
        #timePause = range / speed
        #print("Drone", indice, "lui faut", timePause, "secondes pour atteindre", c.toString(),"Actuellement", droneCoordinates.toString(),"Lancement...")

        goto_position_target_global_int(vehicle, LocationGlobalRelative(c.getX(), c.getY(), vehicle.location.global_relative_frame.alt))
        #point = LocationGlobalRelative(c.getX(), c.getY(), vehicle.location.global_relative_frame.alt)
        #vehicle.simple_goto(point)
        #print("Velocity:", vehicle.velocity)
        
        while c.isReached(currentCoDrone) == False:
            currentCoDrone = Coordinates.Coordinates(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon)
            #print("Drone", indice, "aux coordonnees", Coordinates.Coordinates(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon).toString(), "pour aller en", c.toString())
            time.sleep(0.1)
        
        #time.sleep(15)
        ClientSocket.sendall(pickle.dumps(c))
        #print("[CLIENT] Le drone a atteint les coordonnees, NEXT...")
        
        #time.sleep(30)
    
    """
    # just testing
    for c in coordinates:
        print("Drone", indice, "se dirige aux coordonnees", c, "pour", seconds, "secondes.")
        goto_position_target_global_int(vehicle, LocationGlobalRelative(c[0], c[1], aTargetAltitude))
        time.sleep(seconds)
        print("Drone", indice, "est arrive aux coordonnees", vehicle.location.global_relative_frame)
    """

    #print("[CLIENT] >> Le drone a termine sa mission.")
    ClientSocket.sendall(pickle.dumps(True))

    vehicle.mode = VehicleMode("RTL")
    # Close vehicle object before exiting script
    vehicle.close()

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

def receive_messages_from_server(message):
    while True:
        data = ClientSocket.recv(4096)
        machin = pickle.loads(data)

        if type(machin) == bool:
            print("[CLIENT] >> Message from Server: EVERYTHING IS CLEARED! CONGRATULATIONS!")
            message = True
            break
        else:
            print(machin)

def arm_and_takeoff(vehicle, aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print('[CLIENT] >> Basic pre-arm checks in process...')
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print('[CLIENT] >> Waiting for vehicle to initialise...')
        time.sleep(1)

    print('[CLIENT] >> Arming motors')
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print('[CLIENT] >> Waiting for arming...')
        time.sleep(1)

    # on envoie des donnees pour indiquer que le robot est initialise
    # quand le serveur aura recu un message de tout le monde, il lancera l'algorithme
    # pendant ce temps, on fait voler le robot et le prochain message recu sera le tableau de coordonnees
    Data = vehicle.location.global_relative_frame
    print(type(vehicle.location.global_relative_frame.alt))
    ClientSocket.sendall(pickle.dumps(Data))

    print('[CLIENT] >> Taking off!')
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        #print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print('[CLIENT] >> Reached target altitude!')
            print('[CLIENT] >> Waiting for coordinates from the server...')

            # thread pour recevoir les messages du serveur (de la part des autres drones)
            start_new_thread(receive_messages_from_server, (final_message,))

            # on recoit les coordonnees du serveur
            # confirmation qu'il est connecte
            Response = ClientSocket.recv(4096)
            coordinates = pickle.loads(Response)
            travel_vehicle_all_coordinates(vehicle, coordinates)
            break

        time.sleep(1)

def check_for_final_message():
    while True:
        if final_message == True:
            break

        time.sleep(5)


# parser arguments
parser = argparse.ArgumentParser(description="Connect drone")
parser.add_argument('connect', type=str, help="the url of the drone")

if __name__ == '__main__':
    args = parser.parse_args(sys.argv[1:])
    #print(args.connect)

    print('[CLIENT] >> Waiting for a Connection...')
    try:
        ClientSocket.connect((host, port))
    except socket.error as e:
        print(str(e))

    # confirmation qu'il est connecte
    Response = ClientSocket.recv(4096)
    print(Response)

    # broadcast: tout les robots sont connectes
    Response = ClientSocket.recv(4096)
    print(Response)

    # on envoie au serveur les coordonnees
    print('[CLIENT] >> Drone is being connected...')
    connection_string = args.connect
    vehicle = connect(connection_string, wait_ready=True)
    vehicle.airspeed = speed
    vehicle.groundspeed = speed
    arm_and_takeoff(vehicle, 20)

    # on lance le robot
    # une fois pret on envoie une notif au serveur
    #Response = ClientSocket.recv(4096)
    
    check_for_final_message()

    ClientSocket.close()