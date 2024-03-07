#create a E_car
"""
Car Model: Name
Car Battery Capacity in KW
Car Current Battery status
Car Range in KM
Can cover range, on the basis of charge available
oneKm : power required for one Km (milage)


 [-p BatteryCapacity, BatteryStatus, range,TimesToDrive, groundClearance]
"""
 
import random
from math import floor

#-----Threading
import threading
 
 
#----Progress Bar
from time import sleep
from rich.progress import Progress
from rich.console import Console

#Server connection
import socket
import threading
#for client class
import clientClass

#For connecting to blockchain
#For connecting to blockchain
#=========== ABI section
import json
#Web3 connection
from web3 import Web3,exceptions
import os
import subprocess
#from eth_defi.event_reader.logresult import decode_log
#from web3-ethereum-defi import eth_defi.revert_reason

#import time module
import time
#import Bconnect

#MongoDB connection
#from transaction import Transactions


class E_car():
   vName=""
   EV_id=0
   carRange=0 #Range on full charging
   coverRange=0 #Range car can go
   oneKm=0 #Energy for one Km
   #===============================
   uAdd="" #user account
   privKey="" #users private key
   cAdd="" #Contract address
   w3="" #Web3 connection
   x="" #web3 connection parameter
   newContract="" #instance of Contract
   #==========================Battery
   b_type="" #Type of battery
   b_age=0 #in months from buy
   b_life=0 #in year 
   b_opt_temp=0 #battery operating temperature
   b_degradationFactor=0 #Degradation factor of battery
   b_power_output=0 #power output of battery [Discharge rate]
   b_cycle=0 #Number of times charge
   b_capacity=0 # in kWh
   b_status=0 # in %
   b_charged=0 #in kWh
   b_resistance_full=0 #Full charged battery resistance
   b_discharge_time=0 #Discharge time in hours
   b_charging_mode=['wired','wireless'] # [ Cabled, Wireless ]
   #=======================================EV
   values=[['normal',20], ['medium',60], ['heavy',130], ['very heavy',200]]
   userType=""
   dailyDrive=0
   suddenDrive=random.randint(0,50)
   #-------------------------
   carAge=0 #Age of EV
   carRange=0 #Range on full charging
   coverRange=0 #Range car can go
   oneKm=0 #Energy for one Km
   distanceTraveled=0 #Distance Traveled
   #==============================Ground Clearance
   groundClear=0 #ground clearance
   #===============================   Blockchain Connection 
   #========= Times to Run
   timeToRun=0
   #------------------ Number of user
   nUsers="" #---For targetaed devices it is ip
   serverIp=""  #------ source system
   #------------------------ indicator
   ind=0
   #================== Policy indicators [Id of the policy owner owns]
   policyId=None
   balance=0
   old_balance=0

   def __init__(self,name,b_capacity,b_status,carRange,timeToRun,gClear,uadd,privKey,cadd,nUsers):
       self.vName=name
       self.EV_id=random.choice(range(1,1000)) #== randomly creating an EV
       self.b_capacity= b_capacity
       self.b_status=b_status
       self.carRange=carRange
       self.oneKm = (self.b_capacity/self.carRange)
       self.groundClear=gClear
       #====Connecting to blockchain
       #self.uAdd=uadd
       #self.privKey=privKey
       #self.cAdd=cadd
       #self.bc=Bconnect.Bc(uAdd,privKey,cAdd,gClear)
       #===object creation client
       result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
       output = result.stdout.strip()
       myIp=output.split()
       if len(myIp)==1:
         myIp=myIp[0]
       else:
         myIp=myIp[0]
       print("IP:",myIp)
       #------------------------reading server IP
       fhand = open('host.txt')
         # Loop through each line via file handler
       for line in fhand:
        self.serverIp=line.strip()

       print("Target IP:",self.serverIp)
    #    self.client=clientClass.Clients(self.serverIp,5051)
    #    msg=self.vName+" New Status:"+str(self.b_status)
    #    self.client.send(msg)
       #=======mongoDb
       #self.mdb=Transactions()
       #============CarAge
       self.carAge=random.randint(1,8) #Years
       #=====================Battery Age
       self.b_age=random.randint(0,7) #years
       while self.carAge<self.b_age:
           self.b_age=random.randint(0,7) #years
       #======================= User Type
       uValue=random.randint(0,3) #User Type
       self.userType=self.values[uValue][0]
       self.dailyDrive=self.values[uValue][1]
       #==================Distance Traveled
       if self.userType=="normal":
           self.distanceTraveled= (self.dailyDrive + random.randint(1000,3000))*self.carAge
       elif self.userType=="medium":
           self.distanceTraveled= (self.dailyDrive+ random.randint(3000,5000))*self.carAge
       elif self.userType=="heavy":
           self.distanceTraveled= (self.dailyDrive + random.randint(3000,7000))*self.carAge
       else:
           self.distanceTraveled= (self.dailyDrive + random.randint(3000,10000))*self.carAge
       #===================== Blockchain Connection
        #====Connecting to blockchain
       f=open('./abis/smartParking.json') #manually feeded
       abi=json.load(f)
       #print(abi): 172.16.68.105
       link= "HTTP://"+self.serverIp+":8545"
       #link= "HTTP://172.16.68.105:8545"
       #self.w3=Web3(Web3.HTTPProvider('HTTP://127.0.0.1:8545'))
       self.w3=Web3(Web3.HTTPProvider(link))
       self.x=self.w3.is_connected()
       print("Blockchain Connection status....",self.x)
       #===Connecting to the network and getting first address
       #user_number=input("Enter user number:[2-9]")
       #self.address1=self.w3.eth.accounts[int(user_number)]
       self.uAdd=Web3.to_checksum_address(uadd)
       self.privKey=privKey
       print("Your address:",self.uAdd)
       print("Your balance:",self.w3.eth.get_balance(self.uAdd))
        #===============================Setting default account
       self.w3.eth.default_account=self.uAdd
       #=====To communicate to a contract we need 1)Contract address 2)contract abi
       self.cAdd=Web3.to_checksum_address(cadd)
       #========= instantiating contract through the contract address
       self.newContract=self.w3.eth.contract(address=self.cAdd,abi=abi)
       #============== Times to Run
       self.timeToRun = timeToRun
       #---------------------------------
       self.nUsers=nUsers
       self.timesToDriveEv() #---------running vehicle
    
   def getGasConsumed(self,functionName,tx):
       receipt = self.w3.eth.wait_for_transaction_receipt(tx)
       gas_used = receipt['gasUsed']
       print("Function:",functionName,"Gas used:",gas_used)




