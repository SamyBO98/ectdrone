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
vehicle1.airspeed = 10
vehicle1.groundspeed = 10
vehicle2.airspeed = 10
vehicle2.groundspeed = 10

def arm_and_takeoff(v1,v2,altitudeV1,altitudeV2):
    """
    Arms vehicle1,vehicle2 and fly to aTargetAltitude.
    """

    print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    while not v1.is_armable:
        print " Waiting for vehicle1 to initialise..."
        time.sleep(1)
    while not v2.is_armable:
        print " Waiting for vehicle2 to initialise..."
        time.sleep(1)

    print "Arming motors"
    # Copter should arm in GUIDED mode
    v1.mode = VehicleMode("GUIDED")
    v2.mode = VehicleMode("GUIDED")
    v1.armed = True
    v2.armed = True

    # Confirm vehicle armed before attempting to take off
    while not v1.armed:
        print " Waiting for vehicle1 arming..."
        time.sleep(1)
    while not v2.armed:
        print " Waiting for vehicle2 arming..."
        time.sleep(1)    

    print "Taking off! Vehicle1"
    v1.simple_takeoff(altitudeV1) # Take off to target altitude
    print "Taking off! Vehicle2"
    v2.simple_takeoff(altitudeV2) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print " Altitude Vehicle1: ", v1.location.global_relative_frame.alt
        print " Altitude Vehicle2: ", v2.location.global_relative_frame.alt
        #Break and return from function just below target altitude.
        if v1.location.global_relative_frame.alt>=altitudeV1*0.95:
            print "Reached target altitude"
            break
        if v2.location.global_relative_frame.alt>=altitudeV2*0.95:
            print "Reached target altitude"
            break

        time.sleep(1)


def start_move(v1,x1,y1,z1,duration1,v2,x2,y2,z2,duration2):
    """
    Move vehicle in direction based on specified velocity vectors.
    """
    msgVehicle1 = v1.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, 0, 0, # x, y, z positions (not used)
        x1, y1, z1, # x, y, z velocity in m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    msgVehicle2 = v2.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, 0, 0, # x, y, z positions (not used)
        x2, y2, z2, # x, y, z velocity in m/s
        0, 0, 0, # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)


    # send command to vehicle on 1 Hz cycle
    for x in range(0,duration1):
        v1.send_mavlink(msgVehicle1)
        time.sleep(1)
    for y in range(0,duration2):
        v2.send_mavlink(msgVehicle2)
        time.sleep(1)    

if __name__ == "__main__":
    arm_and_takeoff(vehicle1,vehicle2,10,20)
    # velocity_x > 0 => fly North
    # velocity_x < 0 => fly South
    # velocity_y > 0 => fly East
    # velocity_y < 0 => fly West
    # velocity_z < 0 => ascend
    # velocity_z > 0 => descend
    start_move(vehicle1,2,0,0,2,vehicle2,-2,0,0,2)
    vehicle1.mode = VehicleMode("RTL")
    vehicle2.mode = VehicleMode("RTL")
    vehicle1.close()
    vehicle2.close()
    
