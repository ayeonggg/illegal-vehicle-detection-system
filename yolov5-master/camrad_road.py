import torch
import cv2
import numpy as np
import serial
import time

# 파일 경로 설정
image_path = "C:/Users/USER/Desktop/yolo/yolov5-master/KakaoTalk_20240605_145012622.jpg"

# YOLO 모델 설정
yolo_weights = "C:/Users/USER/Desktop/yolo/yolov5-master/parkingspace_result_best.pt"  # YOLO 모델 가중치 파일 경로

# 시리얼 포트 설정
serial_port = 'COM3'  # Windows에서는 'COMx', Linux에서는 '/dev/ttyUSBx' 또는 '/dev/ttyACMx'
baud_rate = 9600
timeout_duration = 2  # 타임아웃 설정

# 카메라 화각 (도)
camera_fov = 60

# 카메라의 수평 해상도
camera_horizontal_resolution = 1920  # 가로 픽셀

# LiDAR 데이터 읽기 함수
def read_lidar_data():
    with serial.Serial(serial_port, baud_rate, timeout=timeout_duration) as ser:
        while True:
            if ser.in_waiting > 0:
                try:
                    line = ser.readline().decode('utf-8').strip()  # utf-8로 디코딩
                    print(f"수신한 데이터: {line}")  # 디버깅용 출력
                    if "거리" in line:
                        dist_part = line.split("거리 =")[1].strip().split()[0]  # 거리 부분 추출
                        dist = int(dist_part)
                        return dist
                except (ValueError, UnicodeDecodeError) as e:
                    print(f"라인 읽기 오류: {e}")
                    continue 
            else:
                print("수신 데이터 없음, 대기 중...")
                time.sleep(1)

# 도로의 실제 면적 계산 함수
def calculate_real_area(lidar_distance, camera_fov, camera_horizontal_resolution):
    lidar_distance_max = lidar_distance  # LiDAR로 측정된 최대 거리로 설정
    lidar_distance_min = lidar_distance * 0.6  # LiDAR로 측정된 최소 거리 설정 (예시)

    lidar_distance_ratio = lidar_distance_min / lidar_distance_max  # LiDAR 거리의 최소-최대 비율

    # 카메라의 세로 해상도 계산
    camera_vertical_resolution = camera_horizontal_resolution / np.tan(np.radians(camera_fov / 2))

    # 카메라의 실제 세로 길이 계산
    camera_height_real = lidar_distance_max * lidar_distance_ratio * camera_vertical_resolution / camera_horizontal_resolution

    # 카메라의 가로 길이 계산
    camera_width = 2 * lidar_distance_max * np.tan(np.radians(camera_fov / 2))

    # 도로의 실제 면적 계산 (가로 길이 * 세로 길이)
    road_area_real = camera_width * camera_height_real

    return road_area_real

# YOLO 모델을 로드하고 도로를 인식하는 함수
def detect_road(image_path):
    # YOLOv5 모델 로드
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    
    # 이미지 로드
    img = cv2.imread(image_path)
    
    # 추론 수행
    results = model(img)
    
    # 도로 박스 추출
    road_boxes = []
    for *xyxy, conf, cls in results.xyxy[0]:
        if int(cls) == 7:  # 클래스 7이 도로 클래스라 가정
            road_boxes.append([int(x) for x in xyxy])
    
    return road_boxes, img

# 메인 함수
def main():
    while True:
        # LiDAR 데이터 읽기
        lidar_distance = read_lidar_data()
        if lidar_distance:
            print(f"LiDAR 거리: {lidar_distance} 미터")
        
            # 실제 도로 면적 계산
            road_area_real = calculate_real_area(lidar_distance, camera_fov, camera_horizontal_resolution)
            
            # 출력 포맷으로 변경
            print(f"LiDAR 거리: {lidar_distance} 미터, 실제 도로 면적: {road_area_real:.2f} 제곱미터")
        
        # 잠시 대기
        time.sleep(1)

# 메인 함수 실행
if __name__ == "__main__":
    main()
