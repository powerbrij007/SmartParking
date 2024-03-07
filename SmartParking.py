import socket
import threading
import time
#------ Smart Parking 
#====================== SmartParking
# Number of parking lots: z
# Number of parkonly: p
# ESC : Energy Storage Capacity: e
# SoC : Current Power Status: s
# Public key: u
# Private Key: k
# Smart Contract Address: c
#=======================
import subprocess
import random

import optparse
#For connecting to blockchain
#=========== ABI section
import json
#Web3 connection
from web3 import Web3

#============ Smart Parking
spAddress=""
spPrivateKey=""
smartContractAdd="" 
spTotalSlot=0 #Total number of parking
spParkOnly=0  #Parking only
spCapacity=0  #Power Capacity
spSoC=0       #State of Charge

#create a parser object
parser = optparse.OptionParser()


#adding argument
parser.add_option("-z")
parser.add_option("-p",dest="a",type="int", help="Car parameters")
parser.add_option("-u", help="User address")
parser.add_option("-k", help="User private address")
parser.add_option("-c", help="Contract address")
parser.add_option("-e", help="Energy Storage Capacity")
parser.add_option("-s", help="State of charge")
parser.add_option("-n", help="Number of participants")

(options, args)=parser.parse_args()
#Showing a meaningful address
if not options.a:
   #print("No argument is provided")
   parser.error("No argument is provided")
else:
    a1=options.a
    spAddress=options.u
    spPrivateKey=options.k
    smartContractAdd=options.c
    spTotalSlot=0 #Total number of parking
    spParkOnly=0  #Parking only
    spCapacity=options.e  #Power Capacity
    spSoC=options.s
    nParticipant=options.n





#==================== Server Section
PORT=5051
#SERVER="127.0.0.1" #local host or can be IP of your system

#Automatically getting IP address
#SERVER=socket.gethostbyname(socket.gethostname())
result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
output = result.stdout.strip()
myIp=output.split() #-------------- wifi and lan both
if len(myIp)==1:
    output=myIp[0]
else:
    output=myIp[0]

SERVER=output

#Address
ADDR = (SERVER,PORT)
#socket
server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Header
HEADER=64
FORMAT = 'utf-8'

#Disconnecting
DISCONNECT_MESSAGE="!DISCONNECT"

#Binding the address and socket
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW Connection] {addr} connected.")
    connected=True
    while connected:
        msg= conn.recv(1024).decode(FORMAT)
        if msg==DISCONNECT_MESSAGE:
            connected=False
            break
        elif msg=="":
            pass
        else:
            print(f"[{addr}{msg}]")
    conn.close()


def startServer():
    server.listen()
    print(f"[LISTENING] on ip..{SERVER}")
    while True:
        conn,addr = server.accept()
        thread=threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        #print(f"[ACTIVE CONNECTIONS {threading.active_count()-1}")
        parkingBalance()
        powerStatus()
        #subprocess.run("clear")

print("[STARTING] Smart parking..")
print("Smart parking address:",spAddress)
print("Smart parking privateKey:",spPrivateKey)
print("Smart contract:",smartContractAdd)

def getGasConsumed(self,functionName,tx):
    receipt = self.w3.eth.wait_for_transaction_receipt(tx)
    gas_used = receipt['gasUsed']
    print("Function:",functionName,"Gas used:",gas_used)


       #============================ for getting transaction details [ CSV ]
def transactionDetails(funcName,exeTime,tx,demand):
       fPath="results/results"+str(nParticipant)
       fPath1=fPath+"/allTransactions.csv"
       data=w3.eth.wait_for_transaction_receipt(tx)
       if funcName=="registerParking":
           fPath=fPath+"/registerParking.csv"
       elif funcName=="updateParking":
           #================================================ Recording the EV demands
           fPath=fPath+"/updateParking.csv"
       
       with open(fPath, 'a') as f:
          print(funcName,",",data['from'],",",data['to'],",",exeTime,",",data['gasUsed'], file=f)
       
       #========================== All Transactions in a file
       with open(fPath1,'a') as f:
           if demand !=0:
               print(funcName,",",data['from'],",",data['to'],",",exeTime,",",data['gasUsed'], file=f)
           else:
               print(funcName,",",data['from'],",",data['to'],",",exeTime,",",data['gasUsed'],",",demand, file=f)




#=========================== policy creator
#===================== Blockchain Connection
#====Connecting to blockchain
f=open('./abis/smartParking.json') #manually feeded
abi=json.load(f)
#print(abi)
link= "HTTP://"+output+":8545"
#w3=Web3(Web3.HTTPProvider('HTTP://127.0.0.1:8545'))
w3=Web3(Web3.HTTPProvider(link))
x=w3.is_connected()
print("Blockchain Connection status....",x)
       #===Connecting to the network and getting first address
       #user_number=input("Enter user number:[2-9]")
       #self.address1=self.w3.eth.accounts[int(user_number)]
uAdd=Web3.to_checksum_address(spAddress)
privKey=spPrivateKey
print("Your address:",uAdd)
print("Your balance:",w3.eth.get_balance(uAdd))
#===============================Setting default account
w3.eth.default_account=uAdd
#=====To communicate to a contract we need 1)Contract address 2)contract abi
cAdd=Web3.to_checksum_address(smartContractAdd)
#========= instantiating contract through the contract address
newContract=w3.eth.contract(address=cAdd,abi=abi)

start = time.time()
tx=newContract.functions.registerParking(1000,1000,10).transact()
            #msg = fetch_transaction_revert_reason(Web3,self.newContract.functions.vehicleRegistration(self.uAdd,self.vName,self.b_capacity,self.groundClear).transact())
end=time.time()
exeTime=(end-start) * 10**3
print("Smart Parking Created:",(end-start) * 10**3, "ms")
transactionDetails("registerParking",exeTime,tx,0)
#self.transactionDetails("evRegistration",exeTime,tx,0)
print("=========Starting Server==========")


def powerStatus():
    receivedPower=random.randint(1,20)
    tx=""
    start = time.time()
    tx=newContract.functions.updateParking(receivedPower,1,uAdd).transact()
            #msg = fetch_transaction_revert_reason(Web3,self.newContract.functions.vehicleRegistration(self.uAdd,self.vName,self.b_capacity,self.groundClear).transact())
    end=time.time()
    exeTime=(end-start) * 10**3
    print("Power received:",exeTime, "ms")
    transactionDetails("updateParking",exeTime,tx,receivedPower)


def parkingBalance():
           bal=w3.eth.get_balance(uAdd)
           print("Parking balance:",w3.from_wei(bal,'ether'))


#def parkingStatus():



startServer()