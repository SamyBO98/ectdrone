#coding:utf-8
import socket

# Dans le client on met toute la partie drone avec les mouvements
# Dans le serveur on met toute la partie traitement
# Serveur envoie les chemins au client

# Chopper les valeurs des batteries des différents drones
# Client envoie niveau de batterie au serv 
# Si une batterie arrive à 0 on calcule la distance + les batteries des autres et on affecte à celui qu'on veut 
# Le serveur renvoit les données au client qui s'adapter
# Ici on a qu'une seul socket qui permet au client d'envoyer et au serveur de recevoir
# Il faut faire une autre socket coté serveur pour que le serv puisse envoyer au client


batterieDrone1 = 10
batterieDrone2 = 20
batterieDrone3 = 50
batterieDrone4 = 100

host, port = ('localhost',5566)
socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    socket.connect((host,port))
    print "Client connecté"
    
    #Add batteries from all drones
    socket.sendall(str.encode("\n".join([str(batterieDrone1), str(batterieDrone2)])))
    print(batterieDrone1)

except:
    print "Connexion au serveur échouée"
finally:
    socket.close()
