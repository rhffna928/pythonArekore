from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import time
from collections import deque
import threading
import paho.mqtt.client as mqtt
import json

# 그래프 설정
fig = plt.figure()
ax = plt.axes(xlim=(0, 50), ylim=(0, 20))
line, = ax.plot([], [], lw=1, c='blue', marker='d', ms=3)

max_points = 50
x = np.arange(max_points)
ydata = deque([np.nan]*max_points, maxlen=max_points)

# MQTT 토픽 통계
latest_value = {"value": 0.0}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ MQTT 연결 성공")
        client.subscribe("#")  # 전체 구독
    else:
        print(f"❌ MQTT 연결 실패: {rc}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        
        # 원하는 값 추출 (예: heading, speed 등)
        if isinstance(data, dict) and "data" in data and "heading" in data["data"]:
            latest_value["value"] = float(data["data"]["heading"])
    except Exception as e:
        print(f"⚠️ 메시지 처리 오류: {e}")

def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("223.130.131.234", 31883, 60)
    client.loop_forever()

def init():
    line.set_ydata([np.nan]*max_points)
    return line,

def animate(frame):
    y = start_mqtt()
    ydata.append(y)
    line.set_ydata(ydata)
    return line,

# 애니메이션 설정
anim = animation.FuncAnimation(
    fig, animate, init_func=init,
    frames=None, interval=200, blit=True
)
plt.show()
if __name__ == "__main__":
    mqtt_thread = threading.Thread(target=start_mqtt, daemon=True)
    mqtt_thread.start()
    
