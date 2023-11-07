import rospy
from std_msgs import String
from std_msgs import Bool
from xbot_msgs.msg import pose_action

unit_hor = 10
unit_ver = 10
unit_fwd = 20

class UI2XBOT:
    def __init__(self):
        self.cmd_talker = rospy.Publisher('/goal', Pose)
        # x: arm to board, y: left right, z: top and bottom
        self.locker_coordinates = {
            1:[unit_fwd, -unit_hor, unit_ver],  2:[unit_fwd, 0, unit_ver],  3:[unit_fwd, unit_hor, unit_ver],
            4:[unit_fwd, -unit_hor, 0],         5:[unit_fwd, 0, 0],         6:[unit_fwd, unit_hor, 0],
            7:[unit_fwd, -unit_hor, -unit_ver], 8:[unit_fwd, 0, -unit_ver], 9:[unit_fwd, unit_hor, -unit_ver]
        }
    
    def callback(self, msg):
        str_data = str(msg.data)
        locker_id = int(str_data[0])
        action = str_data[1:]

        goal = pose_action()

        goal.wait_ls = True
        goal.store = False
        if action == 'store':
            goal.store = True

        goal.position.x = self.locker_coordinates[locker_id][0]
        goal.position.y = self.locker_coordinates[locker_id][1]
        goal.position.z = self.locker_coordinates[locker_id][2]

        self.cmd_talker.pub(goal)

    def run(self):
        rospy.Subscriber('/ui', String, self.callback)
        rospy.spin()

class LS2XBOT:
    def __init__(self):
        self.cmd_talker = rospy.Publisher('/goal', Pose)
    
    def callback(self, msg):
        ls_open = bool(msg.data)

        goal = pose_action()
        goal.wait_ls = not ls_open

        self.cmd_talker.pub(goal)

    def run(self):
        rospy.Subscriber('/limit_switch', Bool, self.callback)
        rospy.spin()



def main():
    ui_node = UI2XBOT
    ui_node.run()
    ls_node = LS2XBOT
    ls_node.run()


if __name__ == '__main__':
    main()