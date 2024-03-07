## Manual

## Virtual box network connection configuration
* It requires to change `Adapter 1` settings

## Environment for python
To activate the virtual environment be in the root directory
```bash
python3 -m venv myenv
source myenv/bin/activate
```

## Install Web3.py
* create an virtual environment
* then only `pip install web3`
* for rich.progress bar: `pip install rich`  
```
pip install --upgrade pip setuptools
```

## Need to create truffle config file



## Steps to run
* `Update_contract ABI`
* **all.sh** : to ger run permission for all files
* **genconfig.py** : to generate truffle config file

* Comment it [DONE]
```python
#MongoDB connection
from transaction import Transactions
```
* **IP Address** The ip address of the Ganache System
* **the server option** [ car.py]

## car.py
* **serverIp** : global variable for storing server ip

## ================ Resulting Files
>- No extra folder creation result will be written on results folder only
```python
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
```


## Check befor update
* **runCar.sh**: 
>- remove gnome-terminal
>- must start from python 
>- to send multiple values as argument to the python program use :
```python
Python hello.py --v 12 13 -c 23
```

## Uploading and downloading files 
* `Uploading` Secure Copy  
```bash
$scp -r <fileToCopy> <remoteDestination:location>
```
* `Downloading` Secure Copy  
```bash
$scp -r <remoteDestination:location> <locationToStore> 
```

* **SSH with other ports**
```bash
scp -P 4422 -r clientSystem -p 4422 b22@localhost:.
```

```bash
$ssh -p 4422 b22@localhost
```
