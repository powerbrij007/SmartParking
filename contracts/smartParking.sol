// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

//Registring a vehicle
// Functions : 1) Parking initialization
// 2) Parking slot allocation
// 3) Charging payment
// 4) Transaction query

contract smartParking{


//------------ contract balance
uint256 public contractBalance;
//============ Receive funds
// Function to allow deposit of Ether
receive() external payable {
    contractBalance += msg.value;
    //investors[msg.sender].invested_amt+=msg.value;
    //emit Deposit(msg.sender, msg.value);
    //policyHolder[_uAdd][_evid].premium=msg.value;
}


//------------------- Vehicle Section

struct vehicleRsg{
    address vAdd;
    string vName;
    uint capacity;
    uint gClearance;
    bool vRegStatus;  //======= default value of boolean in false

}
mapping(address=>vehicleRsg) public vRegistere;
//address[] public vehicleRegistered;
//=========== Vehicle Mapping
//mapping(uint=>address) public vAdd;

function vehicleRegistration(address _vAdd, string memory _vName, uint _capacity, uint _gClear ) public {
   //vehicleRsg memory = vRegistere[_vAdd];
   require(vRegistere[_vAdd].vAdd !=_vAdd, "Address exist can not be register twice!");
   vRegistere[_vAdd]= vehicleRsg(_vAdd, _vName, _capacity, _gClear,true);
   //vehicleRegistered.push(_vAdd);
}

function checkRegistration(address _vAdd) view public returns(bool){
  return vRegistere[_vAdd].vRegStatus;
}
//===================getting info
//function getVehicle(address _vAdd) public returns(address[] memory){
//  return vRegistere[_vAdd];
//}

//parking slot
enum Slot{Available, Occupied}
//========================Parking information
struct parking{
  address pAdd;
  uint256 available; //--- charge available
  uint256 capacity;
  uint256 pSlots; //---------nomuber of parking lots
  uint256 ocuupied;
}

mapping(address=>parking) public sParking;
mapping(uint=>address) public parkingId;
uint256 pid;
//================================================== Parking Registration
function registerParking(uint256 _available,uint256 _capacity, uint256 _pSlots) public {
    sParking[msg.sender]=parking(msg.sender,_available, _capacity,_pSlots,0);
    parkingId[pid]=msg.sender;
    pid+=1;
}

//----------------- updating power [ While calling from request creation the address of parking is required
function updateParking(uint256 _available,uint256 _operation, address _pAdd) public{
    if(_operation==1){
        sParking[msg.sender].available+=_available; //---Supplied
    }else{
        sParking[_pAdd].available-=_available; //------ demanded
    }
}

//============================================
enum Status{Created, Waiting, Charging, Discharging,ParkingOnly,Completed}
enum Role{ParkingOnly, Charging, Discharging}
enum paymentStatus{NotPaid, Paid} //-------------- payment status
//======================= Parking Request
struct parkingReq{
  address pAdd; //-------- address of parking
  address vAdd; //== Parked vehicle
  uint eFacter; //----------- urgency factor [0,....1]
  uint SoC; //--------- State of Charge
  uint demSup; //------- Demand or supply
  uint proCharge; //provided charge [ 0: in case of discharge, parking only, amt: charging]
  Status st;
  Role role;
  uint aSlot; //-- allocated slot
  uint adjGclear; //---- Adjusted height
  uint paymentAmt;//======= payable amount for request
  paymentStatus payStatus;

}
//================mapping
mapping(address=>parkingReq) public req; //============ request mapping
//=============== Creating request
function requestCreation(address _parkingAdd, uint _eFacter, uint _SoC, uint _demSup, Role _role) public {
   //require(vRegistere[_vAdd].vRegStatus == true,"Address not registered for request creation."); 
   require(req[msg.sender].st != Status.Waiting || req[msg.sender].st != Status.Charging|| req[msg.sender].st != Status.Discharging,"Request already exist");
   //Role _r=_role;
   require(sParking[_parkingAdd].ocuupied!=sParking[_parkingAdd].pSlots,"No slots available");
   req[msg.sender]=parkingReq(_parkingAdd, msg.sender,_eFacter,_SoC,_demSup,0,Status.Waiting,_role,0,0,0,paymentStatus.NotPaid);
   sParking[_parkingAdd].ocuupied+=1;
   updateParking(_demSup,0,_parkingAdd); //------- supply
    } //=========function end
 
//============function check request
function checkReq(address _vAdd) view public returns(Status){
  return req[_vAdd].st;
}

//=========== Parking slot allocation [ allocate the parking spot and adjGclear ]
function parkingLotAllocation(address _vAdd) public {
  //require(req[_vAdd].vAdd == _vAdd, "Address not registered: Parking Allocation"); 
  require((req[_vAdd].st != Status.Charging || req[_vAdd].st != Status.Discharging || req[_vAdd].st != Status.Completed) , "Parking lot already alloted"); //============ Vehicle registered but waiting for parking lot
    if(req[_vAdd].role == Role.Charging){
           req[_vAdd].st=Status.Charging;
    } else if (req[_vAdd].role == Role.Discharging){
           req[_vAdd].st=Status.Discharging;
    }else{
      req[_vAdd].st=Status.ParkingOnly;
    }
  
}
//==================Vehicle Parked [ On parking lot ]
function vehicleParked(address _vAdd, uint _adjGclear) public {
     if(req[_vAdd].role == Role.Charging){
           req[_vAdd].st=Status.Charging;
           req[_vAdd].adjGclear= _adjGclear; //====== Updating the adjusted height
    } else if (req[_vAdd].role == Role.Discharging){
           req[_vAdd].st=Status.Discharging;
           req[_vAdd].adjGclear= _adjGclear; //====== Updating the adjusted height
    }else{
      req[_vAdd].st=Status.ParkingOnly;
    }
}

//-------------------------------------------- To update vehicle status after charging or discharging
function vehicleParkingStatusUpdate(address _vAdd, uint _proCharge) public {
  if(req[_vAdd].role == Role.Charging){
           req[_vAdd].st=Status.Completed;
           req[_vAdd].proCharge=_proCharge;
    } else if (req[_vAdd].role == Role.Discharging){
           req[_vAdd].st=Status.Completed;
           req[_vAdd].proCharge=_proCharge;
    }
    //req[_vAdd].payStatus = paymentStatus.NotPaid;
}

//===============Payment and reques settelment
function paymentSettlement(address payable _parkingAdd) public payable{
  require(req[msg.sender].st == Status.Completed, "Charging or Discharging not completed");
  require(req[msg.sender].payStatus == paymentStatus.NotPaid, "Already paid");
  req[msg.sender].payStatus = paymentStatus.Paid;
  sParking[_parkingAdd].ocuupied-=1;
  //req[_vAdd].st=Status.Created;
  _parkingAdd.transfer(msg.value);

}


} //End of contract
  