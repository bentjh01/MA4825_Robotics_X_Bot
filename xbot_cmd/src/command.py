import rospy
# import message_filters
from std_msgs.msg import String
from std_msgs.msg import Bool
from geometry_msgs.msg import Pose 
from xbot_msgs.msg import AXState

unit_hor = 10
unit_ver = 10
unit_fwd = 20

class UI2XBOT:
    def __init__(self):
        self.goal_talker = rospy.Publisher('/goal_pose', Pose)
        self.locker_id_subscriber = rospy.Subscriber('/ui', String, self.locker_id_callback)
        self.limit_switch_subsciber = rospy.Subscriber('/limit_switch', Bool, self.limit_switch_callback)
        self.motor_state_subsciber = rospy.Subscriber('/driver/motor_states', AXState, self.motor_state__callback)
        # x: arm to board, y: left right, z: top and bottom
        self.locker_coordinates = {
            1:[unit_fwd, -unit_hor, unit_ver],  2:[unit_fwd, 0, unit_ver],  3:[unit_fwd, unit_hor, unit_ver],
            4:[unit_fwd, -unit_hor, 0],         5:[unit_fwd, 0, 0],         6:[unit_fwd, unit_hor, 0],
            7:[unit_fwd, -unit_hor, -unit_ver], 8:[unit_fwd, 0, -unit_ver], 9:[unit_fwd, unit_hor, -unit_ver]
        }
        self.collection_pose = Pose()
        self.collection_pose.position.x = 0.1
        self.collection_pose.position.y = -0.1
        self.collection_pose.position.z = 0.15

        self.rest_pose = Pose()
        self.rest_pose.position.x = 0.0
        self.rest_pose.position.y = -0.13
        self.rest_pose.position.z = 0.3

        self.motor_states = []
        self.joint_states = []
        self.motor_ready = False
        self.limit_switch_pressed = True
        self.arm_state = 0 # 0:waiting for locker id, 1: at item, 2: collected item, 4: go to collection Pose, 5: waiting for collection, 
        self.goal_pose = Pose()
 
    
    def locker_id_callback(self, msg):
        data = msg.data
        locker_id = int(data[0])
        self.goal_pose.position.x = self.locker_coordinates[locker_id][0]
        self.goal_pose.position.y = self.locker_coordinates[locker_id][1]
        self.goal_pose.position.z = self.locker_coordinates[locker_id][2]

    def motor_state__callback(self, motor_status_msg):
        self.joint_states = motor_status_msg.Present_Position
        self.motor_states = motor_status_msg.Moving
        self.motor_ready = True
        for motor_state in self.motor_states:
            if motor_state:
                self.motor_ready = False
                break

    def limit_switch_callback(self, limit_switch_msg):
        data = limit_switch_msg.data
        self.limit_switch_pressed = True
        if data:
            self.limit_switch_pressed = False

    def run(self):
        while not rospy.is_shutdown():
            self.locker_id_subscriber
            self.limit_switch_subsciber 
            self.motor_state_subsciber

            if self.arm_state ==0: 
                # arm is at reset state
                if self.motor_ready and not self.limit_switch_pressed:
                    self.goal_talker.publish(self.goal_pose)
                    self.arm_state = 1
                    self.motor_ready = False
            elif self.arm_state==1:
                # arm is below item
                if self.motor_ready:
                    self.goal_pose.z += 0.05
                    self.goal_talker.publish(self.goal_pose)
                    self.arm_state = 2
                    self.motor_ready = False
            elif self.arm_state==2:
                # arm has collected item
                if self.motor_ready and self.limit_switch_pressed:
                    self.goal_pose.z = self.collection_pose
                    self.goal_talker.publish(self.goal_pose)
                    self.arm_state = 3
                    self.motor_ready = False
            elif self.arm_state==3:
                # item has been collected
                if self.motor_ready and not self.limit_switch_pressed:
                    self.goal_pose.z = self.rest_pose
                    self.goal_talker.publish(self.goal_pose)
                    self.arm_state = 3
                    self.motor_ready = False
                    self.arm_state = 0

def main():
    ui_node = UI2XBOT
    ui_node.run()
    

if __name__ == '__main__':
    main()