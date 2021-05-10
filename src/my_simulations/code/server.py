from __future__ import print_function
import socket
import os
import pickle
from _thread import *
import time
import socket
import exceptions
import math
import sys
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

# parser arguments
parser = argparse.ArgumentParser(description="Drones")
parser.add_argument('nbDrones', type=int, help="gives number of drones by using this script")

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1234
Threads = []
ThreadsCountBeforeStartAlgorithm = 0

def broadcast(nbDrones):
    print('[SERVER] >> Broadcast for my clients...')
    for Athread in Threads:
        Athread[0].sendall(str.encode("[CLIENT] Broadcast"))

def connect_client(connection, address):
    connection.sendall(str.encode('[CLIENT] >> Welcome to the server!'))
    """
    while True:
        data = connection.recv(2048)
        print('[SERVER] >> Received from ', address[0], ':', address[1], pickle.loads(data))
        #reply = 'Server Says: ' + data.decode('utf-8')
        # switch: check what data we receive
        if not data:
            break
        connection.sendall(pickle.dumps(pickle.loads(data)))
    connection.close()
    """

def receive_coordinates(dronesThreads):
    for droneThread in dronesThreads:
        data = droneThread[0].recv(4096)
        machin = pickle.loads(data)
        droneThread[2] = machin
        print('[SERVER] >> I receive something:', machin)

    print('[SERVER] Start the algorithm...')

def generate_and_send_coordinates(dronesThreads):
    # Create drones array
    dronesFromGazebo = Drones.Drones()

    # Add drones
    for droneThread in dronesThreads:
        drone = Drone.Drone(Coordinates.Coordinates(droneThread[2].lon, droneThread[2].lat))
        print(drone.getCoordinates().toString())
        dronesFromGazebo.addDrone(drone)

    # Create board
    boardDrone = Board.Board(Coordinates.Coordinates(-35.363041, 149.164961), Coordinates.Coordinates(-35.363484, 149.165521), Zone.Zone(0.00012, 0.00012))
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
    for i in range(len(dronesThreads)):
        Data = bestWay[1].getDrone(i)
        dronesThreads[i][0].sendall(pickle.dumps(Data))

    bestWay[0].idString()
    bestWay[1].toString()
    print("Number of movements:", bestWay[2])


if __name__ == '__main__':
    args = parser.parse_args(sys.argv[1:])
    #print(args.nbDrones)

    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))

    print('[SERVER] >> Waiting for a Connection...')
    ServerSocket.listen(5)

    while True:
        Client, address = ServerSocket.accept()
        print('[SERVER] >> Client', address[0], ':', address[1], 'is now connected!')
        start_new_thread(connect_client, (Client, address))
        Threads.append([Client, address, None])

        if len(Threads) == args.nbDrones:
            break
    
    broadcast(args.nbDrones)

    receive_coordinates(Threads)
    
    # just in case
    """
    for Athread in Threads:
        print('[SERVER | DEBUG] >>> ', Athread[2])
    """

    generate_and_send_coordinates(Threads)

    # fonction qui recupere les infos des drones
    # avec un while true (pour chaque info recu d'un drone, on broadcast...)
    # une fois qu'un robot a tout termine, il ping le client

    ServerSocket.close()