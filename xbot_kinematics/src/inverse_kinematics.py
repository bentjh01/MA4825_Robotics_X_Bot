import rospy
from geometry_msgs.msg import Pose
from sensor_msgs.msg import JointState
from moveit_comander import MoveGroupComander

class InverseKinamatics():
    def __init__(self) -> None:
        self.__init__rospy()
        self.move_group = MoveGroupComander('robot_arm')
        
    def __init__rospy(self):
        rospy.init_node('xbot_kinematics')
        self.locker_pose_subscriber = rospy.Subscriber('/goal_pose', Pose, self.locker_pose_callback)
        self.set_joint_subscriber = rospy.Subscriber('/move_group/fake_controller_joint_states', JointState, self.set_joint_callback)
        self.set_states_publisher = rospy.Publisher('/goal_joint_states', JointState, queue_size = 1)
        self.set_states_publish_rate = rospy.Rate(5)

    def locker_pose_callback(self, msg):
        self.move_group.set_pose_target(msg)
        sucess = self.move_group.go(wait=True)

    def set_joint_callback(self, msg):
        self.set_states_publisher.publish(msg)

    def run(self):
        while not rospy.is_shutdown():
            self.locker_pose_subscriber 
            self.set_joint_subscriber
