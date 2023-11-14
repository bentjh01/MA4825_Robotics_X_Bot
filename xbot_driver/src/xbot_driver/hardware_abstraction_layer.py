from dynamixel_sdk import *

class Config:
    def __init__(self):
        self.set_position_topic = "set_position"
        self.baude_rate = 1000000
        self.device_name = '/dev/ttyUSB0'
        self.protocol_version = 1.0
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
        self.joint = True # False if endless a.k.a motor mode
        self.reduction_ratio = 254 
        self.stall_torque = 1.5 # [Nm]
        self.protocol_version = 1.0
        self.max_position = 1023 # uint10
        self.position_resolution_deg = 0.29297 # [deg/ count]
        self.position_range_deg = 299.71# [deg]
        self.speed_resolution_rpm = 0.111 # [rpm/count]
        self.speed_range_rpm = 113.553 # [rpm]

    def address(self):
        # get only
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
        # set and get
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
        # self.model_number = self.get_model_number()
        # self.firmware_version = 
        # self.ID = 
        # self.baude_rate = self.get_baude_rate()
        # self.return_delay_time =
        # self.cw_angle_limit = 0
        # self.ccw_angle_limit = 0
        # self.temp_limit = 
        # self.min_voltage = 
        # self.max_voltage = 
        # self.max_torque = 
        # self.status_return_level = 
        # self.alarm_led = 
        # self.shutdown = 

        self.torque_enabled = 1 # 1 for True, 0 for False
        self.led_enabled = 1
        # self.cw_compliance_margin = 
        # self.ccw_compliance_margin = 
        # self.cw_compliance_slope = 
        # self.ccw_compliance_slope = 
        self.goal_position = None
        self.moving_speed = None
        # self.torque_limit = 
        # self.present_position = self.get_position()
        # self.present_speed = 
        # self.present_load = 
        # self.present_volatage = 
        # self.present_temperature = 
        # self.registered = 
        # self.moving_status = self.get_moving_status()
        # self.lock = 
        # self.punch = 

    def set_goal_position(self, goal_position):
        if goal_position == self.goal_position:
            print('no change in set_goal')
            return
        self.goal_position = goal_position
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.ID, self.goal_position_address, self.goal_position)
        if dxl_comm_result != 0:
            print(f'FAILED to set_goal_position = {goal_position} {self.packetHandler.getTxRxResult(dxl_comm_result)}')
        elif dxl_error != 0:
            print(f'FAILED to set_goal_position = {goal_position} {self.packetHandler.getRxPacketError(dxl_error)}')
        else:
            print(f"SUCCESS Change goal position to {self.goal_position}")
            
    def set_moving_speed(self, moving_speed):
        if moving_speed == self.moving_speed:
            print('no change in move_speed')
            return
        self.moving_speed = moving_speed
        dxl_comm_result, dxl_error = self.packetHandler.write2ByteTxRx(self.portHandler, self.ID, self.moving_speed_address, self.moving_speed)
        if dxl_comm_result != 0:
            print(f'FAILED to set moving_speed = {moving_speed} {self.packetHandler.getTxRxResult(dxl_comm_result)}')
        elif dxl_error != 0:
            print(f'FAILED to set moving_speed = {moving_speed} {self.packetHandler.getRxPacketError(dxl_error)}')
        else:
            print(f"SUCCESS Change moving speed to {self.moving_speed}")

    def set_torque_enabled(self, torque_enabled = 1):
        if torque_enabled == self.torque_enabled:
            return
        self.torque_enabled = torque_enabled
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.ID, self.torque_enabled_address, self.torque_enabled)
        if dxl_comm_result != 0:
            print(f'FAILED to set torque_enabled = {torque_enabled} {self.packetHandler.getTxRxResult(dxl_comm_result)}')
        elif dxl_error != 0:
            print(f'FAILED to set torque_enabled = {torque_enabled} {self.packetHandler.getRxPacketError(dxl_error)}')
        else:
            print(f"SUCCESS Change torque enabled to {self.torque_enabled}")

    # def set_led_enabled(self, led_enabled = 1):
    #     if led_enabled == self.led_enabled:
    #         return
    #     self.led_enabled = led_enabled
    #     dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.ID, self.led_address, self.led_enabled)
    #     if dxl_comm_result != 0:
    #         print(f'FAILED to set torque_enabled = {led_enabled} {self.packetHandler.getTxRxResult(dxl_comm_result)}')
    #     elif dxl_error != 0:
    #         print(f'FAILED to set torque_enabled = {led_enabled} {self.packetHandler.getRxPacketError(dxl_error)}')
    #     else:
    #         print(f"SUCCESS Change LED enabled to {self.led_enabled}")

    def get_position(self):
        dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.ID, self.present_position_address)
        if dxl_comm_result != 0:
            print("FAILED %s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("FAILED %s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            self.present_position = dxl_present_position
            return dxl_present_position
    
    def get_moving_status(self):
        dxl_moving_status, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.portHandler, self.ID, self.moving_status_address)
        if dxl_comm_result != 0:
            print("FAILED %s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("FAILED %s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            self.moving_status = dxl_moving_status
            return dxl_moving_status
    
    # def get_baude_rate(self):
    #     dxl_baude_rate, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.portHandler, self.ID, self.baude_rate_address)
    #     self.baude_rate = dxl_baude_rate
    #     return dxl_baude_rate
    
    # def get_model_number(self):
    #     dxl_model_number, dxl_comm_result, dxl_error = self.packetHandler.read2ByteTxRx(self.portHandler, self.ID, self.model_number_address)
    #     return dxl_model_number


import math
import numpy as np

def radian__2__degree(radian:float):
    if radian is None:
        print(f'Received {type(radian)}, Expected float')
        return
    degree = radian/math.pi * 180
    return float(degree)

def degree__2__radian(degree:float):
    if degree is None:
        print(f'Received {type(float)}, Expected float')
        return
    radian = degree/180 * math.pi
    return float(radian)

def rpm__2__radian_second(rpm):
    radian_second = rpm/60*math.pi
    return float(radian_second)

def radian_second__2__rpm(radian_second):
    rpm = radian_second*60/math.pi
    return float(rpm)

# def uint102degree(uint10):
#     degree = np.interp(uint10, [0,1023], [-150, 149.71])
#     degree = round(round(degree/0.29)*0.29,2)
#     return float(degree)

def radian2uint10(radian):
    degree = radian__2__degree(radian)
    uint10 = np.interp(degree, [-150,149.71], [0, 1024])
    return int(uint10)

def uint102radian(uint10):
    degree = np.interp(uint10, [0,1023], [-150, 149.71])
    radian = round(degree__2__radian(round(round(degree/0.29297)*0.29297,2)),4)
    return float(radian)

def radian_second2uint10(radian_second):
    if radian_second is None:
        return 0.01
    rpm = radian_second__2__rpm(radian_second)
    uint10 = round(rpm/0.111)
    return int(uint10)

def uint102radian_second(uint10):
    rpm = np.interp(uint10, [0,1023], [0.111, 113.553])
    radian_second = round(radian_second__2__rpm(rpm), 2)
    return float(radian_second)