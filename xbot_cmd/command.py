import rospy
from std_msgs import String
from xbot_msgs.msg import goal_pose

def callback(data):
    locker_coordinates =    {1:[1,2,3], 2:[1,2,3], 3:[1,2,3],
                             4:[1,2,3], 5:[1,2,3], 6:[1,2,3],
                             7:[1,2,3], 8:[1,2,3], 9:[1,2,3]}
    
    str_data = str(data.data)
    
    goal.store = False
    if 'Store' in str_data:
        goal.store = True
    
    locker_id = int(str_data[-1])
    goal = goal_pose()
    goal.position.x = locker_coordinates[locker_id][0]
    goal.position.y = locker_coordinates[locker_id][1]
    goal.position.z = locker_coordinates[locker_id][2]

    goal.orientation.x = locker_coordinates[locker_id][3]
    goal.orientation.y = locker_coordinates[locker_id][4]
    goal.orientation.z = locker_coordinates[locker_id][5]
    goal.orientation.w = locker_coordinates[locker_id][6]

    cmd_talker.pub(goal)

def main():
    cmd_talker = rospy.Publisher('/goal', Pose)
    cmd_listener = rospy.Subscriber('/ui', String, callback)
    rospy.init_node('xBot_cmd')
    cmd_listener
    rospy.spin()

if __name__ == '__main__':
    main()