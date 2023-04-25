
import socket
import threading

class Server:
    def __init__(self):
        self.HOST = "localhost"
        self.PORT = 55555
        self.MAX_BUFFER = 1024
        self.ENC = "utf8"
        self.ADDR = (self.HOST, self.PORT)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.clients = []
        self.nicknames = []

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while 1:
            try:
                message = client.recv(self.MAX_BUFFER)
                self.broadcast(message)
            except:
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.broadcast(f"{nickname} left the chat!".encode(self.ENC))
                self.nicknames.remove(nickname)
                break

    def receive(self):
        while 1:
            try:
                client, addr = self.server.accept()
                print(f"Connected with {str(addr)}")

                client.send("NICK".encode(self.ENC))
                nickname = client.recv(self.MAX_BUFFER).decode(self.ENC)
                self.nicknames.append(nickname)
                self.clients.append(client)

                print(f"Nickname of the client is {nickname}!")
                self.broadcast(f"{nickname} joined the chat!".encode(self.ENC))
                client.send("Connected to the server!".encode(self.ENC))

                thread = threading.Thread(target=self.handle, args=(client,))
                thread.start()
            except:
                print("An error occured!")
                self.server.close()
                break

    def run(self):
        self.server.listen()
        print("Server is listening...")
        self.receive()

if __name__ == "__main__":
    server = Server()
    server.run()




        

        
