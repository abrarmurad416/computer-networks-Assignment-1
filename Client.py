import socket

HOST = "127.0.0.1"
PORT = 65432

def start_client():
  try:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((HOST, PORT))
    
    print("Connection establish. Type 'exit' for disconnection")

    while True:
      message = input("> ")
      clientSocket.send(message.encode("utf-8"))
      if message.lower() == "exit":
        break

      received = clientSocket.recv(1024).decode("utf-8")
      print(f"Server: {received}")

  except Exception as e:
    print(f"[ERROR] {e}")

  finally:
    clientSocket.close()

if __name__ == "__main__":
  start_client()