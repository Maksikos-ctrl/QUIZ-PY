import socket
import threading
import pygame
from pygame.locals import *
import json
from fonts import *
from colors import *


class Client:
    

    def __init__(self, host, port, nickname, password="default_password"):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.ADDR = (self.host, self.port)
        self.MAX_BUFFER = 1024
        self.ENC = "utf-8"
        self.nickname = nickname
        self.password = password

    def receive(self):
        while True:
            try:
                message = self.client.recv(self.MAX_BUFFER).decode(self.ENC)
                if message == "NICK":
                    self.client.send(self.nickname.encode(self.ENC))
                else:
                    print(message)
            except:
                print("An error occured!")
                self.client.close()
                break

    def write(self):
        while True:
            try:
                message = f"{self.nickname}: {input()}"
                self.client.send(message.encode(self.ENC))
            except EOFError:
                break

    def run(self):
        self.client.connect(self.ADDR)
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        write_thread = threading.Thread(target=self.write)
        write_thread.start()

    def send_message(self, message):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
        self.client.send(message.encode(self.ENC))


    def disconnect(self):
        self.client.close()
        print(f"Client {self.nickname} disconnected!")


def get_nickname():
    return input("Enter your nickname: ")

if __name__ == "__main__":
    client = Client("localhost", 5555, get_nickname())
    client.run()
    client.disconnect()        









