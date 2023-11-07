import rospy
from sensor_msgs.msg import JointStates
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
        self.locker_id = None
        self.motor_ready = True

        # Actions
        self.start = False

        # init msgs
        self.reset_state_msg = JointStates()
        self.reset_state_msg.position = [0,0,0,math.pi/2,0]
        self.customer_state_msg = JointStates()
        self.customer_state_msg.position = [0,0,0,math.pi/2,0] #TODO
        self.goal_state_msg = JointStates()
        self.safety_state_msg = JointStates()
        
    def __init__rospy(self):
        self.set_states_publisher = rospy.Publisher('/manual_kinematics/goal_plan', JointStates, queue_size = 10)
        self.locker_id_subscriber = rospy.Subscriber('/ui', String, self.locker_id_callback)
        self.limit_switch_subsciber = rospy.Subscriber('/limit_switch', Bool, self.limit_switch_callback)
        self.motor_state_subsciber = rospy.Subscriber('/estimated_motor_state', AXState, self.motor_state__callback)
            
    # callbacks
    def motor_state__callback(self, motor_status_msg):
        self.current_state = motor_status_msg.Present_Positions
        self.motor_ready = True

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
    def set_state_publish(self, state_msg):
        self.set_states_publisher.publish(state_msg)
        self.motor_ready = False
        while self.motor_ready == False:
            self.motor_state_subsciber

    def solve(self):
        self.goal_state_msg.position = self.id_final_joint_angles[self.locker_id].copy()

    # planner actions
    def reset_arm(self):
        self.set_state_publish(self.reset_state_msg)

    def face_away_wall(self, goal_state):
        safety_state = [math.pi/2, goal_state[1], goal_state[2], goal_state[3], -math.pi/2]
        if self.locker_id == 3 or self.locker_id == 9:
            safety_state[0] = -math.pi/2
            safety_state[1] = math.pi/2
        self.set_state_publish(self.reset_state_msg)

    def goto_goal(self):
        self.set_state_publish(self.goal_state_msg)

    def collect_prize(self):
        goal_state = self.current_position
        action_msg = JointStates()
        action_msg.position = [goal_state[0], goal_state[1],goal_state[2],goal_state[3],goal_state[4]]
        collecting = True
        count = 0
        resolution = 0.05
        #TODO - calibrate
        while collecting:
            action_msg.position[3] -= resolution
            action_msg.position[2] += resolution
            action_msg.position[1] -= resolution
            self.set_state_publish(action_msg)
            self.limit_switch_subsciber
            if self.limit_switch_pressed:
                break
            count += 1
            if count >= 5:
                break

    def retreat(self):
        retreat_msg = JointStates()
        retreat_msg.position = self.current_state
        #TODO - calibrate
        retreat_msg.position[3] -= 0.1
        retreat_msg.position[2] += 0.1
        retreat_msg.position[1] -= 0.1
        self.set_state_publish(retreat_msg)

    def goto_customer(self):
        self.set_state_publish(self.customer_state_msg)

    def main(self):
        while not rospy.is_shutdown():
            self.locker_id_subscriber
            self.limit_switch_subsciber
            self.motor_state_subsciber 
            if not self.start:
                continue
            self.reset_arm()
            self.face_away_wall(self.id_final_joint_angles[self.locker_id])
            self.goto_goal()
            self.collect_prize()
            self.retreat()
            self.face_away_wall(self.current_state.position)
            self.goto_customer()
            self.start = False


if __name__ == '__main__':
    manualKinematics = ManualKinematics()
    manualKinematics.main()