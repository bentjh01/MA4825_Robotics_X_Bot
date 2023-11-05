import rospy
from xbot_driver.MotorClass import AX1xA
from xbot_driver.Configuration import Config
from dynamixel_sdk import *
from xbot_msgs.msg import AX

class XBotDriver():
    def __init__(self): 
        self.config = Config()
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
        self.motor_1 = AX1xA("motor_1", 1, self.portHandler)
        self.motor_2 = AX1xA("motor_2", 2, self.portHandler)
        self.motor_3 = AX1xA("motor_3", 3, self.portHandler)
        self.motor_4 = AX1xA("motor_4", 4, self.portHandler)
        # self.motor_5 = AX1xA("motor_5", 5, self.portHandler)
        self.motor_6 = AX1xA("motor_6", 6, self.portHandler)

        self.motors = [self.motor_1, self.motor_2, self.motor_3, self.motor_4, self.motor_6]

        for motor in self.motors:
            motor.set_torque_mode(True)

        rospy.init_node('xbot_driver')
        self.state_publisher = rospy.Publisher('/motor_states', AX, queue_size=10)
        self.set_position_subscriber = rospy.Subscriber('/set_position', AX, self.set_position_callback)
        self.state_publish_rate = rospy.Rate(10)

    def set_position_callback(self, msg):
        for motor in self.motors:
            if msg.ID == motor.ID and not motor.get_moving():
                motor.set_moving_speed(msg.Moving_Speed)
                motor.set_goal_position(msg.Goal_Position)
                motor.set_led(msg.LED)

    def motor_state_update(self):
        for motor in self.motors:
            msg = AX()
            id = motor.ID
            present_position = motor.get_position()
            moving = motor.get_moving()
            msg.ID = id
            msg.Present_Position = present_position
            msg.Moving = moving
            self.state_publisher.publish(msg)
        self.state_publish_rate.sleep()

    def main(self):
        print('Running')
        while not rospy.is_shutdown():
            self.set_position_subscriber
            # self.motor_state_update()
    
if __name__ == "__main__":
    xBotDriver = XBotDriver()
    xBotDriver.main()