import socket
import threading
import os

def get_header(code, content):
    length = str(len(content))
    if code == 200:
        h = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: " + length + "\r\n\r\n"
    else:
        h = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: " + length + "\r\n\r\n"
    return h.encode('utf-8') + content
    

def read_file(path):
    file = open(path, 'rb')
    content = file.read()
    return content


def handle_client(client_socket, client_address):
    print("Ready to serve...")
    while True:
        try:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break

            print(f"Received request from {client_address}: {request}")
            
            requested_file = request.split()[1][1:]
            if (requested_file == None or requested_file == ''):
                requested_file = 'index.html'
            
            if os.path.exists(requested_file):
                content = read_file(requested_file)
                response = get_header(200, content)
            else:
                if os.path.exists('404.html'):
                    content = read_file('404.html')
                    response = get_header(404, content)
                else:
                    raise Exception('404.html not found')
            
            client_socket.sendall(response)
        except Exception as e:
            print(f"Error: {e}")
            exit()
    client_socket.close()
    print(f"Connection closed with {client_address}")


def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}...")
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


if __name__ == "__main__":
    ports = [8080, 9090, 6060, 80]
    for port in ports:
        threading.Thread(target=start_server, args=(port,)).start()
