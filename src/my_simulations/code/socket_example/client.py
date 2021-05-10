import socket
import pickle
import TestClass

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1234

print('Waiting for connection...')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)

while True:
    x = input('x coordinates: ')
    y = input('y coordinates: ')
    Data = TestClass.TestClass(int(x), int(y))
    #Input = input('Say Something: ')
    #ClientSocket.send(str.encode(Input))
    ClientSocket.send(pickle.dumps(Data)) # envoie un objet
    Response = pickle.loads(ClientSocket.recv(1024)) # recoit un objet
    print(Response.toString())

ClientSocket.close()