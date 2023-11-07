#!/usr/bin/env python
import rospy
from xbot_msgs.msg import AX

def motor_states_callback(msg):
    # Callback function to process the received motor state messages
    motor_id = msg.ID
    present_position = msg.Present_Position
    # Do something with the motor position data
    print(f"Motor {motor_id} - Present Position: {present_position}")

def motor_states_subscriber():
    # Initialize the ROS node
    rospy.init_node('motor_states_subscriber')

    # Create a subscriber for the /motor_states topic
    rospy.Subscriber('/motor_states', AX, motor_states_callback)

    # Spin to keep the script running and processing messages
    rospy.spin()

if __name__ == "__main__":
    motor_states_subscriber()
