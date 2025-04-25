#09.20 실행
#IG
import socket
import json
import time
from datetime import datetime
import pandas as pd
import paho.mqtt.client as mqtt
import psycopg2

def receive_data():
    host = '172.30.1.40'
    port = 9999
    buffer = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"Connected to {host}:{port}")
        while True:
            data = s.recv(4096)
            if not data:
                break
            buffer += data.decode('utf-8')
            while True:
                try:
                    obj, idx = json.JSONDecoder().raw_decode(buffer)
                    buffer = buffer[idx:].lstrip()
                    yield obj
                except json.JSONDecodeError:
                    break

# 평균값 계산
def calculate_average(data_points):
    if not data_points:
        return {}
    vehicle_data = []
    location_data = []
    for batch in data_points:
        for item in batch:
            if item['type'] == 'VEHICLE_INFO':
                vehicle_data.append(item['data'])
            if item['type'] == 'LOCATION':
                location_data.append(item['data'])
                
    vehicle_df = pd.DataFrame(vehicle_data)
    location_df = pd.DataFrame(location_data)
    location_df.columns = ['accel', 'autoDrivingStatus', 'brake', 'brakeStatus', 'drivingDistance',
       'emergencyLight', 'mdpsAngle', 'transmission', 'turnSignal',
       'wheelSpeed', 'yawRate', 'l_latitude', 'l_longitude']
    
    
    comm_df = pd.concat([vehicle_df,location_df],axis=1)
    comm_df = comm_df.apply(pd.to_numeric, errors='coerce')
    comm_df = comm_df.mean()
    comm_df['v_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    comm_df['l_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    comm_df['vehicle_id'] = 'STSW000002'
    comm_df['vehicle_type'] = 'S'

    comm_df = comm_df.to_json()
    avg_data = [comm_df]
    print(avg_data)
    
    return avg_data    

#mqtt 발행
def send_to_cloud(avg_data):
    broker_address = "223.130.131.234"
    port = 31883
    topic = "special_vehicle/data"

    client = mqtt.Client("EdgeNode")
    client.connect(broker_address, port)
    client.publish(topic, json.dumps(avg_data))
    client.disconnect()
                
def process_data():
    data_points = []
    start_time = time.time()

    for data in receive_data():
        data_points.append(data)
        #save_to_db(data)
        #print(data)
        if time.time() - start_time >= 1:
            avg_data = calculate_average(data_points)
            send_to_cloud(avg_data)
            data_points = []            
            start_time = time.time()

if __name__ == "__main__":
    process_data()