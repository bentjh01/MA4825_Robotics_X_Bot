import rospy
from std_msgs import String
from xbot_msgs.msg import pose_action

class UI2XBOT:
    def __init__(self):
        self.cmd_talker = rospy.Publisher('/goal', Pose)
        self.locker_coordinates =   {1:[1,2,3], 2:[1,2,3], 3:[1,2,3],
                                     4:[1,2,3], 5:[1,2,3], 6:[1,2,3],
                                     7:[1,2,3], 8:[1,2,3], 9:[1,2,3]}
    
    def call_back(self, data):
        str_data = str(data.data)
        locker_id = int(str_data[-1])

        goal = pose_action()
        goal.store = False
        if 'Store' in str_data:
            goal.store = True

        goal.position.x = self.locker_coordinates[locker_id][0]
        goal.position.y = self.locker_coordinates[locker_id][1]
        goal.position.z = self.locker_coordinates[locker_id][2]

        goal.orientation.x = self.locker_coordinates[locker_id][3]
        goal.orientation.y = self.locker_coordinates[locker_id][4]
        goal.orientation.z = self.locker_coordinates[locker_id][5]
        goal.orientation.w = self.locker_coordinates[locker_id][6]

        self.cmd_talker.pub(goal)

    def run(self):
        rospy.Subscriber('/ui', String, self.callback)
        rospy.spin()

    
def main():
    node = UI2XBOT
    node.run()

if __name__ == '__main__':
    main()