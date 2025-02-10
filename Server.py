import socket
import datetime
import threading;

# server configuration

# localhost address
HOST = "127.0.0.1"
# port number for communication
PORT = 65432
# maximum number of clients
CLIENT_MAX = 3
# dictionary to store cleint connection details
clients = {}
# number of currently connected clients
current_count = 0;
# number of clients connected through session
total_count = 0;
# lock for thread-safe operations
lock = threading.Lock()

def start_server():
  global total_count, current_count
  # TCP socket creation
  serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # connect server to specified host and port
  serverSocket.bind((HOST, PORT))
  # listen for incoming connections
  serverSocket.listen(CLIENT_MAX)
  
  print(f"[SERVER ACTIVATION] Listening on {HOST} : {PORT}")

  while True:
      # accept new connections only if limit is not reached
      if current_count < CLIENT_MAX:
        # accept a client connection
        connectionSocket, address = serverSocket.accept()
        print(f"[CONNECTED] Connection from {address}")
        with lock:
          # assign a unique client name
          connectionName = f"Client{total_count+1:02d}"
          # increment current client count
          current_count += 1
          # increment total client count
          total_count += 1
        # start a new thread to handle the client
        thread = threading.Thread(target=client_memory, args=(connectionSocket, address, connectionName))
        thread.start()
        
def client_memory(connectionSocket, address, connectionName):
  global clients, current_count
  print(f"[CONNECTION ESTABLISHED] {connectionName} connected from Address: {address}")

  with lock:
    # store connection time
    clients[connectionName] = {"connection_time": datetime.datetime.now(), "disconnect_time": None}
  
  try:
    while True:
      # receive message
      messageData = connectionSocket.recv(1024).decode("utf-8")
      if not messageData:
        # exit loop if message is empty
        break

      print(f"[{connectionName}] {messageData}")

      # handle client disconnection request
      if messageData.lower() == "exit":
        break
      # send status of all clients
      elif messageData.lower() == "status":
        statusMessage = "\n".join([f"{name} - Connected: {info['connection_time']} - Disconnected: {info['disconnect_time']}"
        for name, info in clients.items()])
        # send client status to requester
        connectionSocket.send(statusMessage.encode("utf-8"))
      else:
        # echo message with "ACK"
        connectionSocket.send(f"{messageData} ACK".encode("utf-8"))

  except Exception as e:
    print(f"[ERROR] {connectionName}: {e}")

  with lock:
    # record disconnection time
    clients[connectionName]["disconnect_time"] = datetime.datetime.now()
    # decrement client count
    current_count -= 1
  
  print(f"[DISCONNECTED] {connectionName}")
  # close client socket
  connectionSocket.close()

if __name__ == "__main__":
  start_server()