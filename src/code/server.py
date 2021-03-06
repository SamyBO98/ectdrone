#!/usr/bin/python
# coding: utf8
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
from classes import coordinates as Coordinates
from classes import zone as Zone
from classes import case as Case
from classes import board as Board
from classes import drones as Drones
from classes import drone as Drone
from classes import tree4 as Tree
from classes import movement as EnumMovement

# parser arguments
parser = argparse.ArgumentParser(description="Drones")
parser.add_argument('nbDrones', type=int, help="gives number of drones by using this script")

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
Threads = []
ThreadsCountBeforeStartAlgorithm = 0

def broadcast(nbDrones):
    '''
    @summary: Envoi un broadcast à tout les clients connectés (ne fonctionne que quand le nombre de drones donné est atteint)
    @param nbDrones: Nombre de drones
    @type nbDrones: int
    '''
    print('[SERVER] >> Broadcast for my clients...')
    for Athread in Threads:
        Athread[0].sendall(str.encode("[CLIENT] Broadcast"))

def connect_client(connection, address):
    '''
    @summary: Envoi un message de bienvnue au client qui vient de se connecter
    @param connection: Socket de connection
    @param address: Socket d'addresse (inutile ici)
    '''
    connection.sendall(str.encode('[CLIENT] >> Welcome to the server!'))

def receive_coordinates(dronesThreads):
    '''
    @summary: Recoit les messages des clients (indiquant chacun ses coordonnées initiales) avant de lancer l'algorithme de recherche
    @param dronesThreads: Liste de drones connectés
    @type dronesThreads: [array] [socket de connection, socket d'addresse, [latitude, longitude], booléen indiquant si le drone à finit son exploration]
    '''
    for droneThread in dronesThreads:
        data = droneThread[0].recv(4096)
        machin = pickle.loads(data)
        droneThread[2] = machin
        print('[SERVER] >> I receive something:', machin)

    print('[SERVER] Start the algorithm...')

def generate_and_send_coordinates(dronesThreads):
    '''
    @summary: Génère le meilleur chemin pour chaque drone et les envoie par l'envoi d'un message
    @param dronesThreads: Liste de drones connectés
    @type dronesThreads: [array] [socket de connection, socket d'addresse, [latitude, longitude], booléen indiquant si le drone à finit son exploration]
    '''
    # Create drones array
    dronesFromGazebo = Drones.Drones()

    # Add drones
    for droneThread in dronesThreads:
        drone = Drone.Drone(Coordinates.Coordinates(droneThread[2].lat, droneThread[2].lon))
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

def drones_broadcast(droneThread):
    '''
    @summary: Recoit les messages des drones pour les envoyer aux autres (modèle client <=> serveur <=> client) à chaque fois qu'un drone à atteint une des coordonnées donnée pendant la phase d'exploration
    @param dronesThreads: Liste de drones connectés
    @type dronesThreads: [array] [socket de connection, socket d'addresse, [latitude, longitude], booléen indiquant si le drone à finit son exploration]
    '''
    while True:
        data = droneThread[0].recv(4096)
        machin = pickle.loads(data)

        # message recu = coordonnee: on continue
        # sinon, le drone a finit sa recherche
        if type(machin) != bool:
            print("[SERVER] >> I just received that " + str(droneThread[1][0]) + ":" + str(droneThread[1][1]) + " send me coordinates. I will make a broadcast")
            for drone in Threads:
                if drone[2] != droneThread[2]:
                    drone[0].sendall(pickle.dumps(
                        str.encode(
                            "[MESSAGE FROM SERVER] >> "
                            + str(droneThread[1][0]) + ":" + str(droneThread[1][1])
                            + " has just visited ["
                            + str(machin.getX()) + ", " + str(machin.getY()) + "]"
                        )
                    ))

        else:
            print("[SERVER] >> I just received that " + str(droneThread[1][0]) + ":" + str(droneThread[1][1]) + " finished his travel. I will prevent other drones")
            for drone in Threads:
                if drone[2] != droneThread[2]:
                    drone[0].sendall(
                        pickle.dumps(str.encode(
                            "[MESSAGE FROM SERVER] >> " 
                            + str(droneThread[1][0]) + ":" + str(droneThread[1][1])
                            + " has just finished his travel"
                        )
                    ))
            droneThread[3] = True
            break

def check_drones_finished():
    '''
    @summary: Vérifie si les drones ont tous finit leurs explorations
    '''
    while True:
        allDronesHaveFinished = True
        for droneThread in Threads:
            if droneThread[3] == False:
                allDronesHaveFinished = False
        
        if allDronesHaveFinished == True:
            break
        else:
            time.sleep(5)

def final_broadcast():
    '''
    @summary: Envoie un message final à tout les clients une fois qu'ils ont tous terminé leurs phases d'explorations
    '''
    print("[SERVER] >> Final broadcast in process...")
    for droneThread in Threads:
        droneThread[0].sendall(pickle.dumps(True))
    print("[SERVER] >> Server will be closed")

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
        Threads.append([Client, address, None, False])

        if len(Threads) == args.nbDrones:
            break
    
    broadcast(args.nbDrones)

    receive_coordinates(Threads)

    generate_and_send_coordinates(Threads)

    # fonction qui recupere les infos des drones
    # avec un while true (pour chaque info recu d'un drone, on broadcast...)
    # une fois qu'un robot a tout termine, il ping le client
    for droneThread in Threads:
        start_new_thread(drones_broadcast, (droneThread,))

    # fonction qui attend que tout les drones aient termines leurs parcours
    check_drones_finished()

    # broadcast final
    final_broadcast()

    ServerSocket.close()