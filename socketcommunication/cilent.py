import socket
import os


HOST = '54.180.26.177'
PORT = 8888 # 서버에서 사용하는 포트 번호로


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((HOST, PORT))


except ConnectionRefusedError:
    print('서버에 연결할 수 없습니다.')
    print('1. 서버의 ip주소와 포트번호가 올바른지 확인하십시오.')
    print('2. 서버 실행 여부를 확인하십시오.')
    os._exit(1)


while True:
    message = input('Enter message (type "quit" to exit): ')
    if message == 'quit':
        break


    client_socket.send(message.encode())


    received_data = client_socket.recv(1024)
    print('Received from server:', received_data.decode())


client_socket.close()