#==================================== Server settings
   def serverConnection(self,msg):
       result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
       output = result.stdout.strip()
       myIp=output.split()
       if len(myIp)==1:
         myIp=myIp[0]
       else:
         myIp=myIp[0]
       print("IP:",myIp)
       #------------------------reading server IP
       fhand = open('host.txt')
         # Loop through each line via file handler
       for line in fhand:
        self.serverIp=line.strip()

       print("Target IP:",self.serverIp)
       self.client=clientClass.Clients(self.serverIp,5051)
       print("Server Ip:",self.serverIp)
       if(msg=="Disconnect"):
           msg1="DISCONNECT_MESSAGE"
           self.client.send(msg1)
       else:
           msg1=self.vName+" New Status:"+str(msg)
       #self.client.send(msg1)


   def getGasConsumed(self,functionName,tx):
       receipt = self.w3.eth.wait_for_transaction_receipt(tx)
       gas_used = receipt['gasUsed']
       print("Function:",functionName,"Gas used:",gas_used)

    #======== To registering the vehicle with smart contract
    #---- need to cheack that this function can only be called once
   def evRegister(self):
       #record start time
        rs = self.newContract.functions.checkRegistration(self.uAdd).call()
        print("Result: ",rs)
        msg=""
        if(rs==True):
            print("Address already registered.")
        else:
            start = time.time()
            tx=self.newContract.functions.vehicleRegistration(self.uAdd,self.vName,self.b_capacity,self.groundClear).transact()
            #msg = fetch_transaction_revert_reason(Web3,self.newContract.functions.vehicleRegistration(self.uAdd,self.vName,self.b_capacity,self.groundClear).transact())
            end=time.time()
            exeTime=(end-start) * 10**3
            #print("Vehicle registration time :",(end-start) * 10**3, "ms")
            self.transactionDetails("evRegistration",exeTime,tx,0)
            #self.getGasConsumed("Registration",tx)
            #self.transactionRecorder("User registration",exeTime,tx,0)

   def toEther(self,value):
       return self.w3.from_wei(value,'ether')
       
   def info(self): #1
       print("Name:",self.vName)
       print("EV_id:",self.EV_id)
       print("Address:",self.uAdd)
       print("Balance:",self.toEther(self.w3.eth.get_balance(self.uAdd)))
       print("Contract Add:",self.cAdd)
       print("Contract balance:",self.toEther(self.w3.eth.get_balance(self.cAdd)))
       print("Battery Capacity:",self.b_capacity,"kWh")
       print("Battery Status:",self.b_status ,"kWh")
       print("Car Range: ",self.carRange,"Km")
       self.coverRange = floor((1/self.b_capacity)*self.b_status*self.carRange)
       print("Distance can go:",self.coverRange ,"Km")
 
   def canGo(self,dist): #Distance car can cover 2
       self.b_status=self.b_status-(dist*self.oneKm)
       self.coverRange = floor(((1/self.b_capacity)*self.b_status*self.carRange))
       #print(">>",self.coverRange)
       return int(self.coverRange)
 
 
   def drive(self): #it will drive the car 3
       #d=self.canGo(0)
       
       print("---Driving----")
       if(self.b_status>2):   
           dist=random.randint(5,self.coverRange)
           console=Console()
           with console.status("[bold green]Driving car...") as status:
               sleep(1)
           print("Distance traveled:",dist,"Km")
           print("Can go:",self.canGo(dist),"Km")
           print("Battery Status:",self.b_status,"kWh")
           print("--------------")
           #self.info()
       else:
           print("Not enough charge!!")
           time.sleep(random.randint(3,7))
           self.chargeCar()
           time.sleep(random.randint(2,8))
           self.parkingAllocation()
           time.sleep(random.randint(2,6))
           self.vehicleParked()
           time.sleep(random.randint(2,7))
           self.parkingStatusUpdate()
           time.sleep(random.randint(2,7))
           self.paymentSettlement()
           print("=====================")
           self.info()

