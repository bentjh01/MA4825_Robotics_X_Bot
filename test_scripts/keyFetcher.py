import rospy
import moveit_commander
from moveit_commander import PlanningSceneInterface
from geometry_msgs.msg import PoseStamped

def main():
    rospy.init_node('my_robot_control', anonymous=True)
    robot = moveit_commander.RobotCommander()
    scene = PlanningSceneInterface()
    group_name = "robot_arm"  # Change this to the name of the planning group in your SRDF
    move_group = moveit_commander.MoveGroupCommander(group_name)

    target_pose = move_group.get_random_pose()
    print(target_pose.pose.position)

    # Set the target pose
    # move_group.set_random_target()

    target_pose = PoseStamped()
    target_pose.pose.position.x = -0.11  # 设置 x 坐标
    target_pose.pose.position.y = -0.15  # 设置 y 坐标
    target_pose.pose.position.z = -0.068  # 设置 z 坐标

    # # 设置目标姿态（姿态四元数或欧拉角）
    # # 例如，使用四元数表示姿态
    # target_pose.orientation.x = 0.0
    # target_pose.orientation.y = 0.0
    # target_pose.orientation.z = 0.0
    # target_pose.orientation.w = 1.0

    move_group.set_pose_target(target_pose)

    # Plan and execute the motion
    plan_success, plan, planning_time, error_code = move_group.plan()
    print(f'{plan_success}\n, {plan}\n, {planning_time}\n, {error_code}\n')

    target_pose = move_group.get_joint_value_target()
    # target_pose = move_group.get_current_pose()
    print(target_pose)

    if plan_success:
        move_group.execute(plan)
    else:
        print("fail to plan a motion")

if name == 'main':
    main()