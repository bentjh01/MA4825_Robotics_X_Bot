import rospy
from geometry_msgs.msg import Pose
import moveit_commander
import moveit_msgs.msg

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node("move_group_python_interface_tutorial", anonymous=True)

robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()

group_name = "panda_arm"
move_group = moveit_commander.MoveGroupCommander(group_name)

# We can get the name of the reference frame for this robot:
planning_frame = move_group.get_planning_frame()
print("============ Planning frame: %s" % planning_frame)

# We can also print the name of the end-effector link for this group:
eef_link = move_group.get_end_effector_link()
print("============ End effector link: %s" % eef_link)

# We can get a list of all the groups in the robot:
group_names = robot.get_group_names()
print("============ Available Planning Groups:", robot.get_group_names())

# Sometimes for debugging it is useful to print the entire state of the
# robot:
print("============ Printing robot state")
print(robot.get_current_state())
print("")

pose_goal = Pose()
pose_goal.orientation.w = 1.0
pose_goal.position.x = 0.4
pose_goal.position.y = 0.1
pose_goal.position.z = 0.4

move_group.set_pose_target(pose_goal)

# `go()` returns a boolean indicating whether the planning and execution was successful.
success = move_group.go(wait=True)
# Calling `stop()` ensures that there is no residual movement
move_group.stop()
# It is always good to clear your targets after planning with poses.
# Note: there is no equivalent function for clear_joint_value_targets().
move_group.clear_pose_targets()

###########################################

waypoints = []

wpose = move_group.get_current_pose().pose
wpose.position.z -= scale * 0.1  # First move up (z)
wpose.position.y += scale * 0.2  # and sideways (y)
waypoints.append(copy.deepcopy(wpose))

wpose.position.x += scale * 0.1  # Second move forward/backwards in (x)
waypoints.append(copy.deepcopy(wpose))

wpose.position.y -= scale * 0.1  # Third move sideways (y)
waypoints.append(copy.deepcopy(wpose))

# We want the Cartesian path to be interpolated at a resolution of 1 cm
# which is why we will specify 0.01 as the eef_step in Cartesian
# translation.  We will disable the jump threshold by setting it to 0.0,
# ignoring the check for infeasible jumps in joint space, which is sufficient
# for this tutorial.
(plan, fraction) = move_group.compute_cartesian_path(
    waypoints, 0.01, 0.0  # waypoints to follow  # eef_step
)  # jump_threshold

# Note: We are just planning, not asking move_group to actually move the robot yet:
return plan, fraction

# Use execute if you would like the robot to follow the plan that has already been computed:
move_group.execute(plan, wait=True)

###########################################

import rospy
from sensor_msgs.msg import JointStates
from geometry_msgs.msg import Pose
from std_msgs.msg import String

#TODO: Add the joint positions for each locker number here
#TODO: Implement feedback to system so that the arm doesnt execute a store when it supposed to retrieve

class ManualKinematics():
    def __init__(self):
        self.id_2_plan_map = {
            1:[], 2:[], 3:[],
            4:[], 5:[], 6:[],
            7:[], 8:[], 9:[]
        }
        self.generate_id_2_plan_map()
        self.locker_id = None
        self.store = None 
        self.ready = False
        self.__init__rospy()

    def __init__rospy(self):
        node_name = 'manual_kinematics'
        self.set_states_publisher = rospy.Publisher(f'/{node_name}/goal_plan', JointStates, queue_size = 10)
        # self.goal_pose_subcriber = rospy.Subsciber('xbot_ui/goal_pose', Pose, self.goal_pose_callback)
        self.store_retrieve_subscriber = rospy.Subscriber(f'UI_Topic', String, self.store_retrieve_callback) #TODO-get correct topic
        self.set_states_publish_rate = rospy.Rate(10)

    # def goal_pose_callback(self, goal_pose_msg):
    #     self.goal_pose = goal_pose_msg
        # pose_x = goal_pose_msg.position.x
        # pose_y = goal_pose_msg.position.y
        # pose_z = goal_pose_msg.position.z
        # orientation_x = goal_pose_msg.orientation.x
        # orientation_y = goal_pose_msg.orientation.y
        # orientation_z = goal_pose_msg.orientation.z
        # orientation_w = goal_pose_msg.orientation.w

    def solve(self):
        self.plan_msg = self.id_2_plan_map[self.locker_id]

    def store_retrieve_callback(self, store_retrieve_msg):
        data = store_retrieve_msg.data
        if 'Store' in data:
            self.store = True
        else:
            self.store = False
        self.locker_id = int(data[0])
        self.solve()
        self.ready = True

    def generate_id_2_plan_map(self):
        for key in self.id_2_plan_map.keys():
            joint_state = JointStates()
            for i in range(5):
                joint_state.name[i] = f'joint_{i+1}'
            joint_state.position = self.id_2_plan_map[key]
            self.id_2_plan_map[key] = joint_state

    def set_state_publish(self):
        # for i in range(5):
        #     set_state.name[i] = f'joint_{i+1}'
        #     set_state.position[i] = None
        self.set_states_publisher.publish(self.plan_msg)
        self.set_states_publish_rate.sleep()

    def main(self):
        while not rospy.is_shutdown():
            self.goal_pose_subcriber 
            self.store_retrieve_subscriber
            while not self.ready:
                continue
            self.set_state_publish()
            self.ready = False