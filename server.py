import socket
import threading

class Server:
    def __init__(self):
        self.HOST = "localhost"
        self.PORT = 5555
        self.MAX_BUFFER = 1024
        self.ENC = "utf8"
        self.ADDR = (self.HOST, self.PORT)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.clients = []
        self.nicknames = []
        self.ready_clients = []
        self.start_game_lock = threading.Lock() # Lock to synchronize game start

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        try:
            while True:
                message = client.recv(self.MAX_BUFFER)
                if message:
                    self.broadcast(message.decode(self.ENC))
                else:
                    self.remove_client(client)
                    if client in self.clients:  # Check if the client is still in the list
                        self.winner(client)  # Call winner() when a client is disconnected
                    break
        except ConnectionResetError:
            self.remove_client(client)
            if client in self.clients:  # Check if the client is still in the list
                self.winner(client)  # Call winner() when a client is disconnected
        except ValueError:
           # Handle the case when a client that has already been removed is disconnected
            pass




    def remove_client(self, client):
        index = self.clients.index(client)
        nickname = self.nicknames[index]
        self.clients.remove(client)
        client.close()
        self.nicknames.remove(nickname)
        self.broadcast(f"{nickname} left the chat!".encode(self.ENC))
        if client in self.ready_clients:
            self.ready_clients.remove(client)        


    def send_message(self, client, message):
        client.send(message.encode(self.ENC))


    def send_question(self, client, question):
        self.send_message(client, f"Question: {question}")            

    def receive(self):
        while True:
            try:
                client, addr = self.server.accept()
                print(f"Connected with {str(addr)}")

                client.send("NICK".encode(self.ENC))
                nickname = client.recv(self.MAX_BUFFER).decode(self.ENC)
                self.nicknames.append(nickname)
                self.clients.append(client)

                print(f"Nickname of the client is {nickname}!")
                self.broadcast(f"{nickname} joined the chat!".encode(self.ENC))
             

                thread = threading.Thread(target=self.handle, args=(client,))
                thread.start()

                # Check if enough clients are ready to start the game
                with self.start_game_lock:
                    self.ready_clients.append(client)
                    if len(self.ready_clients) == 2:
                        self.start_game()
                        print("Game started!")
                    # if third client wants to join, send a message that the game is full, and close the connection
                    elif len(self.ready_clients) == 3:
                        self.send_message(client, "The game is full. Please try again later.")
                        self.remove_client(client)
                        print("Game is full!")


            except:
                print("Server error occurred!")
                self.server.close()
                break

    def start_game(self):
        # Send a "start" message to all ready clients
        self.broadcast("START".encode(self.ENC))


        # Reset the ready clients list
        self.ready_clients = []  


    def winner(self, client):
        # Send a "winner" message to all clients
        self.broadcast(f"{self.nicknames[self.clients.index(client)]} won!".encode(self.ENC))
        # Reset the ready clients list
        self.ready_clients = []      


    def winner(self, client):
        winner_index = self.clients.index(client)
        winner_nickname = self.nicknames[winner_index]
        self.broadcast(f"Winner: {winner_nickname}".encode(self.ENC))
        # Reset the ready clients list
        self.ready_clients = []         


    def run(self):
        self.server.listen()
        print("Server is listening...")
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

if __name__ == "__main__":
    server = Server()
    server.run()


        

        
