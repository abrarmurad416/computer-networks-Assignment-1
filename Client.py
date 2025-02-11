import socket

HOST = "127.0.0.1"
PORT = 65432

# Derek Hunziker & Abrar Murad
def start_client():
  try:
    # TCP socket
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to the server
    clientSocket.connect((HOST, PORT))
    
    print("Connection establish. Type 'exit' for disconnection")

    while True:
      # get user input
      message = input("> ")
      # send message to server
      clientSocket.send(message.encode("utf-8"))
      # exit condition
      if message.lower() == "exit":
        break
      
      # receive response from server
      received = clientSocket.recv(1024).decode("utf-8")
      print(f"Server: {received}")

  except Exception as e:
    # print error messages
    print(f"[ERROR] {e}")

  finally:
    # close client socket
    clientSocket.close()

if __name__ == "__main__":
  start_client()