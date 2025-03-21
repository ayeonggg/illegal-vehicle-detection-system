import socket
import cv2
import numpy as np
import base64
import threading
import time
from datetime import datetime


class ServerSocket:
    def __init__(self, ip='', port=8080):
        self.TCP_IP = ip
        self.TCP_PORT = port
        self.socketOpen()
        self.receiveThread = threading.Thread(target=self.receiveImages)
        self.receiveThread.start()


    def socketClose(self):
        self.sock.close()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is close')


    def socketOpen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.TCP_IP, self.TCP_PORT))
        self.sock.listen(1)
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is open')
        self.conn, self.addr = self.sock.accept()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is connected with client')


    def receiveImages(self):
        try:
            while True:
                length = self.recvall(self.conn, 64)
                length1 = length.decode('utf-8')
                stringData = self.recvall(self.conn, int(length1))
                stime = self.recvall(self.conn, 64)


                # Receive image data and timestamp
                print('receive time: ' + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'))
                data = np.frombuffer(base64.b64decode(stringData), np.uint8)
                decimg = cv2.imdecode(data, 1)


                # Save the received image to a file
                filename = "received_image_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
                cv2.imwrite(filename, decimg)


                cv2.imshow("image", decimg)
                cv2.waitKey(1)
        except Exception as e:
            print(e)
            self.socketClose()
            cv2.destroyAllWindows()
            self.socketOpen()
            self.receiveThread = threading.Thread(target=self.receiveImages)
            self.receiveThread.start()


    def recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf


def main():
    server = ServerSocket('', 8080)


if __name__ == "__main__":
    main()
