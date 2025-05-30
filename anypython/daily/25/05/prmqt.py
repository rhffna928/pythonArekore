import paho.mqtt.client as mqtt
import time
import collections

# --- 설정 (Configuration) ---
BROKER_ADDRESS = "223.130.131.234"  # MQTT 브로커 주소 (예: "localhost" 또는 "broker.hivemq.com")
BROKER_PORT = 31883           # MQTT 브로커 포트
TOPICS = [                   # 모니터링할 토픽 리스트
    ("#", 0),  # QoS 0으로 home/ 아래 모든 temperature 토픽 구독
    #("sensors/pressure", 1),    # QoS 1로 sensors/pressure 토픽 구독
    #("my/data/#", 0)            # QoS 0으로 my/data/ 아래 모든 하위 토픽 구독
]
# 토픽 설명:
# - "+"는 한 레벨의 와일드카드입니다. (예: home/livingroom/temperature, home/bedroom/temperature)
# - "#"는 여러 레벨의 와일드카드입니다. (예: my/data/sensor1, my/data/sub/sensor2)

# --- 전역 변수 (Global Variables) ---
message_counts = collections.defaultdict(int) # 각 토픽별 메시지 수를 저장
last_messages = {}                            # 각 토픽별 마지막 메시지 내용을 저장

# --- 콜백 함수 (Callback Functions) ---

# 브로커에 연결 성공 시 호출되는 함수
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("💡 MQTT 브로커에 성공적으로 연결되었습니다.")
        for topic, qos in TOPICS:
            client.subscribe(topic, qos)
            print(f"✅ 토픽 '{topic}' (QoS: {qos}) 구독 완료!")
    else:
        print(f"❌ MQTT 브로커 연결 실패: {rc}")

# 메시지가 도착할 때마다 호출되는 함수
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8') # 페이로드를 UTF-8 문자열로 디코딩
    
    message_counts[topic] += 1
    last_messages[topic] = payload
    
    # 터미널에 메시지 상태 업데이트
    print_status()

# --- 상태 출력 함수 (Status Print Function) ---

def print_status():
    # 터미널 클리어 (OS에 따라 동작하지 않을 수 있음)
    # import os
    # os.system('cls' if os.name == 'nt' else 'clear')

    print("\n" + "="*40)
    print("         MQTT 토픽 관제 현황")
    print("="*40)
    print(f"⏳ 현재 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 40)
    
    if not message_counts:
        print("아직 메시지가 도착하지 않았습니다. 기다리는 중...")
    else:
        print(f"{'토픽':<25} {'메시지 수':<10} {'마지막 메시지':<30}")
        print("-" * 70)
        for topic in sorted(message_counts.keys()):
            count = message_counts[topic]
            last_msg = last_messages[topic]
            # 메시지 내용이 너무 길면 자르기
            display_msg = (last_msg[:27] + '...') if len(last_msg) > 30 else last_msg
            print(f"{topic:<25} {count:<10} {display_msg:<30}")
    print("="*40)

# --- 메인 실행 블록 (Main Execution Block) ---

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        print(f"MQTT 브로커 {BROKER_ADDRESS}:{BROKER_PORT} 에 연결 시도 중...")
        client.connect(BROKER_ADDRESS, BROKER_PORT, 60) # 60초 타임아웃
        
        # 네트워크 루프 시작 (백그라운드에서 메시지 처리)
        client.loop_start() 
        
        # 주기적으로 상태를 업데이트하거나, Ctrl+C로 종료될 때까지 대기
        while True:
            time.sleep(5) # 5초마다 상태 출력 (메시지 도착 시 on_message에서 바로 출력됨)
            # print_status() # 주기적으로 출력하려면 주석 해제 (단, 메시지 올 때마다 출력 중복 가능성)

    except KeyboardInterrupt:
        print("\n👋 사용자 요청으로 스크립트를 종료합니다.")
    except Exception as e:
        print(f"🚨 오류 발생: {e}")
    finally:
        if client:
            client.loop_stop() # 네트워크 루프 중지
            client.disconnect() # 브로커 연결 해제
            print("🔗 MQTT 연결이 해제되었습니다.")