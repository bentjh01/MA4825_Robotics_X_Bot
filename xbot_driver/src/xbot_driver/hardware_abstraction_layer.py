import math
import numpy as np
from motor_class import AX1xA

motorClass = AX1xA()

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
#     degree = np.interp(uint10, [0,1023], [-motorClass.half_position_range_deg, motorClass.half_position_range_deg])
#     degree = round(round(degree/0.29)*0.29,2)
#     return float(degree)

def radian2uint10(radian):
    degree = radian__2__degree(radian)
    uint10 = round(degree/motorClass.position_resolution_deg)
    return int(uint10)

def uint102radian(uint10):
    degree = np.interp(uint10, [0,1023], [-motorClass.half_position_range_deg, motorClass.half_position_range_deg])
    radian = round(degree__2__radian(round(round(degree/motorClass.position_resolution_deg)*motorClass.position_resolution_deg,2)),4)
    return float(radian)

def radian_second2uint10(radian_second):
    rpm = rpm__2__radian_second(radian_second)
    uint10 = round(rpm/motorClass.speed_resolution_rpm)
    return int(uint10)

def uint102radian_second(uint10):
    rpm = np.interp(uint10, [0,1023], [0, motorClass.speed_range_rpm])
    radian_second = round(radian_second__2__rpm(rpm), 2)
    return float(radian_second)