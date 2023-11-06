# MA4825_Robotics_X_Bot
This repo is for the course project MA4825 Robotics
## Startup

## Setup
### NVIDIA Jetson Xavier Dev Kit
#### GPIO Setup
[JETSON XAVIER NX DEVELOPER USER GUIDE](https://developer.download.nvidia.com/assets/embedded/secure/jetson/Xavier%20NX/Jetson_Xavier_NX_Developer_Kit_User_Guide.pdf?d37pwh1FXwVQGgBHs5bdTTzLxJcKNdnP58PVVUkszH-OpMg5bhL1fHhMKovpBBUnjWhk27ThlrJzPGtwH-csR4IUpyZ7992O9uV5qbPU4Vv2duIpsFw3flSfqbg_eEFT_RfcVIE6L8WGxAOqJubo-9HeM9l8WOg1WuiX6uQp8ycUCu8sdrfxi6hSYdbpCKtjD4gJ7ZiS&t=eyJscyI6ImdzZW8iLCJsc2QiOiJodHRwczovL3d3dy5nb29nbGUuY29tLyJ9)
##### Installation 
```sudo pip install Jetson.GPIO```


### Dynamixel Motors
#### U2D2 Setup
- Allows serial communication to U2D2 device. 
##### Linux
[ROBOTIS U2D2 eManual](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/device_setup/#controller)
##### Udev rules configuration
\$ `wget https://raw.githubusercontent.com/ROBOTIS-GIT/dynamixel-workbench/master/99-dynamixel-workbench-cdc.rules`  
\$ `sudo cp ./99-dynamixel-workbench-cdc.rules /etc/udev/rules.d/`  
\$ `sudo udevadm control --reload-rules`  
\$ `sudo udevadm trigger`
##### Check USB Port
1. Check device discovered  
\$ `lsusb | grep FT232H`
2. Check device port  
\$ `ls /dev/ttyUSB*`
#### ROS
[ROS Wiki Noetic Installation](http://wiki.ros.org/noetic/Installation/Ubuntu)
##### Dynamixel Workbench
- [ROBOTIS Dynamixel Workbench eManual](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_workbench/)
- [GitHub Dynamixel Workbench](https://github.com/ROBOTIS-GIT/dynamixel-workbench.git)    
##### Dynamixel SDK
- [ROBOTIS Dynamixel SDK eManual](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/)
- [GitHub Dynamixel SDK](https://github.com/ROBOTIS-GIT/DynamixelSDK.git)  
\$ `sudo apt install ros-noetic-dynamixel-sdk`

