import rospy
from moveit_commander import MoveGroupCommander
import geometry_msgs

rospy.init_node('key_fetcher_node')
robot = MoveGroupCommander('robot_arm')

# 设置目标位置和姿态
target_pose = geometry_msgs.msg.Pose()
target_pose.position.x = 0.05  # 设置 x 坐标
target_pose.position.y = 0.05  # 设置 y 坐标
target_pose.position.z = 0.05  # 设置 z 坐标

# 设置目标姿态（姿态四元数或欧拉角）
# 例如，使用四元数表示姿态
target_pose.orientation.x = 0.0
target_pose.orientation.y = 0.0
target_pose.orientation.z = 0.0
target_pose.orientation.w = 1.0

# 设置目标位置姿态为机械臂的目标
robot.set_pose_target(target_pose)

# 规划轨迹
plan_success, plan, planning_time, error_code= robot.plan()
print(plan_success)
print(f'{plan_success}\n, {plan}\n, {planning_time}\n, {error_code}\n')

# 执行轨迹
robot.execute(plan)

rospy.signal_shutdown('Done')