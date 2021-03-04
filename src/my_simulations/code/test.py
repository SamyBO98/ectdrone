#!/usr/bin/env python
from dronekit import connect, VehicleMode,LocationGlobalRelative,APIException
import time
import socket
import exceptions
import math
import argparse
from pymavlink import mavutil


def connectMyCopter():
    parser = argparse.ArgumentParser(description='commands')
    parser.add_argument('--connect')
    args = parser.parse_args()

    connection_string = args.connect

    if not connection_string:
        import dronekit_sitl
        sitl = dronekit_sitl.start_default()
        connection_string = sitl.connection_string()

    vehicle = connect(connection_string,wait_ready=True)
    return vehicle

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """
    connected_drone = connectMyCopter()

    print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    while not connected_drone.is_armable:
        print " Waiting for vehicle to initialise..."
        time.sleep(1)

    print "Arming motors"
    # Copter should arm in GUIDED mode
    connected_drone.mode    = VehicleMode("GUIDED")
    connected_drone.armed   = True

    # Confirm vehicle armed before attempting to take off
    while not connected_drone.armed:
        print " Waiting for arming..."
        time.sleep(1)

    print "Taking off!"
    connected_drone.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print " Altitude: ", connected_drone.location.global_relative_frame.alt
        #Break and return from function just below target altitude.
        if connected_drone.location.global_relative_frame.alt>=aTargetAltitude*0.95:
            print "Reached target altitude"
            break
        time.sleep(1)



if __name__ == "__main__":
    arm_and_takeoff(20)