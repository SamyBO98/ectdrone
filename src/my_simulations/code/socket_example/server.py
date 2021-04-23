#coding:utf-8
import socket 
import threading



class ThreadForClient(threading.Thread):
    def __init__(self,conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        data1, data2 = [int(i) for i in self.conn.recv(2048).decode('utf-8').split('\n')]
        print str(data1) + " " + str(data2)


host, port = ('',5566)

socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.bind((host,port))
print("Le serveur est démarré")

while True:
    socket.listen(5)
    conn, address = socket.accept()
    print "Un client vient de se connecter"

    my_thread = ThreadForClient(conn)
    my_thread.start()


conn.close()
socket.close()