#---------------- Getting the smart parking status
   def parkingAddress(self):
       parkingList=[]
       try:
           parkingList=self.newContract.functions.parkingId(0).call()
           print("Parking address:",parkingList)
       except Exception as e:
           print("Unable to get Smart Parking address...",e)
       return parkingList

   #=============== Parking slot availability 
   def parkingSlotAvailability(self,parkingAddress):
       try:
           parkingDetails=self.newContract.functions.sParking(parkingAddress).call()
           print("Parking address:",parkingDetails)
       except Exception as e:
           print("Unable to get Smart Parking Details...",e)
       return parkingDetails[3],parkingDetails[4]


       
#Request Creation: requestCreation
#uAdd
# Urgency Factor
# SoC
# demand/Supply
# role : uint8 [ ParkingOnly, Charging, Discharging]
   def chargeCar(self): #charging the car 4
       #difference between start end time in milli. secs
    #    start = time.time()
    #    tx=Web3.toJSON(self.newContract.functions.vRegister(self.uAdd).call())
    #    end=time.time()
    #    #difference between start end time in milli. secs
    #    print("=======================================")
    #    print("Charging request time :",(end-start) * 10**3, "ms")
    #    print("Transaction hash:",tx)
       parkingAddress=self.parkingAddress()
       print("Parking address at calling:",parkingAddress)
       print("Checking charging slot availability")
       tx=""          
       demand=random.randint(5,floor(self.b_capacity-self.b_status))
       self.b_status=self.b_status+demand
       #difference between start end time in milli. secs
       time.sleep(random.randint(3,7))
       self.serverConnection(demand)       
       start = time.time()

       #=========== Waiting loop
       go=0
       while go!=1:
           capacity,occupied=self.parkingSlotAvailability(parkingAddress)
           availableSlot=capacity-occupied
           print("Capacity=",capacity,"and Occupied=",occupied,"and Available=",availableSlot)
           if availableSlot>2:
               go=1
               try:
                   tx=self.newContract.functions.requestCreation(parkingAddress,2,floor(self.b_status),demand,1).transact()
               except Exception as e:
                   print("Unable to create parking request..",e)
           else:
               print("Waiting for charging slot...")
               time.sleep(random.randint(3,7))
        
      
       end=time.time()
       #difference between start end time in milli. secs
       print("=======================================")
       exeTime=(end-start) * 10**3
       #print("Vehicle registration time :",(end-start) * 10**3, "ms")
       self.transactionDetails("requestCreation",exeTime,tx, demand)
    #    receipt = self.w3.eth.getTransactionReceipt(tx)
    #    print("Receipt:", receipt)
       #==To mongoDb
       #Transactions.saveTransaction(self.uAdd,self.vName,self.b_capacity,demand,demand,10,tx)
       with Progress() as progress:
           task1=progress.add_task("[red]Charging..",total=self.b_status)
           while not progress.finished:
               progress.update(task1,advance=0.10)
               sleep(0.02)
       print("Charged....",demand)


   def parkingAllocation(self):
       #record start time
       start = time.time()
       try:
           tx=self.newContract.functions.parkingLotAllocation(self.uAdd).transact()
       except Exception as e:
           print("Unable to allocate parking lot..",e)
       end=time.time()
       #difference between start end time in milli. secs
       print("=======================================")
       exeTime=(end-start) * 10**3
       #print("Vehicle parked :",(end-start) * 10**3, "ms")
       print("Vehicle parking allocated ")
       self.transactionDetails("parkingAllocation",exeTime,tx,0)

   def vehicleParked(self):
       #record start time
       start = time.time()
       tx=self.newContract.functions.vehicleParked(self.uAdd,120).transact()
       end=time.time()
       #difference between start end time in milli. secs
       print("=======================================")
       exeTime=(end-start) * 10**3
       #print("Vehicle registration time :",(end-start) * 10**3, "ms")
       print("Vehicle parked ")
       self.transactionDetails("vehicleParked",exeTime,tx,0)



   def parkingStatusUpdate(self):
       #record start time
       start = time.time()
       tx=self.newContract.functions.vehicleParkingStatusUpdate(self.uAdd,floor(self.b_status)).transact()
       end=time.time()
       #difference between start end time in milli. secs
       print("=======================================")
       exeTime=(end-start) * 10**3
       #print("Vehicle registration time :",(end-start) * 10**3, "ms")
       self.transactionDetails("parkingStatusUpdate",exeTime,tx,0)

   def paymentSettlement(self):
       parkingAddress=self.parkingAddress()       
       #===================Reading policy buying
       start = time.time()       
       #record start time
       transaction = self.newContract.functions.paymentSettlement(parkingAddress).build_transaction({
       'from': self.uAdd,
       'value': self.w3.to_wei(5, 'ether'),  # Amount of Ether to deposit (in wei)
       'gas': 2000000,  # Adjust the gas limit as needed
       'gasPrice': self.w3.to_wei('50', 'gwei'),  # Adjust the gas price as needed
       'nonce': self.w3.eth.get_transaction_count(self.uAdd),
       })

       # Sign the transaction
       signed_txn = self.w3.eth.account.sign_transaction(transaction, self.privKey)

        # Send the transaction
       try:
           tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
           end=time.time()
           #print("Buying policy:",(end-start) * 10**3, "ms")
           self.serverConnection("Disconnect")
       except Exception as e:
           print("Error in payment settelment.",e)
       
       # Wait for the transaction to be mined
       #tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
       #print("Transaction receipt:", tx_receipt)
       #self.getGasConsumed("Buying policy",tx_hash)
       exeTime=(end-start) * 10**3
       print("Payment Settelment Completed..")
       bal=self.w3.eth.get_balance(self.uAdd)
       print("Vehicle balance:",self.w3.from_wei(bal,'ether'))

       self.transactionDetails("paymentSettlement",exeTime,tx_hash,0)


    #============================ for getting transaction details [ Normal File]
