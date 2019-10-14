from pathlib import Path
from tkinter import *

import socket
import os

def showfiles(files,list):

    for i in range(len(files)):
        list.insert(i,files[i])
    list.pack()


def nextdir(*event):
    print("first line")
    sel = list.get(list.curselection()[0])
    print(sel)
    if os.path.isfile(sel):
        print("Its a file.")
    else:
        os.chdir(os.getcwd()+"\\"+sel)
        list.delete(0,'end')
        showfiles(os.listdir(os.getcwd()),list)
    print(os.getcwd())

def goback(*event):
    print("previous dir")
    os.chdir(Path(os.getcwd()).parent)
    showfiles(os.listdir(os.getcwd()), list)

def snd(*event):
    print("Sending file...")

    sendFile(list.get(list.curselection()[0]))

def sendFile(file):

    print(str(file))
    port = 5000

    s=socket.socket()
    host=socket.gethostname()
    s.bind((host,port))
    s.listen(5)

    print("Sender working...")
    try:
        while True:
            conn, addr=s.accept()

            print("Got connection from",addr)

            sf=file(os.getcwd()+"\\"+file)
            f=open(sf,'rb')
            l=f.read(1024)
            while l:
                conn.send(l)
                print("Sent ",repr(l))
                l=f.read(1024)
            f.close()

        print("Sucessfully sent!")
        conn.send("From Server to client: Terminating Connection")
    except Exception as e:
        print("SENDER EXCEPTION>>>>>>>>>>>>>\n"+e)

    conn.close()

def recv(*event):
    print("Reciveing file...")
    receiveFile()


def receiveFile():



    s=socket.socket()
    host="192.168.43.89"
    port = 5000
    s.connect((host,port))
    #s.send("From client side")


    print("Receiver working...")
    #print(os.chdir(homedir))
    with open('New_recieved','wb') as f:
        print("file opened...")
        try:
            while True:
                print('receiving data...')
                data = s.recv(1024)

                print("data=%s",(data))
                if not data:
                    f.close()
                    print("No more data")
                f.write(data)
        except Exception as e:
            print("RECEIVER EXCEPTION>>>>>>>>>>\n"+e)

    print("Successfully received!")
    s.close()
    print("Connection closed")

root=Tk()



#MAINFRAME
bg=PhotoImage(file="bg.png")
mainframe=Frame(root,bg="cyan",)
mainframe.pack(fill=BOTH)

#Frame for SEND and RECEIVE button
topframe=Frame(mainframe,bg="cyan",height=2)
topframe.pack()

#creating SEND button
sendb = PhotoImage(file="send.png")
send = Button(topframe, image=sendb)
send.bind("<ButtonRelease-1>",snd)
send.pack(side=LEFT)

#creating RECEIVE button
receiveb = PhotoImage(file="receive.png")
receive = Button(topframe, image=receiveb)
receive.bind("<ButtonRelease-1>",recv)
receive.pack()



#Frame for file list and Path
filesframe=Frame(mainframe,bg="black")
filesframe.pack(side=TOP,fill=BOTH)

scrollbar=Scrollbar(filesframe)
scrollbar.pack(side=RIGHT,fill=Y)

home=str(Path.home())
print(home)

#Lable for path
Lb1 = Label(filesframe,text="Current path :"+home,height=2)
Lb1.update()
Lb1.pack(side=TOP,fill=X)


homedir=home.replace('\\','//')
print(homedir)
directory=os.chdir(homedir)
files=os.listdir(homedir)
print(files)


# list for files
list=Listbox(filesframe,yscrollcommand=scrollbar.set)
showfiles(files,list)
list.bind("<ButtonRelease-1>",nextdir)
scrollbar.config(command = list.yview)
list.pack(fill=BOTH)

#Frame for Back button
bottomframe=Frame(mainframe)
bottomframe.pack(fill=BOTH)

#BACK Button
backbtn=Button(filesframe,text="Back")
backbtn.pack(side=TOP,fill=BOTH)
backbtn.bind("<ButtonRelease-1>",goback)


root.mainloop()



