import tkinter as tk
from tkinter import Tk
from object_detect import *
from board import BoardApp

#source = "http://192.168.40.125:8080/video" ip 카메라 주소
#source = 0 노트북 캠
__source = 0
root = Tk()
root.geometry('1400x900')
root.title('YOLOv5 Object detection')

main_frame = tk.Frame(root, bd=2, relief=tk.SOLID)
main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

title_label = tk.Label(main_frame, text = '실시간 CCTV')
title_label.place(x=470, y=10)

video_frame = tk.Frame(main_frame, bg='white', width=1000, height=800, bd=1, relief=tk.SOLID)
video_frame.place(x=10, y=40)

video_label = tk.Label(video_frame, bg='white', width=960, height=720, bd=1, relief=tk.SOLID)
video_label.place(x=16,y=20)

txt_frame = tk.Frame(main_frame, bg='white', width=400, height=800, bd=1, relief=tk.SOLID)
txt_frame.place(x=1020, y=40)

board = BoardApp(frame=txt_frame, width=40, height=60)

vb = VideoBox(address='경남 진주시 진주대로 501 경상국립대학교 공과대학 407동 3층', frame=video_frame, label=video_label, source=__source, board=board)

vb.main_page()

root.mainloop()