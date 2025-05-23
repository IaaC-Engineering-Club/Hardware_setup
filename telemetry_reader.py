from pymavlink import mavutil

# Change this to your connection string:
connection_string = '/dev/ttyACM0'  # or 'udp:192.168.x.x:14550'
baud = 57600

# Connect to the flight controller
master = mavutil.mavlink_connection(connection_string, baud=baud)

# Wait for a heartbeat to confirm connection
master.wait_heartbeat()
print(f"Connected to system {master.target_system}, component {master.target_component}")

# Loop to read GPS and IMU data
while True:
    msg = master.recv_match(type=['GPS_RAW_INT', 'ATTITUDE'], blocking=True)
    if not msg:
        continue

    msg_data = {
        'GPS_RAW_INT':{
        'time_usec': msg.time_usec,
        'lat': msg.lat / 1e7,
        'lon': msg.lon / 1e7,
        'alt': msg.alt / 1000,
        },
        'ATTITUDE':{
            'IMU': msg.roll,
            'pitch': msg.pitch,
            'yaw': msg.yaw
        }

    }

    if msg.get_type() == 'GPS_RAW_INT':
        print(f"GPS | Lat: {msg_data['GPS_RAW_INT']['lat']}, Lon: {msg_data['GPS_RAW_INT']['lon']}, Alt: {msg_data['GPS_RAW_INT']['alt']} m")
    elif msg.get_type() == 'ATTITUDE':
        print(f"IMU | Roll: {msg_data['ATTITUDE']['IMU']:.2f}, Pitch: {msg_data['ATTITUDE']['pitch']:.2f}, Yaw: {msg_data['ATTITUDE']['yaw']:.2f}")

'''    if msg.get_type() == 'GPS_RAW_INT':
        print(f"GPS | Lat: {msg.lat / 1e7}, Lon: {msg.lon / 1e7}, Alt: {msg.alt / 1000} m")
    elif msg.get_type() == 'ATTITUDE':
        print(f"IMU | Roll: {msg.roll:.2f}, Pitch: {msg.pitch:.2f}, Yaw: {msg.yaw:.2f}")'''
