# MA4825_Robotics_X_Bot
This repo is for the course project MA4825 Robotics

## Running the code
1. Opening the workspace  
`cd /home/$USER/Documents/xbot_ws`
3. Sourcing ROS environment  
`source /opt/ros/noetic/setup.bash`
5. Sourcing workspace environment  
`source devel/setup.bash`
7. Starting roscore  
`roscore`
9. Startig communications with Dynamixel Motors  
`rosrun xbot_driver driver.py`
11. Starting controller  
`python3 src/MA4825_Robotics_X_Bot/xbot_control/src/open_loop_controller.py`
13. Starting Kinematics  
`python3 src/MA4825_Robotics_X_Bot/xbot_kinematics/src/manual_kinematics`
15. Receiving data from sensors  
`rosrun xbot_sensors limit_switch.py`

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
### ROS Setup
[ROS Wiki Noetic Installation](http://wiki.ros.org/noetic/Installation/Ubuntu)
#### Dynamixel Workbench
- [ROBOTIS Dynamixel Workbench eManual](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_workbench/)
- [GitHub Dynamixel Workbench](https://github.com/ROBOTIS-GIT/dynamixel-workbench.git)    
#### Dynamixel SDK
- [ROBOTIS Dynamixel SDK eManual](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/)
- [GitHub Dynamixel SDK](https://github.com/ROBOTIS-GIT/DynamixelSDK.git)  
\$ `sudo apt install ros-noetic-dynamixel-sdk`
#### Moveit
- [ROS MoveIt Tutorials](https://ros-planning.github.io/moveit_tutorials/)
### Jetson Xavier GPIO Setup
- [GitHub Jetson GPIO](https://github.com/NVIDIA/jetson-gpio.git)

