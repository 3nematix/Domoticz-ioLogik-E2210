# Introduction
This code is for the Moxa ioLogik E2210 controller and domoticz.
This code gets INPUT/OUTPUT status (On, Off) and sends the data through API to domoticz smart home system.
# Usage
Firstly launch the main.py, it is the main code to get/send info from moxa to domoticz client.
domoticz_control/main.py file is for updating device output status (ON,Off).

To update the device through domoticz_control/main.py, you should use these parameters which are below.
```
  python3 main.py IP(192.168.1.220) RELAY_NUMBER(1,32) RELAY_STATUS(0,1)
```
# Compatibility for other devices
If you would like to use another device from the same series you should change some functions which are used as numbers (Input/Output relay quantity) and some variables and you should be good to go.
