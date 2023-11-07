from dynamixel_sdk import *

from xbot_driver.src.xbot_driver.driver_configuration import Config
from xbot_driver.hardware_abstraction_layer import *
from xbot_driver.motor_class import AX1xA

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
        # self.motor_5 = AX1xA("motor_5", 5, self.portHandler)
        self.motor_6 = AX1xA("joint_4", 6, self.portHandler)

        self.motors = {2:self.motor_2, 1:self.motor_1, 4:self.motor_4, 6:self.motor_6, 3:self.motor_3}

    def __init__rospy(self):
        node_name = 'xbot_driver'
        controller_name = 'xbot_simple_controller'
        rospy.init_node(node_name)
        self.state_publisher = rospy.Publisher(f'/{node_name}/motor_states', AXState, queue_size=10)
        self.cmd_state_subscriber = rospy.Subscriber(f'/{controller_name}/cmd_state', AXState, self.cmd_state_callback)
        self.state_publish_rate = rospy.Rate(10)

    def cmd_state_callback(self, msg):
        for i, ID in enumerate(msg.ID):
            motor = self.motors[ID]
            moving_speed = radian2uint10(msg.Moving_Speed[i])
            goal_position = radian2uint10(msg.Goal_Position[i])
            led_enabled = int(msg.LED[i])
            torque_enabled = int(msg.Torque_Enable[i])
            motor.set_moving_speed(moving_speed)
            motor.set_goal_position(goal_position)
            motor.set_led_enabled(led_enabled)
            motor.set_torque_enabled(torque_enabled)

    def motor_state_update(self):
        msg = AXState()
        for i, motor in enumerate(self.motors.values()):
            msg.name[i] = motor.motor_name
            msg.ID[i] = motor.ID
            msg.LED[i] = motor.led_enabled
            msg.Torque_Enable[i] = motor.torque_enabled
            msg.Model_Number[i] = motor.model_number
            msg.Baud_Rate[i] = motor.baude_rate
            msg.Goal_Position[i] = uint102radian(motor.goal_position)
            present_position = uint102radian(motor.get_position())
            moving = bool(motor.get_moving_status())
            msg.Present_Position[i] = present_position
            msg.Moving[i] = moving
        self.state_publisher.publish(msg)
        self.state_publish_rate.sleep()

    def main(self):
        print('Running')
        while not rospy.is_shutdown():
            self.cmd_state_subscriber
            self.motor_state_update()
    
if __name__ == "__main__":
    xBotDriver = XBotDriver()
    xBotDriver.main()