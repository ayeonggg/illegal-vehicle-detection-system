import socket
import cv2
import numpy as np
import base64
import time
from datetime import datetime
import sys
import tkinter as tk
from PIL import Image, ImageTk
import torch
import os
import pathlib 
from pathlib import Path
pathlib.PosixPath = pathlib.WindowsPath

model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/Users/USER/Desktop/yolo/yolov5-master/yolov5-master/yolov5s.pt', force_reload=True)
class ClientSocket:
    def __init__(self, address, frame, label, source, board, ip='13.125.205.111', port=8080):
        self.address = address
        self.TCP_SERVER_IP = ip
        self.TCP_SERVER_PORT = port
        self.connectCount = 0
        self.connectServer()

    def connectServer(self):
        while True:
            try:
                self.sock = socket.socket()
                self.sock.connect((self.TCP_SERVER_IP, self.TCP_SERVER_PORT))
                print(u'Client socket is connected with Server socket [ TCP_SERVER_IP: ' + self.TCP_SERVER_IP + ', TCP_SERVER_PORT: ' + str(self.TCP_SERVER_PORT) + ' ]')
                self.connectCount = 0
                self.sendImages()
                break  # 연결이 성공했으므로 while 루프 종료
            except Exception as e:
                print(e)
                self.connectCount += 1
                if self.connectCount == 10:
                    print(u'Connect fail %d times. exit program'%(self.connectCount))
                    sys.exit()
                print(u'%d times try to connect with server'%(self.connectCount))
                time.sleep(1)  # 재연결을 시도하기 전에 잠시 대기
            self.connectServer()
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
                        now = datetime.now()
                        current_time = now.strftime("%Y%m%d%H%M%S")
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
            
    def sendImages(self):
        cnt = 0
        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 315)
        try:
            while capture.isOpened():
                ret, frame = capture.read()
                resize_frame = cv2.resize(frame, dsize=(480, 315), interpolation=cv2.INTER_AREA)

                now = time.localtime()
                stime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')

                encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
                result, imgencode = cv2.imencode('.jpg', resize_frame, encode_param)
                data = np.array(imgencode)
                stringData = base64.b64encode(data)
                length = str(len(stringData))

                # Send length of the string data
                self.sock.sendall(length.encode('utf-8').ljust(64))
                # Send string data itself
                self.sock.send(stringData)
                # Send timestamp
                self.sock.send(stime.encode('utf-8').ljust(64))
                print(u'send images %d'%(cnt))
                cnt+=1
                time.sleep(0.095)
        except Exception as e:
            print(e)
            self.sock.close()
            time.sleep(1)
            self.connectServer()
            self.sendImages()

def main():
    TCP_IP = '13.125.205.111'
    TCP_PORT = 8080
    client = ClientSocket(TCP_IP, TCP_PORT)

if __name__ == "__main__":
    main()
