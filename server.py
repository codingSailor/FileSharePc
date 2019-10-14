import socket
import threading
import os

def sendFile(file):
    host = "127.0.0.1"
    port = 5000

    s=socket.socket()
    s.bind((host,port))
    s.listen(s)

    print("Sender working...")
    while True:
        c,addr=s.accept()
        print("Client connected is: "+str(addr))

        userResponse=c.recv(1024)
        if userResponse[:2]=='OK':
            with open(file,'rb') as f:
                bytesToSend = f.read(1024)
                c.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend=f.read(1024)
                    c.send(bytesToSend)

    c.close()
    s.close()

