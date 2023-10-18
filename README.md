# MA4825_Robotics_X_Bot
This repo is for the course project MA4825 Robotics


## Setup
### U2D2 Setup
- Allows serial communication to U2D2 device. 
#### Linux
[ROBOTIS U2D2 eManual](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/device_setup/#controller)
#### Udev rules configuration
\$ `wget https://raw.githubusercontent.com/ROBOTIS-GIT/dynamixel-workbench/master/99-dynamixel-workbench-cdc.rules`  
\$ `sudo cp ./99-dynamixel-workbench-cdc.rules /etc/udev/rules.d/`  
\$ `sudo udevadm control --reload-rules`  
\$ `sudo udevadm trigger`
#### Check USB Port
1. Check device discovered  
\$ `lsusb | grep FT232H`
2. Check device port  
\$ `ls /dev/ttyUSB*`
### ROS
[ROS Wiki Noetic Installation](http://wiki.ros.org/noetic/Installation/Ubuntu)
#### Dynamixel Workbench
- [ROBOTIS Dynamixel Workbench eManual](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_workbench/)
- [GitHub Dynamixel Workbench](https://github.com/ROBOTIS-GIT/dynamixel-workbench.git)    
#### Dynamixel SDK
- [ROBOTIS Dynamixel SDK eManual](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/)
- [GitHub Dynamixel SDK](https://github.com/ROBOTIS-GIT/DynamixelSDK.git)  
\$ `sudo apt install ros-noetic-dynamixel-sdk`

