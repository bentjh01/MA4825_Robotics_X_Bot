import math
import rospy
from xbot_msgs.msg import AX
from sensor_msgs.msg import JointState

## ros moveit
##

def bit2deg(bit):
    deg = (bit/1023 * 296.67) - 296.67/2
    return deg

def deg2bit(deg):
    bit = (deg+296.67/2)/296.67 * 1023
    return int(bit)

def rad2bit(rad):
    deg = rad/math.pi *180 
    return deg2bit(deg)

def callback(msg):
    for i, name in enumerate(msg.name):
        data_list[i] = msg.position[i]

def state_callback(msg):
    motor_moving = bool(msg.Moving)

def main():
    global data_list, motor_moving
    data_list = [0, 0 , 0, 0 ,0]
    motor_moving = False

    rospy.init_node('test')
    publisher = rospy.Publisher('/set_position', AX, queue_size=10)
    subsciber = rospy.Subscriber('/joint_states', JointState, callback)
    motor_subscriber = rospy.Subscriber('/motor_states', AX, state_callback)
    rate = rospy.Rate(0.2)
    count = 0
    last_time = rospy.get_time()
    last_state = [0]
    while not rospy.is_shutdown():
        msg_1 = AX()
        msg_2 = AX()
        msg_3 = AX()
        msg_4 = AX()
        msg_6 = AX()

        msg_1.ID = 1
        msg_1.Goal_Position = 512
        msg_1.Moving_Speed = 64
        msg_1.LED = True

        msg_2.ID = 2
        msg_2.Goal_Position = 512
        msg_2.Moving_Speed = 64
        msg_1.LED = True

        msg_3.ID  = 3
        msg_3.Goal_Position = 512
        msg_3.Moving_Speed = 64
        msg_1.LED = True

        msg_4.ID  = 4
        msg_4.Goal_Position = 512
        msg_4.Moving_Speed = 64
        msg_1.LED = True

        msg_6.ID  = 6
        msg_6.Goal_Position = 512
        msg_6.Moving_Speed = 64
        msg_6.LED = True

        publisher.publish(msg_1)
        publisher.publish(msg_2)
        publisher.publish(msg_3)
        publisher.publish(msg_4)
        publisher.publish(msg_6)

        motor_subscriber
        rate.sleep()

if __name__ == '__main__':
    main()