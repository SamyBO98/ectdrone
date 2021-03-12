#!/usr/bin/env python
from dronekit import connect, VehicleMode,LocationGlobalRelative,APIException
import time
import socket
import exceptions
import math
import argparse
from pymavlink import mavutil

connection_string1 = '127.0.0.1:14550'
connection_string2 = '127.0.0.1:14560'
vehicle1 = connect(connection_string1,wait_ready=True)
vehicle2 = connect(connection_string2,wait_ready=True)

def arm_and_takeoff(vehicle1,vehicle2,altitudeV1,altitudeV2):
    """
    Arms vehicle1,vehicle2 and fly to aTargetAltitude.
    """

    print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    while not vehicle1.is_armable:
        print " Waiting for vehicle1 to initialise..."
        time.sleep(1)
    while not vehicle2.is_armable:
        print " Waiting for vehicle2 to initialise..."
        time.sleep(1)

    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle1.mode = VehicleMode("GUIDED")
    vehicle2.mode = VehicleMode("GUIDED")
    vehicle1.armed = True
    vehicle2.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle1.armed:
        print " Waiting for vehicle1 arming..."
        time.sleep(1)
    while not vehicle2.armed:
        print " Waiting for vehicle2 arming..."
        time.sleep(1)    

    print "Taking off! Vehicle1"
    vehicle1.simple_takeoff(altitudeV1) # Take off to target altitude
    print "Taking off! Vehicle2"
    vehicle2.simple_takeoff(altitudeV2) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print " Altitude Vehicle1: ", vehicle1.location.global_relative_frame.alt
        print " Altitude Vehicle2: ", vehicle2.location.global_relative_frame.alt
        #Break and return from function just below target altitude.
        if vehicle1.location.global_relative_frame.alt>=altitudeV1*0.95:
            print "Reached target altitude"
            break
        if vehicle2.location.global_relative_frame.alt>=altitudeV2*0.95:
            print "Reached target altitude"
            break

        time.sleep(1)



if __name__ == "__main__":
    arm_and_takeoff(vehicle1,vehicle2,10,15)
