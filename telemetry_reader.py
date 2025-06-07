from pymavlink import mavutil
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Change this to your connection string:
udp = 'udp:127.0.0.1:14551'
connection_string = '/dev/ttyACM0' #'/dev/ttyACM0'  # or 'udp:127.0.0.1:14551'
baud = 57600

# Connect to the flight controller
master = mavutil.mavlink_connection(connection_string, baud=baud)

# Wait for a heartbeat to confirm connection
master.wait_heartbeat()
print(f"Connected to system {master.target_system}, component {master.target_component}")

lat_list = []
lon_list = []
alt_list = []
imu_roll_list = []
imu_pitch_list = []
imu_yaw_list = []

plt.figure(figsize=(10, 8))
plt.ion()

# Loop to read GPS and IMU data
while True:

    msg = master.recv_match(type=['GPS_RAW_INT', 'ATTITUDE'], blocking=True)
    if not msg:
        continue

    if msg.get_type() == 'GPS_RAW_INT':
        lat = msg.lat / 1e7
        lon = msg.lon / 1e7
        alt = msg.alt / 1000

        lat_list.append(lat)
        lon_list.append(lon)
        alt_list.append(alt)
        print(f"GPS | Lat: {lat}, Lon: {lon}, Alt: {alt} m")

    if msg.get_type() == 'ATTITUDE':
        roll = msg.roll
        pitch = msg.pitch
        yaw = msg.yaw

        imu_roll_list.append(roll)
        imu_pitch_list.append(pitch)
        imu_yaw_list.append(yaw)
        print(f"IMU | Roll: {roll:.2f}, Pitch: {pitch:.2f}, Yaw: {yaw:.2f}")

    if msg.get_type() == 'GPS_RAW_INT':
        print(f"GPS | Lat: {msg.lat / 1e7}, Lon: {msg.lon / 1e7}, Alt: {msg.alt / 1000} m")
    elif msg.get_type() == 'ATTITUDE':
        print(f"IMU | Roll: {msg.roll:.2f}, Pitch: {msg.pitch:.2f}, Yaw: {msg.yaw:.2f}")

    # plotting the live data
    plt.clf()
    if lat_list and lon_list:
        plt.subplot(2, 1, 1)
        plt.plot(lon_list, lat_list, marker='o', linestyle='-', color='b')
        plt.title('GPS Position')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.grid()
    if imu_roll_list and imu_pitch_list and imu_yaw_list:
        plt.subplot(2, 1, 2)
        plt.plot(imu_roll_list, label='Roll', color='r')
        plt.plot(imu_pitch_list, label='Pitch', color='g')
        plt.plot(imu_yaw_list, label='Yaw', color='b')
        plt.title('IMU Attitude')
        plt.xlabel('Sample Number')
        plt.ylabel('Angle (degrees)')
        plt.legend()
        plt.grid()

    plt.tight_layout()
    plt.pause(0.1)

    '''if msg.get_type() == 'GPS_RAW_INT':
        print(f"GPS | Lat: {msg_data['GPS_RAW_INT']['lat']}, Lon: {msg_data['GPS_RAW_INT']['lon']}, Alt: {msg_data['GPS_RAW_INT']['alt']} m")
    elif msg.get_type() == 'ATTITUDE':
        print(f"IMU | Roll: {msg_data['ATTITUDE']['IMU']:.2f}, Pitch: {msg_data['ATTITUDE']['pitch']:.2f}, Yaw: {msg_data['ATTITUDE']['yaw']:.2f}")'''
