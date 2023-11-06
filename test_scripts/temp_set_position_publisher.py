import math
import rospy
from xbot_msgs.msg import AX
from sensor_msgs.msg import JointState
from std_msgs.msg import String

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
    global data_list
    data = msg.data[1:-1].split(',')
    for i, val in enumerate(data):
        data[i] = float(val)
    data_list = data

def state_callback(msg):
    motor_moving = bool(msg.Moving)

def main():
    global data_list, motor_moving
    data_list = [0, 0 , 0, 0 ,0]
    motor_moving = False

    rospy.init_node('test')
    publisher = rospy.Publisher('/set_position', AX, queue_size=10)
    subsciber = rospy.Subscriber('/j_positions', String, callback)
    # subsciber_fake_controller = rospy.Subscriber('/move_group/fake_controller_joint_states', String, callback)
    motor_subscriber = rospy.Subscriber('/motor_states', AX, state_callback)
    rate = rospy.Rate(1)
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
        msg_1.Goal_Position = rad2bit(data_list[1])
        # msg_1.Goal_Position = 512
        msg_1.Moving_Speed = 64
        msg_1.LED = True

        msg_2.ID = 2
        msg_2.Goal_Position = rad2bit(data_list[0])
        # msg_2.Goal_Position = 512
        msg_2.Moving_Speed = 64
        msg_1.LED = True

        msg_3.ID  = 3
        msg_3.Goal_Position = rad2bit(data_list[4])
        # msg_3.Goal_Position = 512
        msg_3.Moving_Speed = 64
        msg_1.LED = True

        msg_4.ID  = 4
        msg_4.Goal_Position = rad2bit(data_list[2])
        # msg_4.Goal_Position = 512
        msg_4.Moving_Speed = 64
        msg_1.LED = True

        msg_6.ID  = 6
        msg_6.Goal_Position = rad2bit(data_list[3])
        # msg_6.Goal_Position = 512
        msg_6.Moving_Speed = 64
        msg_6.LED = True

        subsciber
        motor_subscriber

        publisher.publish(msg_1)
        publisher.publish(msg_2)
        publisher.publish(msg_3)
        publisher.publish(msg_4)
        publisher.publish(msg_6)

        rate.sleep()

if __name__ == '__main__':
    main()