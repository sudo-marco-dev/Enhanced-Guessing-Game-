import random
import socket

class GuessingGameServer:
    def __init__(self, host="0.0.0.0", port=7777):
        self.host = host
        self.port = port
        self.secret_number = random.randint(1, 100)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            conn, addr = self.server_socket.accept()
            print(f"Connected by {addr}")
            counter = 0 #Initialize guess attempt counter for each game
            with conn:
                while True:
                    data = conn.recv(1024).decode().strip()
                    if not data:
                        break
                    try:
                        
                        guess = int(data)
                        counter +=1 #Increment guess counter on each valid input
                        if guess < self.secret_number:
                            response = "Too low!"                      
                        elif guess > self.secret_number:
                            response = "Too high!"                        
                        else:
                            response = f"Correct! You win!: {counter} guesses" #Include number of attempts in win message
                            if counter <=5 :
                                response += " = very good" #score evaluation for 1 to 5 guesses
                            elif counter <=10:
                                response += " = good" #evaluation for 6 to 10 guesses
                            else:
                                response += " = fair" #evaluation for 11 or more guesses
                            self.secret_number = random.randint(1, 100)  # Reset for next game
                            
                        conn.sendall(response.encode())
                    except ValueError:
                        conn.sendall("Invalid input! Please enter a number.".encode())

    def stop(self):
        self.server_socket.close()

def main():
    server = GuessingGameServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server.stop()

if __name__ == "__main__":
    main()
