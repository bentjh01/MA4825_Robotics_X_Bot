import rospy
from MotorClass import AX1xA
from Configuration import Config
from dynamixel_sdk import *
from xbot_msgs import dxl_position_msg

def callback(data): 
    global motors
    for motor in motors:
        if data.id == motor.ID:
            motor.set_position(data.goal)

def driver_node():
    global config
    rospy.init_node('driver_node')
    rospy.Subscriber(config.set_position_topic, dxl_position_msg, callback)
    rospy.spin()

def main():
    global config
    global motor_1, motor_2, motor_3, motor_4, motor_5, motors
    config = Config
    portHandler = PortHandler(config.device_name)

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

    # Initialise motors
    motor_1 = AX1xA("base_motor", 1, portHandler)
    motor_2 = AX1xA("motor2", 2, portHandler)
    motor_3 = AX1xA("motor3", 3, portHandler)
    motor_4 = AX1xA("motor4", 4, portHandler)
    motor_5 = AX1xA("motor5", 5, portHandler)

    motors = [motor_1, motor_2, motor_3, motor_4, motor_5]

    driver_node()
    
if __name__ == "__main__":
    main()