import rospy
from xbot_msgs.msg import AXState
from sensor_msgs.msg import JointState
import numpy as np

class SimpleController():
    def __init__(self, reset):
        reset_position = [0.,0.,0.,1.57,0.] # [rad]
        # Goal Trajectory
        self.goal_positions_queue = FIFOQueue()
        self.goal_positions_queue.enqueue(reset_position)
        self.current_goal_positions = reset_position
        self.goal_speeds = []
        # Estimated Feedback
        self.estimated_current_positions = reset_position
        self.estimated_move_complete = True
        # ROS
        self.__init__rospy()
        # Controller constraints
        self.max_speed_limit = 1.0 # [rad/s]
        self.min_speed_limit = 0.1 # [rad/s]

    def __init__rospy(self):
        node_name = 'xbot_open_loop_controller'
        inverse_kinematics_name = 'xbot_manual_kinematics'
        rospy.init_node(node_name)
        self.set_state_subscriber = rospy.Subscriber(f'/{inverse_kinematics_name}/goal_joint_states', JointState, self.set_state_callback)
        self.cmd_state_publisher = rospy.Publisher(f'{node_name}/cmd_state', AXState, queue_size=1)
        self.cmd_publish_rate = rospy.Rate(1)

    def set_state_callback(self, joint_state_msg):
        goal_positons = []
        for i, name in enumerate(joint_state_msg.name):
            proposed_position = joint_state_msg.position[i]
            goal_positons.append(proposed_position)
        self.goal_positions_queue.enqueue(goal_positons)

    def find_move_time(self):
        dtheta_list = []
        for i, goal_position in enumerate(self.goal_positions_queue.query(0)):
            dtheta = goal_position - self.estimated_current_positions[i]
            dtheta_list.append(dtheta)
        max_dtheta = max(dtheta_list)
        min_dtheta = min(dtheta_list)
        for speed in np.linspace(self.min_speed_limit, self.max_speed_limit):
            proposed_time = max_dtheta/speed
            max_speed = min_dtheta/proposed_time
            if max_speed < self.max_speed_limit:
                break
        self.estimated_travel_time = proposed_time
        return dtheta_list, proposed_time
         
    def prepare_move_motors(self):
        dtheta_list, moving_time = self.find_move_time()
        move_speeds = []
        for i, dtheta in enumerate(dtheta_list):
            proposed_speed = dtheta/moving_time
            move_speeds.append(proposed_speed)
        self.goal_speeds = move_speeds

    def publish_cmd_state(self):
        cmd_state_msg = AXState()
        self.current_goal_positions = self.goal_positions_queue.dequeue()
        cmd_state_msg.Moving_Speed = self.goal_speeds
        cmd_state_msg.Goal_Position = self.current_goal_positions
        if self.estimated_move_complete:
            self.cmd_state_publisher(cmd_state_msg)
            self.cmd_sent_time = rospy.get_time()
            self.estimated_move_complete = False
            self.estimate_motor_state(self.current_goal_positions)
            print(f'Published: \nPositions: {cmd_state_msg.Goal_Positon} \nSpeeds:{cmd_state_msg.Moving_Speed}')

    def estimate_motor_state(self, goal_positions):
        time_elapsed = rospy.get_time() - self.cmd_sent_time
        if  time_elapsed >= self.estimated_travel_time:
            self.estimated_current_positions = goal_positions
            self.estimated_move_complete = True

    def main(self):
        while not rospy.is_shutdown():
            self.set_state_subscriber
            self.prepare_move_motors()
            if self.goal_positions_queue.is_empty():
               continue
            self.publish_cmd_state()

if __name__ == '__main__':
    xBotSimpleController = SimpleController()
    xBotSimpleController.main()

class FIFOQueue:
  def __init__(self):
    self._items = []

  def enqueue(self, item):
    self._items.append(item)

  def dequeue(self):
    if not self._items:
      raise IndexError("Queue is empty")
    return self._items.pop(0)
  
  def query(self, index):
    if not self._items:
      raise IndexError("Queue is empty")
    return self._items[index]

  def is_empty(self):
    return not self._items

  def __len__(self):
    return len(self._items)
