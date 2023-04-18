import socket

HOST = 'localhost'  # the server's hostname or IP address
PORT = 55555  # the port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        message = input('Enter a message: ')
        s.sendall(message.encode())
        data = s.recv(1024)
        print('Received', repr(data.decode()))