#    def transactionDetails(self,funcName,exeTime,tx):
#        fPath="results"+str(self.nUsers)
#        data=self.w3.eth.wait_for_transaction_receipt(tx)
#        if funcName=="evRegistration":
#            fPath=fPath+"/evRegistration.txt"
#        elif funcName=="requestCreation":
#            fPath=fPath+"/requestCreation.txt"
#        elif funcName=="parkingAllocation":
#            fPath=fPath+"/parkingAllocation.txt"
#        elif funcName=="vehicleParked":
#            fPath=fPath+"/vehicleParked.txt"
#        elif funcName=="parkingStatusUpdate":
#            fPath=fPath+"/parkingStatusUpdate.txt"
#        else: #funcName=="paymentSettlement"
#            fPath=fPath+"/paymentSettlement.txt"
        
#        with open(fPath, 'a') as f:
#           print(funcName,",",data['from'],",",data['to'],",",exeTime,",",data['gasUsed'], file=f)


       #============================ for getting transaction details [ CSV ]
   def transactionDetails(self,funcName,exeTime,tx,demand):
       #fPath="results/results"+str(self.nUsers)
       fPath="results"
       fPath1=fPath+"/allTransactions.csv"
       data=self.w3.eth.wait_for_transaction_receipt(tx)
       if funcName=="evRegistration":
           fPath=fPath+"/evRegistration.csv"
       elif funcName=="requestCreation":
           #================================================ Recording the EV demands
           chargingDemand=fPath+"/chargingDemand.csv"
           with open(chargingDemand, 'a') as f:
               print(funcName,",",data['from'],",",data['to'],",",exeTime,",",data['gasUsed'],",",demand, file=f)
           fPath=fPath+"/requestCreation.csv"
       elif funcName=="parkingAllocation":
           fPath=fPath+"/parkingAllocation.csv"
       elif funcName=="vehicleParked":
           fPath=fPath+"/vehicleParked.csv"
       elif funcName=="parkingStatusUpdate":
           fPath=fPath+"/parkingStatusUpdate.csv"
       else: #funcName=="paymentSettlement"
           fPath=fPath+"/paymentSettlement.csv"
        
       with open(fPath, 'a') as f:
          print(funcName,",",data['from'],",",data['to'],",",exeTime,",",data['gasUsed'], file=f)
       
       #========================== All Transactions in a file
       with open(fPath1,'a') as f:
           if demand !=0:
               print(funcName,",",data['from'],",",data['to'],",",exeTime,",",data['gasUsed'], file=f)
           else:
               print(funcName,",",data['from'],",",data['to'],",",exeTime,",",data['gasUsed'],",",demand, file=f)
           
     
           
    #    with open('file.txt', 'a') as f:
    #        print(funcName,",",data['from'],",",data['to'],",",exeTime,",",data['gasUsed'], file=f)
    #        #print(funcName,",",data['transactionHash'],",",data['from'],",",data['to'],",",exeTime,",",data['gasUsed'], file=f)
    #        if self.ind == 0:
        #     print("Function ","| Transaction hash ","| from ","| to ","| execution time ","| Gas Used ")
        #     print(funcName,",",data['transactionHash'],",",data['from'],",",data['to'],",",exeTime,",",data['gasUsed'], file=f)
        #    else:
        #     print(funcName,",",data['transactionHash'],",",data['from'],",",data['to'],",",exeTime,",",data['gasUsed'], file=f)
            
           
       #print("Transaction details:", self.w3.eth.get_transaction_receipt(tx))
 
       #print("Transaction hash:",data)
       #print("Function:",funcName,"Transaction hash:",data['transactionHash'],"from: ",data['from'],"to: ",data['to'],"execution time:",exeTime,"ms","Gas Used:",data['gasUsed'])
   
   def writeToTextFile(self):
        # Append to file using the write() method
        with open('file.txt', 'a') as f:
            f.write('I am appended text\n')
       

    #Number of times the EV will be drive
   def timesToDriveEv(self):
       self.info()
       self.evRegister()
       print("Drive:", self.timeToRun)
       while(self.timeToRun>0):
           self.drive()
           self.timeToRun-=1
       #------------------------ Terminates the program[ Comment it if you want to see results]    
       exit() 




# #================= Running Section
# obj.info()
# obj.evRegister()
# print("Driving Times:",a1[3])
# rep=a1[3] #number of times to drive
# while(rep>0):
# obj.drive()
# rep=rep-1
# Print("Driving Times:",rep)