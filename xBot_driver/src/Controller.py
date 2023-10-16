"""
1. receives input of goal position. 
2. Calculates point paths to goal postion within space constraints
3. creates list of points on path from dynamic contraints e.g. acceleration etc
4. outputs a dictionary of {ID:position} at a publish rate
5. receives completed flag
6. checks position within tolerance
7. moves again to go to goal 
"""

from MotorClass import AX1xA
from Configuration import Config

from dynamixel_sdk import *
# from dynamixel_sdk_examples.srv import *
# from dynamixel_sdk_examples.msg import *

config = Config

portHandler = PortHandler(config.device_name)
packetHandler = PacketHandler(config.protocol_version)

# Open port
try:
    portHandler.openPort()
    print("Succeeded to open the port")
except:
    print("Failed to open the port")
    quit()

# Set port baudrate
try:
    portHandler.setBaudRate(config.baude_rate)
    print("Succeeded to change the baudrate")
except:
    print("Failed to change the baudrate")
    quit()

motor_1 = AX1xA("base_motor", 1, portHandler, packetHandler)
motor_2 = AX1xA("motor2", 2, portHandler, packetHandler)
motor_3 = AX1xA("motor3", 3, portHandler, packetHandler)
motor_4 = AX1xA("motor4", 4, portHandler, packetHandler)
motor_5 = AX1xA("motor5", 5, portHandler, packetHandler)

