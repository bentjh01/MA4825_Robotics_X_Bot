import rospy
# import message_filters
from std_msgs.msg import String
from std_msgs.msg import Bool
from geometry_msgs.msg import Point 
from xbot_msgs.msg import pose_action

unit_hor = 10
unit_ver = 10
unit_fwd = 20

class UI2XBOT:
    def __init__(self):
        self.goal_talker = rospy.Publisher('/goal', Point)
        self.action_talker = rospy.Publisher('/key_action', Bool)
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

        goal = Point()
        goal.x = self.locker_coordinates[locker_id][0]
        goal.y = self.locker_coordinates[locker_id][1]
        goal.z = self.locker_coordinates[locker_id][2]

        if action == 'store':
            self.action = True
        elif action == 'retrieve':
            self.action = False

        self.goal_talker.pub(goal)
        self.action_talker.pub(action)

    def run(self):
        rospy.Subscriber('/ui', String, self.callback)
        rospy.spin()

# class LS2XBOT:
#     def __init__(self):
#         self.cmd_talker = rospy.Publisher('/goal', Pose)
    
#     def goal_callback(self, limit_msg, goal_msg):
#         limit_msg = bool(limit_msg.data)
#         goal = goal_msg.data
#         if not goal.start_seq:
#             if goal.action == 'store':
#                 if goal.ls_status != limit_msg: # if limit status changes (pressed when storing or open when retriving)
#                     goal.start_seq = True

#         self.cmd_talker.pub(goal)

#     def run(self):
#         # rospy.Subscriber('/limit_switch', Bool, self.ls_callback)
#         # rospy.Subsciber('/goal', String, self.goal_callback)

#         limit_sub = message_filters.Subscriber('/limit_switch', Bool)
#         goal_sub = message_filters.Subscriber('/goal', String)

#         ts = message_filters.TimeSynchronizer([limit_sub, goal_sub], 10)
#         ts.registerCallback(self.callback)
#         rospy.spin()


def main():
    ui_node = UI2XBOT
    ui_node.run()
    

if __name__ == '__main__':
    main()