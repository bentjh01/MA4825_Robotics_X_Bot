import rospy
from xbot_msgs.msg import AXState
from sensor_msgs.msg import JointState
from std_msgs.msg import String
import sys
from xbot_control.simple_controller_configuration import Config
from xbot_control.controller_tools import FIFOQueue

config = Config()
#TODO-add flick offset when store or retrieve
#TODO-add option to add offset to compensate mechanical tilt
#TODO-add a final pose signal so that controller may check to return to start
class SimpleController():
    def __init__(self, reset):
        self.goal_positions_queue = FIFOQueue()
        self.goal_speeds = []
        self.current_positions = []
        self.move_complete = False
        self.led_enabled_list = []
        self.torque_enabled_list = []
        self.joint_names = []
        self.__init__rospy()
        self.reset = reset
        self.store = True

    def __init__rospy(self):
        node_name = 'xbot_simple_controller'
        inverse_kinematics_name = 'xbot_inverse_kinematics'
        rospy.init_node(node_name)
        self.motor_state_subscriber = rospy.Subscriber('/xbot_driver/motor_states', AXState, self.motor_state_callback)
        self.set_state_subscriber = rospy.Subscriber(f'/{inverse_kinematics_name}/goal_joint_states', JointState, self.set_state_callback)
        self.store_retrieve_subscriber = rospy.Subscriber(f'UI_Topic', String, self.store_retrieve_callback) #TODO-get correct topic
        self.cmd_state_publisher = rospy.Publisher(f'{node_name}/cmd_state', AXState, queue_size=1)
        self.cmd_publish_rate = rospy.Rate(10)

    def store_retrieve_callback(self, store_retrieve_msg): #TODO-to be verified
        data = store_retrieve_msg.data
        if 'Store' in data:
            self.store = True
        else:
            self.store = False

    def motor_state_callback(self, ax_state_msg):
        current_positons = []
        led_enabled_list = []
        torque_enabled_list = []
        joint_names = []
        move_complete = True
        for i, name in enumerate(ax_state_msg.name):
            if ax_state_msg.Moving[i]:
                move_complete = False
            current_positons.append(ax_state_msg.Present_Position[i])
            led_enabled_list.append(ax_state_msg.LED[i])
            torque_enabled_list.append(ax_state_msg.Torque_Enabled[i])
            joint_names.append(name)
        self.move_complete = move_complete
        self.current_positions = current_positons
        self.led_enabled_list = led_enabled_list
        self.torque_enabled_list = torque_enabled_list
        self.joint_names = joint_names

    def set_state_callback(self, joint_state_msg):
        goal_positons = []
        for i, name in enumerate(joint_state_msg.name):
            proposed_position = joint_state_msg.position[i]
            #TODO-uncomment when values added to simple_contrller_configurration.py
            # min_position = self.joint_ranges[i][0]
            # max_position = self.joint_ranges[i][1]
            # if proposed_position < min_position:
            #     proposed_position = min_position
            # elif proposed_position > max_position:
            #     proposed_position = max_position
            goal_positons.append(proposed_position)
        self.goal_positions_queue.enqueue(goal_positons)

    def find_move_time(self):
        dtheta_list = []
        for i, goal_position in enumerate(self.goal_positions_queue.query(0)):
            if i == 3 and self.store: #TODO-check clockwise or anti
                goal_position += config.store_retrieve_offset
            elif i == 3 and not self.store:
                goal_position -= config.store_retrieve_offset
            dtheta = goal_position - self.current_positions[i]
            dtheta_list.append(dtheta)
        max_dtheta = max(dtheta_list)
        min_dtheta = min(dtheta_list)
        for speed in config.speed_linspace:
            proposed_time = max_dtheta/speed
            max_speed = min_dtheta/proposed_time
            if max_speed < config.max_speed_limit:
                break
        return dtheta_list, proposed_time
         

    def prepare_move_motors(self):
        dtheta_list, moving_time = self.find_move_time()
        move_speeds = []
        for i, dtheta in enumerate(dtheta_list):
            proposed_speed = dtheta/moving_time
            if proposed_speed < config.min_speed_limit:
                proposed_speed = config.min_speed_limit
            move_speeds.append(proposed_speed)
        self.goal_speeds = move_speeds

    def publish_cmd_state(self):
        cmd_state_msg = AXState()
        goal_positions = self.goal_positions_queue.dequeue()
        for i, name in enumerate(self.joint_names):
            cmd_state_msg.Moving_Speed[i] = self.goal_speeds[i]
            cmd_state_msg.Goal_Position[i] = goal_positions[i]
            cmd_state_msg.LED[i] = self.led_enabled_list[i]
            cmd_state_msg.Torque_Enable[i] = self.torque_enabled_list[i]
        self.cmd_state_publisher(cmd_state_msg)
        self.cmd_publish_rate.sleep()

    def main(self):
        while not rospy.is_shutdown():
            self.motor_state_subscriber
            self.set_state_subscriber
            if self.reset:
                self.goal_positions_queue.enqueue([0., 0., 0., 0., 0.])
                print('Resetting')
            if not self.move_complete or self.goal_positions_queue.is_empty():
                continue
            self.prepare_move_motors()
            self.publish_cmd_state()
            print('Motion Complete')

if __name__ == '__main__':
    reset = bool(int(sys.argv[-1]))
    xBotSimpleController = SimpleController(reset)
    xBotSimpleController.main()
