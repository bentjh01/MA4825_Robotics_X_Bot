"""
contains specs, addresses, status and functions of a motor. 
MotorClass
- spec
- address
- node of Motor
- subscriber to Motion_topic eg {ID:1, Position:1000}
"""

import rospy
from xBotController.msg import *
from Configuration import Config
import os
config  = Config

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class AX1xA:
    # https://emanual.robotis.com/docs/en/dxl/ax/ax-12a/
    # https://emanual.robotis.com/docs/en/dxl/ax/ax-18a/
    def __init__(self, motor_name, motor_ID, portHandler, packetHandler):
        self.motor_name = motor_name
        self.motor_id = motor_ID
        self.portHandler = portHandler
        self.packetHandler = packetHandler
        self.specs()
        self.address()

    def specs(self):
        self.baude_rate = config.baude_rate # [bps]
        self.weight = 54.6 #[g]
        self.resolution = 0.29 # [deg]
        self.joint = True # False if endless a.k.a motor mode
        self.reduction_ratio = 254 
        self.stall_torque = 1.5 # [Nm]
        self.protocol_version = 1.0

    def address(self):
        # self.model_number_address = 0
        # self.firmware_version_address = 2
        # self.ID_address = 3
        # self.baude_rate_address = 4
        # self.return_delay_time_address = 5
        # self.cw_angle_limit_address = 6
        # self.ccw_angle_limit_address = 8
        # self.temp_limit_address = 11
        # self.min_voltage_address = 12
        # self.max_voltage_address = 13
        # self.max_torque_address = 14
        # self.status_return_level_address = 16
        # self.alarm_led_address = 17
        # self.shutdown_address = 18
        self.torque_enabled_address = 24
        # self.led_address = 25
        # self.cw_compliance_margin_address = 26
        # self.ccw_compliance_margin_address = 27
        # self.cw_compliance_slope_address = 28
        # self.ccw_compliance_slope_address = 29
        self.goal_position_address = 30
        # self.moving_speed_address = 32
        # self.torque_limit_address = 34
        self.present_position_address = 36
        # self.present_speed_address = 38
        # self.present_load_address = 40
        # self.present_volatage_address = 42
        # self.present_temperature_address = 43
        # self.registered_address = 44
        # self.moving_status_address = 46
        # self.lock_address = 47
        # self.punch_address = 48

    def parameter(self):
        self.torque_enabled = 1 # 1 for True, 0 for False
        self.dxl_min_position = 0
        self.dxl_max_position = 1000
        self.moving_status_threshold = 20
        self.position = 0

    def set_position_callback(self, data):
        if data.ID == self.motor_id:
            print("Set Goal Position of ID %s = %s" % (data.id, data.position))
            self.goal_position = data.position
            dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, self.motor_id, self.goal_position_address, data.position)

    def update_state(self, data):
        dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler, data.id, self.present_position_address)
        self.position = dxl_present_position

    def motor_spin(self):
        rospy.init_node(self.motor_name)
        rospy.Subscriber(config.set_position_topic, dxl, self.set_position_callback)
        rospy.Service('get_position', dxl, self.update_state)
        rospy.spin()

    def begin(self):
        # # Open port
        # try:
        #     self.portHandler.openPort()
        #     print("Succeeded to open the port")
        # except:
        #     print("Failed to open the port")
        #     print("Press any key to terminate...")
        #     getch()
        #     quit()

        # # Set port baudrate
        # try:
        #     portHandler.setBaudRate(self.baude_rate)
        #     print("Succeeded to change the baudrate")
        # except:
        #     print("Failed to change the baudrate")
        #     print("Press any key to terminate...")
        #     getch()
        #     quit()

        # Enable Dynamixel Torque
        dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, self.motor_id, self.torque_enabled_address, self.torque_enabled)
        if dxl_comm_result != 0:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            quit()
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            quit()
        else:
            print("DYNAMIXEL has been successfully connected")

        print("Ready to get & set Position.")

        self.motor_spin()