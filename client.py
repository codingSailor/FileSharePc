import socket

def receiveFile():
    host="127.0.0.1"
    port=5000

    s=socket.socket()
    s.connect((host,port))

    data =s.recv(1024)
    print("Receiver working...")
    if data[:6] == 'EXITS':
        filesize = float(data[6:])
        message= input("Recieve file? (Y/N)->")
        if message=='Y':
            s.send('OK')
            f = open("New_"+filesize,'wb')
            data =s.recv(1024)
            totalrecv=len(data)
            f.write(data)
            while totalrecv < filesize:
                data = s.recv(1024)
                totalrecv = len(data)
                f.write(data)
                print("{0:2f}".format((totalrecv/float(filesize))*100)+"% Done \n")

            print("Download Complete!")
    else:
        print("file doesn not exist!")

    s.close()