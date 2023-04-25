

import socket
import threading

class Client:
    def __init__(self, host, port, nickname):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.ADDR = (self.host, self.port)
        self.MAX_BUFFER = 1024
        self.ENC = "utf-8"
        self.nickname = nickname

    def receive(self):
        while True:
            try:
                message = self.client.recv(self.MAX_BUFFER).decode(self.ENC)
                if message == "NICK":
                    self.client.send(self.nickname.encode(self.ENC))
                else:
                    print(message)
            except:
                print("An error occurred!")
                self.client.close()
                break

    def write(self):
        while True:
            message = f"{self.nickname}: {input('')}"
            self.client.send(message.encode(self.ENC))

    def run(self):
        self.client.connect(self.ADDR)
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        write_thread = threading.Thread(target=self.write)
        write_thread.start()

client = Client("localhost", 55555, input("Choose a nickname: "))
client.run()






