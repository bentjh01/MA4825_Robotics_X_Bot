import math
import rospy
from xbot_msgs.msg import AX
from sensor_msgs.msg import JointState
from std_msgs.msg import String
import sys

def bit2deg(bit):
    deg = (bit/1023 * 296.67) - 296.67/2
    return deg

def deg2bit(deg):
    bit = (deg+296.67/2)/296.67 * 1023
    return int(bit)

def rad2bit(rad):
    deg = rad/math.pi *180 
    return deg2bit(deg)

def bit2rad(bit):
    deg = bit2deg(bit)
    return deg/180 * math.pi

def get_angular_speed(dtheta, time):
    speed = dtheta/time
    return speed

def angular_speed_to_byte(angular_speed):
    # 0.111 [rad/min/count] == 0.00185 [rad/s/count]
    return int(abs(angular_speed)//0.00185)

class Motor():
    def __init__(self, ID):
        self.ID = ID
        self.goal_position = 0
        self.current_position = 0
        self.move_complete = True # zero == completed
        self.speed = 64

def callback(msg):
    global m1, m2, m3, m4, m6, ready
    data = msg.data[1:-1].split(',')
    m2.goal_position = float(data[0])
    m1.goal_position = float(data[1])
    m4.goal_position = float(data[2])
    m6.goal_position = float(data[3])
    m3.goal_position = float(data[4])
    ready = True
    print(f'{ready}')

def state_callback(msg):
    global m1, m2, m3, m4, m6
    if msg.ID == 1:
        m1.current_position = bit2rad(msg.Present_Position)
        m1.move_complete = bool(msg.Moving)
    elif msg.ID == 2:
        m2.current_position = bit2rad(msg.Present_Position)
        m2.move_complete = bool(msg.Moving)
    elif msg.ID == 3:
        m3.current_position = bit2rad(msg.Present_Position)
        m3.move_complete = bool(msg.Moving)
    elif msg.ID == 4:
        m4.current_position = bit2rad(msg.Present_Position)
        m4.move_complete = bool(msg.Moving)
    elif msg.ID == 6:
        m6.current_position = bit2rad(msg.Present_Position)
        m6.move_complete = bool(msg.Moving)

def prepare_move_motors():
    t = 5 # time to reach goal
    print('sending')
    global m1, m2, m3, m4, m6
    dtheta_list = [0, 0, 0, 0, 0]
    dtheta_list[0] = m2.goal_position - m2.current_position
    dtheta_list[1] = m1.goal_position - m1.current_position
    dtheta_list[2] = m4.goal_position - m4.current_position
    dtheta_list[3] = m6.goal_position - m6.current_position
    dtheta_list[4] = m3.goal_position - m3.current_position
    max_dtheta = max(dtheta_list)
    min_dtheta = min(dtheta_list)
    m1.speed = get_angular_speed(dtheta_list[1], t)
    m2.speed = get_angular_speed(dtheta_list[0], t)
    m3.speed = get_angular_speed(dtheta_list[4], t)
    m4.speed = get_angular_speed(dtheta_list[2], t)
    m6.speed = get_angular_speed(dtheta_list[3], t)

def main():
    global ready
    global m1, m2, m3, m4, m6
    m1, m2, m3, m4, m6 = Motor(1), Motor(2), Motor(3), Motor(4), Motor(6)
    ready = True

    rospy.init_node('test')
    publisher = rospy.Publisher('/set_position', AX, queue_size=10)
    subsciber = rospy.Subscriber('/j_positions', String, callback)
    # subsciber_fake_controller = rospy.Subscriber('/move_group/fake_controller_joint_states', String, callback)
    motor_subscriber = rospy.Subscriber('/motor_states', AX, state_callback)
    rate = rospy.Rate(1)

    msg_1 = AX()
    msg_1.ID = 1
    msg_2 = AX()
    msg_2.ID = 2
    msg_3 = AX()
    msg_3.ID = 3
    msg_4 = AX()
    msg_4.ID = 4
    msg_6 = AX()
    msg_6.ID = 6
    zero = bool(int(sys.argv[-1]))
    print(f'{zero}')
    while not rospy.is_shutdown():

        subsciber
        motor_subscriber
        rate.sleep()
        print('waiting')
        
        if not ready:
            continue

        prepare_move_motors()

        print(rad2bit(m1.goal_position))
        msg_1.Goal_Position = rad2bit(m1.goal_position)
        msg_1.Moving_Speed = angular_speed_to_byte(m1.speed)
        msg_1.LED = 1 

        msg_2.Goal_Position = rad2bit(m2.goal_position)
        msg_2.Moving_Speed = angular_speed_to_byte(m2.speed)
        msg_2.LED = 1

        msg_3.Goal_Position = rad2bit(m3.goal_position)
        msg_3.Moving_Speed = angular_speed_to_byte(m3.speed)
        msg_3.LED = 1

        msg_4.Goal_Position = rad2bit(m4.goal_position)
        msg_4.Moving_Speed = angular_speed_to_byte(m4.speed)
        msg_4.LED = 1

        msg_6.Goal_Position = rad2bit(m6.goal_position)
        msg_6.Moving_Speed = angular_speed_to_byte(m6.speed)
        msg_6.LED = 1 

        publisher.publish(msg_1)
        publisher.publish(msg_2)
        publisher.publish(msg_3)
        publisher.publish(msg_4)
        publisher.publish(msg_6)

        ready = False

if __name__ == '__main__':
    main()
