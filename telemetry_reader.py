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

    if msg.get_type() == 'GPS_RAW_INT':
        print(f"GPS | Lat: {msg.lat / 1e7}, Lon: {msg.lon / 1e7}, Alt: {msg.alt / 1000} m")
    elif msg.get_type() == 'ATTITUDE':
        print(f"IMU | Roll: {msg.roll:.2f}, Pitch: {msg.pitch:.2f}, Yaw: {msg.yaw:.2f}")
