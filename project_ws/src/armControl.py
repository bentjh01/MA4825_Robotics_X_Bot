import geometry_msgs
import rospy
from moveit_commander import MoveGroupCommander

rospy.init_node('armKeyFetcher')
robot = MoveGroupCommander('robot_arm_jj_v4')

target_pose = geometry_msgs.msg.Pose()
target_pose.position.x = 0.5 
target_pose.position.y = 0.5 
target_pose.position.z = 0.5 

target_pose.orientation.x = 0.0 
target_pose.orientation.y = 0.0 
target_pose.orientation.z = 0.0
target_pose.orientation.w = 1.0

robot.set_pose_target(target_pose)

plan = robot.plan()

robot.execute(plan)

