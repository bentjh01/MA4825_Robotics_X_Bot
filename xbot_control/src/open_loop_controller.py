import rospy
from xbot_msgs.msg import AXState
from sensor_msgs.msg import JointState
import numpy as np

class OpenLoopController():
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
        self.max_speed_limit = 1.111 # [rad/s]
        self.min_speed_limit = 0.111 # [rad/s]

    def __init__rospy(self):
        rospy.init_node('xbot_open_loop_controller')
        self.set_state_subscriber = rospy.Subscriber('/manual_kinematics/goal_joint_states', JointState, self.set_state_callback)
        self.cmd_state_publisher = rospy.Publisher('/open_loop_controller/cmd_state', AXState, queue_size=1)
        self.estimated_motor_state_publisher = rospy.Publisher('/estimated_motor_state', AXState, queue_size=1)
        # self.estimated_motor_state_publish_rate = rospy.Rate()

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

    def publish_motor_state(self):
       estimated_motor_state_msg = AXState()
       estimated_motor_state_msg.Present_Positon = self.estimated_current_positions 
       estimated_motor_state_msg.Moving = [False, False, False, False, False]
       self.estimated_motor_state_publisher.publish(estimated_motor_state_msg)

    def estimate_motor_state(self, goal_positions):
        time_elapsed = rospy.get_time() - self.cmd_sent_time
        if  time_elapsed >= self.estimated_travel_time:
            self.estimated_current_positions = goal_positions
            self.estimated_move_complete = True
            self.publish_motor_state()

    def main(self):
        while not rospy.is_shutdown():
            self.set_state_subscriber
            self.prepare_move_motors()
            if self.goal_positions_queue.is_empty():
               continue
            self.publish_cmd_state()

if __name__ == '__main__':
    xBotSimpleController = OpenLoopController()
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
