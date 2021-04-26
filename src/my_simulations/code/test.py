#!/usr/bin/env python
from dronekit import connect, VehicleMode,LocationGlobalRelative,APIException
import time
import socket
import exceptions
import math
import argparse
from pymavlink import mavutil
from threading import Thread

connection_string1 = '127.0.0.1:14550'
#connection_string2 = '127.0.0.1:14560'
vehicle1 = connect(connection_string1,wait_ready=True)
#vehicle2 = connect(connection_string2,wait_ready=True)
vehicle1.airspeed = 10
vehicle1.groundspeed = 10
#vehicle2.airspeed = 10
#vehicle2.groundspeed = 10



def start_move(v1,x1,y1,z1,duration1):

    while True:
        x = input('Enter lat: ')
        y = input('Enter lon: ')

        print("Goto: ", x, "-", y, ". Current drone coordinates: ", v1.location.global_relative_frame.lat, "-", v1.location.global_relative_frame.lon)

        msg = v1.message_factory.set_position_target_global_int_encode(
            0,       # time_boot_ms (not used)
            0, 0,    # target system, target component
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, # frame
            0b0000111111111000, # type_mask (only speeds enabled)
            x*1e7, # lat_int - X Position in WGS84 frame in 1e7 * meters
            y*1e7, # lon_int - Y Position in WGS84 frame in 1e7 * meters
            10, # alt - Altitude in meters in AMSL altitude, not WGS84 if absolute or relative, above terrain if GLOBAL_TERRAIN_ALT_INT
            0, # X velocity in NED frame in m/s
            0, # Y velocity in NED frame in m/s
            0, # Z velocity in NED frame in m/s
            0, 0, 0, # afx, afy, afz acceleration (not supported yet, ignored in GCS_Mavlink)
            0, 0)    # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

        # send command to vehicle
        v1.send_mavlink(msg)


def arm_and_takeoff(v1,altitude):
    v1.mode = VehicleMode("GUIDED")
    v1.armed = True
    v1.simple_takeoff(altitude) # Take off to target altitude 
    while True:
        pass
        if v1.location.global_relative_frame.alt>=altitude*0.95:
            # start_move(vehicle,x,y,z,duration)
            # velocity_x > 0 => fly North
            # velocity_x < 0 => fly South
            # velocity_y > 0 => fly East
            # velocity_y < 0 => fly West
            # velocity_z < 0 => ascend
            # velocity_z > 0 => descend
            # put x,y,z,duration in parameter of arm_and_takeoff to personalize movements
            # add to threads parameters too
            print("Coordinates: ", v1.location.global_relative_frame.lat, "-", v1.location.global_relative_frame.lon)
            start_move(v1,2,0,0,2)     

def land(v1):
    v1.mode = VehicleMode("RTL")
    v1.close()

if __name__ == "__main__":
    f1 = Thread(target=arm_and_takeoff,args=(vehicle1,10))
    f1.daemon = True 
    f1.start()

    #f2 = Thread(target=arm_and_takeoff,args=(vehicle2,5))
    #f2.daemon = True 
    #f2.start()
    try:
        #ctrl C to end script and print Fini
        while True:
            #print('En vol')
            time.sleep(1.0)
    except KeyboardInterrupt:
        pass

    print('Fini')
    

