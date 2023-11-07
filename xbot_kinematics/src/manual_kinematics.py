import rospy
from sensor_msgs.msg import JointStates
from geometry_msgs.msg import Pose


#TODO:Add the joint positions for each locker number here

class ManualKinematics():
    def __init__(self):
        self.id_2_jointstates_map = {
            1:[], 2:[], 3:[],
            4:[], 5:[], 6:[],
            7:[], 8:[], 9:[]
        }
        self.__init__rospy()

    def __init__rospy(self):
        node_name = 'manual_kinematics'
        self.set_states_publisher = rospy.Publisher(f'/{node_name}/goal_joint_states', JointStates, queue_size = 10)
        self.goal_pose_subcriber = rospy.Subsciber('xbot_ui/goal_pose', Pose, self.goal_pose_callback)

    def goal_pose_callback(self, goal_pose_msg):
        self.goal_pose = goal_pose_msg
        # pose_x = goal_pose_msg.position.x
        # pose_y = goal_pose_msg.position.y
        # pose_z = goal_pose_msg.position.z
        # orientation_x = goal_pose_msg.orientation.x
        # orientation_y = goal_pose_msg.orientation.y
        # orientation_z = goal_pose_msg.orientation.z
        # orientation_w = goal_pose_msg.orientation.w

    def set_state_publish(self):
        set_state = JointStates()
        for i in range(5):
            set_state.name[i] = f'joint_{i+1}'
            set_state.position[i] = None

    def solve(self):
        self.goal_pose
        self.plan = 