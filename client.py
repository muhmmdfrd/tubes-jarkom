from socket import *
import sys

clientsocket = socket(AF_INET, SOCK_STREAM)

if len(sys.argv) != 4:
  print("client.py server_host server_port filename")
  sys.exit(0)

host = str(sys.argv[1])
port = int(sys.argv[2])
request = str(sys.argv[3])
request = "GET /" + request + " HTTP/1.1"
try:
   clientsocket.connect((host,port))
except Exception:
  print ("Please try again.\r\n")
  sys.exit(0)


if __name__ == "__main__":
  clientsocket.send(request.encode())
  response = clientsocket.recv(1024)
  print(response.decode())
  clientsocket.close()




 