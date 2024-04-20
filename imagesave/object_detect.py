import tkinter as tk
import cv2
from PIL import Image, ImageTk
import torch
import time
import os  # os 모듈 추가

import pathlib 
from pathlib import Path
pathlib.PosixPath = pathlib.WindowsPath
# 모델을 로드할 때 force_reload=True 옵션을 사용하여 캐시를 다시 로드

model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/Users/USER/Desktop/yolo/yolov5-master/yolov5-master/yolov5s.pt', force_reload=True)
#model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:\\Users\\USER\\Desktop\\yolo\\yolo\\기말-데모\\serverbest.pt', force_reload=True)
import os
from datetime import datetime

class VideoBox:
    def __init__(self, address, frame, label, source, board):
        self.__check = 0
        self.__start = 0
        self.__end = 0
        self.__board_check = 0
        self.__address = address
        self.__video_frame = frame
        self.__video_label = label
        self.__source = source
        self.board = board
        self.capture_count = 0
        self.image_folder = "C:/Users/USER/Desktop/yolo/yolo/personimage"  # 이미지를 저장할 폴더 경로
        self.image_num = 0  # 이미지 번호 변수 추가

        # 이미지 저장을 위한 폴더 생성
        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)

    def main_page(self): 
        cap = cv2.VideoCapture(self.__source)

        def video_play():
            ret, frame = cap.read()
            if not ret:
                cap.release()
                return

            results = model(frame)

            human = 0
            for *xyxy, conf, cls in results.xyxy[0]:
                if conf > 0.85:  # 정확도가 85프로 이상인 경우에만 저장
                    label = f'{results.names[int(cls)]} {conf:.2f}'
                    cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (255,0,0), 2)
                    cv2.putText(frame, label, (int(xyxy[0]), int(xyxy[1])-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)
                    if results.names[int(cls)] == 'person':
                        detect_fall = 1
                        # 이미지 저장
                        self.image_num += 1  # 이미지 번호 증가
                        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
                        save_path = os.path.join(self.image_folder, f"image_{current_time}_{self.capture_count}.jpg")  # 각 이미지에 고유한 번호를 부여하여 저장
                        cv2.imwrite(save_path, frame)
                        self.capture_count += 1

            if len(results.xyxy[0]) == 0:
                self.__check = 0
                self.__start = 0
                self.__end = 0
                self.__board_check = 0
                self.__video_frame.config(bg='white')
            else:
                if human == 1:
                    if self.__check == 0:
                        self.__start = time.time()
                        self.__check = 1
                    else:
                        self.__end = time.time()

                    if 10 <= (self.__end - self.__start):
                        self.__video_frame.config(bg='red')
                        if self.__board_check == 0:
                            self.__check = 2
                            self.__board_check = 1
                            self.board.update_board(self.__address, self.__source)
                        else:
                            self.__check == 1
                else:
                    self.__check = 0
                    self.__start = 0
                    self.__end = 0
                    self.__board_check = 0
                    self.__video_frame.config(bg='white')

            video = frame
            cv2img = cv2.cvtColor(video, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2img)
            imgtk = ImageTk.PhotoImage(image=img)

            self.__video_label.imgtk = imgtk
            self.__video_label.configure(image=imgtk)

            self.__video_label.after(10, video_play)

        video_play()
