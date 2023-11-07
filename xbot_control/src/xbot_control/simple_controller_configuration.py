import numpy as np

class Config():
    def __init__(self):
        self.max_speed_limit = 1.5 # [rad/s]
        self.min_speed_limit = 0.3 # [rad/s]
        self.speed_linspace = np.linspace(self.max_speed_limit, self.min_speed_limit, 10)

        #TODO-obtain minimum and maximum physical angles
        self.joint_1_range = [] # [min, max] [rad]
        self.joint_2_range = [] # [min, max] [rad]
        self.joint_3_range = [] # [min, max] [rad]
        self.joint_4_range = [] # [min, max] [rad]
        self.joint_5_range = [] # [min, max] [rad]
        
        self.joint_ranges = [self.joint_1_range, self.joint_2_range, 
                             self.joint_3_range, self.joint_4_range,
                             self.joint_5_range]
        
        #TODO-obtain optimal value
        self.store_retrieve_offset = 0.26 
        #TODO-obtain optimal value
        self.gravity_offset = 0.26