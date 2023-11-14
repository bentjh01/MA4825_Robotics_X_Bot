import rospy
from xbot_msgs.msg import AXState
from sensor_msgs.msg import JointState
import numpy as np

class FIFOQueue:
  def __init__(self):
    self._items = []

  def enqueue(self, item):
    self._items.append(item)
    while self.__len__() > 2:
      self.dequeue(self)

  def dequeue(self):
    if not self._items:
      raise IndexError("Queue is empty")
    return self._items.pop(0)
  
  def query(self, index):
    if self.is_empty():
      raise IndexError("Queue is empty")
    return self._items[index]

  def is_empty(self):
    return not self._items

  def __len__(self):
    return len(self._items)

class OpenLoopController():
    def __init__(self):
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
        self.max_speed_limit = 0.8 # [rad/s]
        self.min_speed_limit = 0.6 # [rad/s]

    def __init__rospy(self):
        rospy.init_node('xbot_open_loop_controller')
        self.set_state_subscriber = rospy.Subscriber('/manual_kinematics/goal_joint_states', JointState, self.set_state_callback)
        self.cmd_state_publisher = rospy.Publisher('/open_loop_controller/cmd_state', AXState, queue_size=1)
        self.estimated_motor_state_publisher = rospy.Publisher('/estimated_motor_state', AXState, queue_size=1)
        # self.estimated_motor_state_publish_rate = rospy.Rate()

    def set_state_callback(self, joint_state_msg):
        goal_positions = []
        self.goal_positions_queue.enqueue(joint_state_msg.position)
        print(goal_positions)

    def find_move_time(self):
        dtheta_list = []
        for i, goal_position in enumerate(self.goal_positions_queue.query(0)):
            dtheta = goal_position - self.estimated_current_positions[i]
            dtheta_list.append(dtheta)
        max_dtheta = max(dtheta_list)
        min_dtheta = min(dtheta_list)
        print(f'max {max_dtheta}')
        print(f'fmin {min_dtheta}')
        for speed in np.linspace(self.max_speed_limit, self.min_speed_limit,10):
            proposed_time = min_dtheta/speed
            min_speed = max_dtheta/proposed_time
            if min_speed > self.min_speed_limit:
                break
        self.estimated_travel_time = proposed_time
        return dtheta_list, proposed_time
         
    def prepare_move_motors(self):
        dtheta_list, moving_time = self.find_move_time()
        move_speeds = []
        for i, dtheta in enumerate(dtheta_list):
            proposed_speed = dtheta/moving_time
            if proposed_speed > self.max_speed_limit:
               proposed_speed = self.max_speed_limit
            if proposed_speed < self.min_speed_limit:
               proposed_speed = self.min_speed_limit
            move_speeds.append(proposed_speed)
        self.goal_speeds = move_speeds

    def publish_cmd_state(self):
        cmd_state_msg = AXState()
        self.current_goal_positions = self.goal_positions_queue.dequeue()
        for i, val in enumerate(self.goal_speeds):
           if type(val) != float:
              self.goal_speeds[i] = 0.3
        cmd_state_msg.Moving_Speed = self.goal_speeds
        cmd_state_msg.Goal_Position = self.current_goal_positions
        if self.estimated_move_complete:
            self.cmd_state_publisher.publish(cmd_state_msg)
            self.cmd_sent_time = rospy.get_time()
            self.estimated_move_complete = False
            self.estimate_motor_state(self.current_goal_positions)
            print(f'Published: \nPositions: {cmd_state_msg.Goal_Position} \nSpeeds:{cmd_state_msg.Moving_Speed}')

    def publish_motor_state(self):
       estimated_motor_state_msg = AXState()
       estimated_motor_state_msg.Present_Position = self.estimated_current_positions 
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
            if self.goal_positions_queue.is_empty():
               continue
            self.prepare_move_motors()
            self.publish_cmd_state()

if __name__ == '__main__':
    xBotSimpleController = OpenLoopController()
    xBotSimpleController.main()
