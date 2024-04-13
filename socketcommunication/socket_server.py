import _thread
import socket


end = 0
print("안녕하세요")




def threaded(client_socket, addr):
    print('Connected by: ', addr[0], ':', addr[1])


    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print('Disconnected by ' + addr[0], ':', addr[1])
                break


            print('Received from ' + addr[0], ':', addr[1], data.decode())


            client_socket.send(data)
        except ConnectionResetError as e:
            print("Disconnected by", addr[0], ':', addr[1])
            print(f"e: {e}")




def main():
    ip = ''
    port = 8888


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((ip, port))
    server_socket.listen()


    print('안녕하세요\nServer start')


    while True:
        client_socket, addr = server_socket.accept()
        print('Connected by:', addr[0], ':', addr[1])


        while True:
            data = client_socket.recv(1024)
            if not data:
                break


            print('Received from', addr[0], ':', addr[1], data.decode())
            client_socket.sendall(data)


        client_socket.close()


if __name__ == "__main__":
    main()
