import rospy
from sensor_msgs.msg import JointStates
from geometry_msgs.msg import Pose
from std_msgs.msg import String

#TODO: Add the joint positions for each locker number here
#TODO: Implement feedback to system so that the arm doesnt execute a store when it supposed to retrieve
#TODO: add print() to be more verbose on working status
#TODO: wait for msg to have been sent

class ManualKinematics():
    def __init__(self):
        #TODO: find values
        self.id_2_plan_map = {
            1:[], 2:[], 3:[],
            4:[], 5:[], 6:[],
            7:[], 8:[], 9:[]
        }
        self.generate_id_2_plan_map()
        self.locker_id = None
        self.store = None 
        self.ready = False
        self.__init__rospy()

    def __init__rospy(self):
        node_name = 'manual_kinematics'
        self.set_states_publisher = rospy.Publisher(f'/{node_name}/goal_plan', JointStates, queue_size = 10)
        self.store_retrieve_subscriber = rospy.Subscriber(f'UI_Topic', String, self.store_retrieve_callback) #TODO-get correct topic
        self.set_states_publish_rate = rospy.Rate(10)

    def solve(self):
        self.plan_msg = self.id_2_plan_map[self.locker_id]

    def store_retrieve_callback(self, store_retrieve_msg):
        data = store_retrieve_msg.data
        if 'Store' in data:
            self.store = True
        else:
            self.store = False
        self.locker_id = int(data[0])
        self.solve()
        self.ready = True

    def generate_id_2_plan_map(self):
        for key in self.id_2_plan_map.keys():
            joint_state = JointStates()
            for i in range(5):
                joint_state.name[i] = f'joint_{i+1}'
            joint_state.position = self.id_2_plan_map[key]
            self.id_2_plan_map[key] = joint_state

    def set_state_publish(self):
        self.set_states_publisher.publish(self.plan_msg)
        self.set_states_publish_rate.sleep()
        self.ready = False

    def main(self):
        while not rospy.is_shutdown():
            self.goal_pose_subcriber 
            self.store_retrieve_subscriber
            while not self.ready:
                continue
            self.set_state_publish()

if __name__ == '__main__':
    manualKinematics = ManualKinematics()
    manualKinematics.main()