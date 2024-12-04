import socket
import struct
import math
import os

"""
To read ardupilot sitl values accurately you need to modify the following code piece:
ardupilot/libraries/AP_HAL_SITL/SITL_State.cpp

Find the function below:
void SITL_State::_output_to_flightgear(void)

Comment the section below in this function
fdm.ByteSwap();

"""

clear = lambda: os.system('cls')

class FGNetFDM:
    def __init__(self):
        # Define the format string for unpacking
        self.fmt = '<'  # Little-endian format
        self.fmt += 'II'  # 2 uint32_t: version, padding
        self.fmt += 'dd'  # 2 double: longitude, latitude
        self.fmt += 'df'  # 1 double, 1 float: altitude, agl
        self.fmt += 'fff'  # 3 float: phi, theta, psi
        self.fmt += 'fff'  # 3 float: alpha, beta, phidot
        self.fmt += 'fff'  # 3 float: thetadot, psidot, vcas
        self.fmt += 'f'  # 1 float: climb_rate
        self.fmt += 'fff'  # 3 float: v_north, v_east, v_down
        self.fmt += 'fff'  # 3 float: v_body_u, v_body_v, v_body_w
        self.fmt += 'fff'  # 3 float: A_X_pilot, A_Y_pilot, A_Z_pilot
        self.fmt += 'ff'  # 2 float: stall_warning, slip_deg
        self.fmt += 'I'  # 1 uint32_t: num_engines
        self.fmt += '4I'  # 4 uint32_t: eng_state
        self.fmt += '4f'  # 4 float: rpm
        self.fmt += '4f'  # 4 float: fuel_flow
        self.fmt += '4f'  # 4 float: fuel_px
        self.fmt += '4f'  # 4 float: egt
        self.fmt += '4f'  # 4 float: cht
        self.fmt += '4f'  # 4 float: mp_osi
        self.fmt += '4f'  # 4 float: tit
        self.fmt += '4f'  # 4 float: oil_temp
        self.fmt += '4f'  # 4 float: oil_px
        self.fmt += 'I'  # 1 uint32_t: num_tanks
        self.fmt += '4f'  # 4 float: fuel_quantity
        self.fmt += 'I'  # 1 uint32_t: num_wheels
        self.fmt += '3I'  # 3 uint32_t: wow
        self.fmt += '3f'  # 3 float: gear_pos
        self.fmt += '3f'  # 3 float: gear_steer
        self.fmt += '3f'  # 3 float: gear_compression
        self.fmt += 'I'  # 1 uint32_t: cur_time
        self.fmt += 'i'  # 1 int32_t: warp
        self.fmt += 'f'  # 1 float: visibility
        self.fmt += 'ffffffffff'  # 10 float: control inputs

    def unpack(self, data):
        # Unpack the data using the defined format
        unpacked_data = struct.unpack(self.fmt, data)

        # Assign the unpacked values to the corresponding class attributes
        self.version = unpacked_data[0]
        self.padding = unpacked_data[1]
        self.longitude = unpacked_data[2]
        self.latitude = unpacked_data[3]
        self.altitude = unpacked_data[4]
        self.agl = unpacked_data[5]
        self.phi = unpacked_data[6]
        self.theta = unpacked_data[7]
        self.psi = unpacked_data[8]
        self.alpha = unpacked_data[9]
        self.beta = unpacked_data[10]
        self.phidot = unpacked_data[11]
        self.thetadot = unpacked_data[12]
        self.psidot = unpacked_data[13]
        self.vcas = unpacked_data[14]
        self.climb_rate = unpacked_data[15]
        self.v_north = unpacked_data[16]
        self.v_east = unpacked_data[17]
        self.v_down = unpacked_data[18]
        self.v_body_u = unpacked_data[19]
        self.v_body_v = unpacked_data[20]
        self.v_body_w = unpacked_data[21]
        self.A_X_pilot = unpacked_data[22]
        self.A_Y_pilot = unpacked_data[23]
        self.A_Z_pilot = unpacked_data[24]
        self.stall_warning = unpacked_data[25]
        self.slip_deg = unpacked_data[26]
        self.num_engines = unpacked_data[27]
        self.eng_state = unpacked_data[28:32]
        self.rpm = unpacked_data[32:36]
        self.fuel_flow = unpacked_data[36:40]
        self.fuel_px = unpacked_data[40:44]
        self.egt = unpacked_data[44:48]
        self.cht = unpacked_data[48:52]
        self.mp_osi = unpacked_data[52:56]
        self.tit = unpacked_data[56:60]
        self.oil_temp = unpacked_data[60:64]
        self.oil_px = unpacked_data[64:68]
        self.num_tanks = unpacked_data[68]
        self.fuel_quantity = unpacked_data[69:73]
        self.num_wheels = unpacked_data[73]
        self.wow = unpacked_data[74:77]
        self.gear_pos = unpacked_data[77:80]
        self.gear_steer = unpacked_data[80:83]
        self.gear_compression = unpacked_data[83:86]
        self.cur_time = unpacked_data[86]
        self.warp = unpacked_data[87]
        self.visibility = unpacked_data[88]
        self.elevator = unpacked_data[89]
        self.elevator_trim_tab = unpacked_data[90]
        self.left_flap = unpacked_data[91]
        self.right_flap = unpacked_data[92]
        self.left_aileron = unpacked_data[93]
        self.right_aileron = unpacked_data[94]
        self.rudder = unpacked_data[95]
        self.nose_wheel = unpacked_data[96]
        self.speedbrake = unpacked_data[97]
        self.spoilers = unpacked_data[98]

# UDP Socket Setup
UDP_IP = "127.0.0.1"  # Replace with the actual IP address of the C++ server
UDP_PORT = 5503

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)  # Adjust buffer size as needed
    hex_string = ':'.join(hex(byte)[2:] for byte in data)
    #print(hex_string)
    fdm_data = FGNetFDM()
    fdm_data.unpack(data)

    # Now you can access the unpacked data:
    print("Longitude    :", fdm_data.longitude * (180.0 / math.pi), "°")
    print("Latitude     :", fdm_data.latitude * (180.0 / math.pi), "°")
    print("Altitude     :", fdm_data.altitude, "m")
    print("AGL          :", fdm_data.agl, "m")
    print("Roll         :", fdm_data.phi * (180.0 / math.pi), "°")
    print("Pitch        :", fdm_data.theta * (180.0 / math.pi), "°")
    print("Yaw          :", fdm_data.psi * (180.0 / math.pi), "°")
    clear()
    # ... (access other attributes as needed)