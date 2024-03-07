module.exports = {
    networks: {
    development: {
    host: "192.168.117.64",   
    port: 8545,            
    network_id: "*",       
    },
  },
  mocha: {
    // timeout: 100000
  },
  // Configure your compilers
  compilers: {
    solc: {
      version: "0.8.10",   
    } 
  },
};