"""
Connecting to the ganache running on server

"""
import subprocess
#Web3 connection
from web3 import Web3
import os
# Get the file handler
fhand = open('host.txt')
ip=""
# Loop through each line via file handler
for line in fhand:
  ip=line.strip()
link="HTTP://"+ip+":8545" 
print(link)
w3=Web3(Web3.HTTPProvider(link))
x=w3.is_connected()
print("Connection status....",x)