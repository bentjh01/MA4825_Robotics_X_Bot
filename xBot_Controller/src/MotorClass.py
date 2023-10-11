"""
contains specs, addresses, status and functions of a motor. 
"""

class AX1xA:
    # https://emanual.robotis.com/docs/en/dxl/ax/ax-12a/
    # https://emanual.robotis.com/docs/en/dxl/ax/ax-18a/
    def __init__(self):
        self.specs()
        self.address()

    def specs(self):
        self.baude_rate = 1000000 # [bps]
        self.weight = 54.6 #[g]
        self.resolution = 0.29 # [deg]
        self.joint = True # False if endless a.k.a motor mode
        self.reduction_ratio = 254 
        self.stall_torque = 1.5 # [Nm]\
        self.protocol_version = 1.0

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

    # def load_config