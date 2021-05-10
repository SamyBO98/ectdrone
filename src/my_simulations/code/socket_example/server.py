import socket
import os
import pickle
import TestClass
from _thread import *

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1234
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection, address):
    connection.send(str.encode('Welcome to the Servern'))
    while True:
        data = connection.recv(2048)
        print('I received from', address[0] + ':' + str(address[1]), pickle.loads(data))
        #reply = 'Server Says: ' + data.decode('utf-8')
        if not data:
            break
        connection.sendall(pickle.dumps(pickle.loads(data)))
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, address))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()