import socket
import datetime
import threading;

HOST = "127.0.0.1"
PORT = 65432
CLIENT_MAX = 3
clients = {}
current_count = 0;
total_count = 0;
lock = threading.Lock()

def start_server():
  global total_count, current_count

  serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  serverSocket.bind((HOST, PORT))
  serverSocket.listen(CLIENT_MAX)
  
  print(f"[SERVER ACTIVATION] Listening on {HOST} : {PORT}")

  while True:
      if current_count < CLIENT_MAX:
        connectionSocket, address = serverSocket.accept()
        print(f"[CONNECTED] Connection from {address}")
        with lock:
          connectionName = f"Client{total_count+1:02d}"
          current_count += 1
          total_count += 1
        thread = threading.Thread(target=client_memory, args=(connectionSocket, address, connectionName))
        thread.start()
        
def client_memory(connectionSocket, address, connectionName):
  global clients, current_count
  print(f"[CONNECTION ESTABLISHED] {connectionName} connected from Address: {address}")

  with lock:
    clients[connectionName] = {"connection_time": datetime.datetime.now(), "disconnect_time": None}
  
  try:
    while True:
      messageData = connectionSocket.recv(1024).decode("utf-8")
      if not messageData:
        break

      print(f"[{connectionName}] {messageData}")

      if messageData.lower() == "exit":
        break
      elif messageData.lower() == "status":
        statusMessage = "\n".join([f"{name} - Connected: {info['connection_time']} - Disconnected: {info['disconnect_time']}"
        for name, info in clients.items()])
        connectionSocket.send(statusMessage.encode("utf-8"))
      else:
        connectionSocket.send(f"{messageData} ACK".encode("utf-8"))

  except Exception as e:
    print(f"[ERROR] {connectionName}: {e}")

  with lock:
    clients[connectionName]["disconnect_time"] = datetime.datetime.now()
    current_count -= 1
  
  print(f"[DISCONNECTED] {connectionName}")
  connectionSocket.close()

if __name__ == "__main__":
  start_server()