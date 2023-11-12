import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import String, Bool
from xbot_msgs.msg import AXState
import math 

#TODO: Add the joint positions for each locker number here
#TODO: Implement feedback to system so that the arm doesnt execute a store when it supposed to retrieve
#TODO: add print() to be more verbose on working status
#TODO: wait for msg to have been sent

class ManualKinematics():
    def __init__(self):
        # higher than 512 is positive rad
        self.id_final_joint_angles = {
            1:[0.7795, -0.2176, 0.9313, 0.2683, -0.8807],
            3:[-0.7795, -0.2176, 0.8554, 0.2429, 0.7542],
            5:[0.0, 0.3442, 1.9284, 0.0405, -0.0304],
            7:[0.7795, -0.3897, 1.7766, -0.7288, -0.82],
            9:[-0.7542, -0.3695, 1.726, -0.577, 0.6782]
            }

        self.__init__rospy()

        # Sensors and Feedback
        self.limit_switch_pressed = False
        self.locker_id = 1
        self.motor_ready = True

        # Actions
        self.start = False

        # init msgs
        self.reset_state_msg = JointState()
        self.reset_state_msg.position = [0,0,0,math.pi/2,0]
        self.customer_state_msg = JointState()
        self.customer_state_msg.position = [0.6952999830245972, -0.301800012588501, 1.9020999670028687, -0.7106999754905701, -0.07159999758005142] #TODO

        self.goal_state_msg = JointState()
        self.goal_state_msg.position = [0,0,0,math.pi/2,0]
        self.safety_state_msg = JointState()
        self.current_state = JointState()
        
    def __init__rospy(self):
        rospy.init_node('moveit')
        self.set_states_publisher = rospy.Publisher('/manual_kinematics/goal_joint_states', JointState, queue_size = 1)
        self.locker_id_subscriber = rospy.Subscriber('/ui', String, self.locker_id_callback)
        self.limit_switch_subsciber = rospy.Subscriber('/limit_switch', Bool, self.limit_switch_callback)
        self.motor_state_subsciber = rospy.Subscriber('/driver/motor_states', AXState, self.motor_state__callback)
        self.set_states_publish_rate = rospy.Rate(5)
            
    # callbacks
    def motor_state__callback(self, motor_status_msg):
        a_list = motor_status_msg.Present_Position
        self.current_state.position = a_list
        self.motor_state = motor_status_msg.Moving
        self.motor_ready = True
        for motor_state in self.motor_state:
            if motor_state:
                self.motor_ready = False
                break

    def limit_switch_callback(self, limit_switch_msg):
        data = limit_switch_msg.data
        self.limit_switch_pressed = True
        if data:
            self.limit_switch_pressed = False

    def locker_id_callback(self, store_retrieve_msg):
        data = store_retrieve_msg.data
        self.locker_id = int(data[0])
        self.solve()
        self.start = True

    # publisher
    def set_state_publish(self):
        self.set_states_publisher.publish(self.goal_state_msg)
        self.set_states_publish_rate.sleep()

    def solve(self):
        self.goal_state_msg.position = self.id_final_joint_angles[self.locker_id]

    # planner actions
    def reset_arm(self):
        print('reset position')
        present_state = self.loadTup2List(self.current_state.position)
        self.goal_state_msg.position = [present_state[0],0,0,math.pi/2,present_state[4]]
        self.set_state_publish()
        rospy.sleep(3)
        self.goal_state_msg.position = [0,0,0,math.pi/2,0]

    def noj4_reset_arm(self):
        print('reset position')
        present_state = self.loadTup2List(self.current_state.position)
        self.goal_state_msg.position = [present_state[0],0,0,math.pi/2,present_state[4]]
        self.set_state_publish()
        self.goal_state_msg.position = [0,0,0,math.pi/2,0]


    def face_away_wall(self):
        print("face away from wall")
        present_state = self.loadTup2List(self.current_state.position)
        present_state[0] = math.pi/2
        present_state[4] = -math.pi/2
        if self.locker_id == 3 or self.locker_id == 9:
            present_state[0] = -math.pi/2
            present_state[4] = math.pi/2
        self.goal_state_msg.position = present_state

    def j4faceout(self):
        print("face away from wall")
        present_state = self.loadTup2List(self.current_state.position)
        # present_state[4] -= math.pi/2
        # if self.locker_id == 3 or self.locker_id == 9:
        #     present_state[4] += math.pi/2
        if self.locker_id == 1 :
            present_state[4] += math.pi/2
            present_state[3] += math.pi/4
        if self.locker_id == 7:
            present_state[4] += math.pi/2
        if self.locker_id == 3:
            present_state[4] -= math.pi/2
            present_state[3] += math.pi/4
        if self.locker_id == 9:
            present_state[4] -= math.pi/2
        

        self.goal_state_msg.position = present_state

    def j2j3j4_move(self):
        print('j2j3j4')
        a_list = [1,2,3,4,5]
        a_list[0] = self.current_state.position[0]
        a_list[1] = self.id_final_joint_angles[self.locker_id][1]
        a_list[2] = self.id_final_joint_angles[self.locker_id][2]
        a_list[3] = self.id_final_joint_angles[self.locker_id][3]
        a_list[4] = self.current_state.position[4]
        self.goal_state_msg.position = a_list

    def loadTup2List(self, tup):
        a_list = []
        for i in tup:
            a_list.append(i)
        return a_list   

    def goto_goal(self):
        print('go to goal')
        self.goal_state_msg.position = self.id_final_joint_angles[self.locker_id]

    def collect_prize(self):
        print('collect')
        present_state = self.loadTup2List(self.current_state.position)
        if self.locker_id == 1:
            present_state[2]-=math.pi/8
        elif self.locker_id == 3:
            present_state[3]-=math.pi/8
        elif self.locker_id ==7:
            present_state[3]-=math.pi/8
        else:
            present_state[3]-=math.pi/8
        self.goal_state_msg.position = present_state

    def retreat(self):
        print('retreat')
        present_state = self.loadTup2List(self.current_state.position)
        if self.locker_id == 1:
            pass
        if self.locker_id == 3:
            pass
        self.goal_state_msg.position = present_state

    def goto_customer(self):
        print('goto customer')
        present_state = self.loadTup2List(self.customer_state_msg.position)
        # self.goal_state_msg.position = [0.0, 0.3442, 1.9284, 0.0405, -0.0304]

    def main(self):
        delay_ = 3
        # start_time = rospy.get_time()
        while not rospy.is_shutdown():
            self.locker_id_subscriber
            self.limit_switch_subsciber
            self.motor_state_subsciber 
            if not self.start:
                continue
            self.set_state_publish()
            self.reset_arm()
            self.set_state_publish()
            rospy.sleep(delay_)

            self.face_away_wall()
            self.set_state_publish()
            rospy.sleep(delay_)

            self.j2j3j4_move()
            self.set_state_publish()
            rospy.sleep(delay_)
###
            self.goto_goal()
            self.set_state_publish()
            rospy.sleep(delay_)
###
            self.collect_prize()
            self.set_state_publish()
            rospy.sleep(delay_)

            self.retreat()
            self.set_state_publish()
            rospy.sleep(delay_)
###

            self.face_away_wall()
            self.set_state_publish()
            rospy.sleep(delay_)

            self.j2j3j4_move()
            self.set_state_publish()
            rospy.sleep(delay_)
### 
            self.j4faceout()
            self.set_state_publish()
            rospy.sleep(delay_+6)

            # self.noj4_reset_arm()
            # self.set_state_publish()
            # rospy.sleep(delay_)

            self.reset_arm()
            self.set_state_publish()
            rospy.sleep(delay_)

            # self.goto_customer()
            # self.set_state_publish()
            # rospy.sleep(delay_)

            self.start = False
            print("Done")


if __name__ == '__main__':
    manualKinematics = ManualKinematics()
    manualKinematics.main()