from dynamixel_sdk import *

from xbot_driver.src.xbot_driver.driver_configuration import Config
from xbot_driver.hardware_abstraction_layer import *

import rospy
from xbot_msgs.msg import AXState

class XBotDriver():
    def __init__(self): 
        self.config = Config()
        self.__init__dynamixel()
        self.__init__rospy()

    def __init__dynamixel(self):
        self.portHandler = PortHandler(self.config.device_name)

        # Open port
        try:
            self.portHandler.openPort()
            print("Succeeded to open the port")
        except:
            print("Failed to open the port")
            quit()

        # Set port baudrate
        try:
            self.portHandler.setBaudRate(self.config.baude_rate)
            print("Succeeded to change the baudrate")
        except:
            print("Failed to change the baudrate")
            quit()

        # Initialise motors
        self.motor_1 = AX1xA("joint_2", 1, self.portHandler)
        self.motor_2 = AX1xA("joint_1", 2, self.portHandler)
        self.motor_3 = AX1xA("joint_5", 3, self.portHandler)
        self.motor_4 = AX1xA("joint_3", 4, self.portHandler)
        self.motor_6 = AX1xA("joint_4", 6, self.portHandler)

        self.motors = [self.motor_2, self.motor_1, self.motor_4, self.motor_6, self.motor_3]

        for motor in self.motors:
            motor.set_torque_enabled(1)

    def __init__rospy(self):
        rospy.init_node('xbot_driver')
        self.cmd_state_subscriber = rospy.Subscriber('/open_loop_controller/cmd_state', AXState, self.cmd_state_callback)
        self.state_publish_rate = rospy.Rate(10)

    def cmd_state_callback(self, msg):
        for i, motor in self.motors:
            moving_speed = radian_second2uint10(msg.Moving_Speed[i])
            goal_position = radian2uint10(msg.Goal_Position[i])
            motor.set_moving_speed(moving_speed)
            motor.set_goal_position(goal_position)

    def main(self):
        print('Running')
        while not rospy.is_shutdown():
            self.cmd_state_subscriber
    
if __name__ == "__main__":
    xBotDriver = XBotDriver()
    xBotDriver.main()