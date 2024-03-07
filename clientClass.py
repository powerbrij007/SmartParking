import socket
import threading

import subprocess

class Clients:
    PORT=0
    #SERVER="127.0.0.1" #local host or can be IP of your system
    #Automatically getting IP address
    result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
    output = result.stdout.strip()
    myIp=output.split() #------------ It works in both cases wirless and wired
    if len(myIp)==1:
        output=myIp[0]
    else:
        output=myIp[0]
    #link="http://"+output+":8545"
    SERVER=""   #input("Server:")
    #Address
    ADDR = (SERVER,PORT)
    #socket
    client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Header
    HEADER=64
    FORMAT = 'utf-8'

    #Disconnecting
    DC="!DISCONNECT"

    #Binding the address and socket
    #client.connect(ADDR)

    def __init__(self,s_ip, port,):
        self.SERVER=s_ip
        self.PORT=port
        #Address
        self.ADDR = (self.SERVER,self.PORT)
        #socket
        self.client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Binding the address and socket
        self.client.connect(self.ADDR)

    
    #client.send("Hello").encode(FORMAT)
    def send(self,msg):
        message=msg.encode(self.FORMAT)
        msg_length=len(message)
        send_length=str(msg_length).encode(self.FORMAT)
        self.client.send(message)


#
# send("Hello")
#send(DISCONNECT_MESSAGE)

""" a=Clients("127.0.1.1",5050)
a.send("Hello")
a.send("!DISCONNECT") """



