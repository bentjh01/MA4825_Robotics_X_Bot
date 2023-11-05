import rospy
from xbot_driver.Configuration import Config
from dynamixel_sdk import *
config  = Config()

class AX1xA:
    # https://emanual.robotis.com/docs/en/dxl/ax/ax-12a/
    # https://emanual.robotis.com/docs/en/dxl/ax/ax-18a/
    def __init__(self, motor_name, ID, portHandler):
        self.specs()
        self.address()
        self.motor_name = motor_name
        self.ID = ID
        self.portHandler = portHandler
        self.packetHandler = PacketHandler(self.protocol_version)
        self.parameter()

    def specs(self):
        self.baude_rate = config.baude_rate # [bps]
        self.weight = 54.6 #[g]
        self.resolution = 0.29 # [deg] Angle 0-300 mapped to 0-1023
        self.joint = True # False if endless a.k.a motor mode
        self.reduction_ratio = 254 
        self.stall_torque = 1.5 # [Nm]
        self.protocol_version = 1.0
        self.max_position = 1023

    def address(self):
        self.model_number_address = 0
        self.firmware_version_address = 2
        self.ID_address = 3
        self.baude_rate_address = 4
        self.return_delay_time_address = 5
        self.cw_angle_limit_address = 6
        self.ccw_angle_limit_address = 8
        self.temp_limit_address = 11
        self.min_voltage_address = 12
        self.max_voltage_address = 13
        self.max_torque_address = 14
        self.status_return_level_address = 16
        self.alarm_led_address = 17
        self.shutdown_address = 18
        self.torque_enabled_address = 24
        self.led_address = 25
        self.cw_compliance_margin_address = 26
        self.ccw_compliance_margin_address = 27
        self.cw_compliance_slope_address = 28
        self.ccw_compliance_slope_address = 29
        self.goal_position_address = 30
        self.moving_speed_address = 32
        self.torque_limit_address = 34
        self.present_position_address = 36
        self.present_speed_address = 38
        self.present_load_address = 40
        self.present_volatage_address = 42
        self.present_temperature_address = 43
        self.registered_address = 44
        self.moving_status_address = 46
        self.lock_address = 47
        self.punch_address = 48

    def parameter(self):
        self.model_number = self.get_model_number()
        # self.firmware_version = 
        # self.ID = 
        self.baude_rate = self.get_baude_rate()
        # self.return_delay_time =
        self.cw_angle_limit = 0
        self.ccw_angle_limit = 0
        # self.temp_limit = 
        # self.min_voltage = 
        # self.max_voltage = 
        # self.max_torque = 
        # self.status_return_level = 
        # self.alarm_led = 
        # self.shutdown = 
        self.torque_enabled = 1 # 1 for True, 0 for False
        self.led = 0
        # self.cw_compliance_margin = 
        # self.ccw_compliance_margin = 
        # self.cw_compliance_slope = 
        # self.ccw_compliance_slope = 
        self.goal_position = 0
        self.moving_speed = 64
        # self.torque_limit = 
        self.present_position = self.get_position()
        # self.present_speed = 
        # self.present_load = 
        # self.present_volatage = 
        # self.present_temperature = 
        # self.registered = 
        # self.moving_status = 
        # self.lock = 
        # self.punch = 

    def set_goal_position(self, goal_position):
        self.goal_position = goal_position
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.ID, self.goal_position_address, self.goal_position)
        # print(f'{self.ID} position {self.goal_position}')

    def set_moving_speed(self, moving_speed = 128):
        self.moving_speed = moving_speed
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.ID, self.moving_speed_address, self.moving_speed)
        # print(f'{self.ID} speed {self.moving_speed}')

    def set_cw_ccw_limits(self, cw_limit = None, ccw_limit = None):
        # if both zero, then wheel mode enabled
        if cw_limit is not None:
            self.cw_angle_limit = cw_limit
        if ccw_limit is not None:
            self.ccw_angle_limit = ccw_limit
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.ID, self.cw_angle_limit_address, self.cw_angle_limit)
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.ID, self.ccw_angle_limit_address, self.ccw_angle_limit)

    def set_torque_mode(self, torque_enabled):
        if torque_enabled:
            self.torque_enabled = 1
        else:
            self.torque_enabled = 0
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.ID, self.torque_enabled_address, self.torque_enabled)
        if dxl_comm_result != 0:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print("DYNAMIXEL has been successfully connected")

    def set_led(self, led_enabled):
        if led_enabled:
            self.led = 1
        else:
            self.led = 0
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.ID, self.led_address, self.led)

    def get_position(self):
        dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.ID, self.present_position_address)
        self.present_position = dxl_present_position
        return dxl_present_position
    
    def get_baude_rate(self):
        dxl_baude_rate, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.portHandler, self.ID, self.baude_rate_address)
        self.baude_rate = dxl_baude_rate
        return dxl_baude_rate
    
    def get_model_number(self):
        dxl_model_number, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.ID, self.model_number_address)
        return dxl_model_number
    
    def get_moving(self):
        dxl_moving_status, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.portHandler, self.ID, self.moving_status_address)
        return dxl_moving_status

    # def get_error(self):
    #     dxl_moving_status, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.portHandler, self.ID, self.moving_status_address)
    #     return dxl_moving_status