// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

//Registring a vehicle
// Functions : 1) Parking initialization
// 2) Parking slot allocation
// 3) Charging payment
// 4) Transaction query

contract smartParking{


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
  uint capacity;
  uint pSlots; //---------nomuber of parking lots
}



//============================================
enum Status{Created, Waiting, Charging, Discharging,ParkingOnly,Completed}
enum Role{ParkingOnly, Charging, Discharging}
enum paymentStatus{NotPaid, Paid} //-------------- payment status
//======================= Parking Request
struct parkingReq{
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
function requestCreation(address _vAdd,uint _eFacter, uint _SoC, uint _demSup, Role _role) public {
   //require(vRegistere[_vAdd].vRegStatus == true,"Address not registered for request creation."); 
   require(req[_vAdd].st != Status.Waiting || req[_vAdd].st != Status.Charging|| req[_vAdd].st != Status.Discharging,"Request already exist");
   //Role _r=_role;
    req[_vAdd]=parkingReq(_vAdd,_eFacter,_SoC,_demSup,0,Status.Waiting,_role,0,0,0,paymentStatus.NotPaid);
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
function paymentSettlement(address _vAdd) public {
  require(req[_vAdd].st == Status.Completed, "Charging or Discharging not completed");
  require(req[_vAdd].payStatus == paymentStatus.NotPaid, "Already paid");
  req[_vAdd].payStatus = paymentStatus.Paid;
  //req[_vAdd].st=Status.Created;
}


} //End of contract
  