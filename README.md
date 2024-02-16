# illegal-vehicle-detection-system
## Capstone design
### Drone Video Illegal Parking Detection System

외장그래픽 gput 있는 데스크탑 사용시 Visual Studio Code또는  Pycharm으로 딥러닝 가능.
내장그래픽만 있는 데스크탑의 경우 Colab으로 학습시켜서 best.pt모델 다운로드한 후 VSC에서 yolov5-master폴더 열어, 코드 수정 후 실행

컴퓨터 카메라로 객체탐지 실행 terminal명령어: python detect.py --weight best.pt --conf 0.5 --img 416 --source 0



참고자료: (yolov5 github)https://github.com/ultralytics/yolov5, (유튜브 구현 영상)https://www.youtube.com/watch?v=U-wkRQ8U3GE, https://www.youtube.com/watch?v=AAYswMNyooY
