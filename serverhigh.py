import socket
import ssl
import threading
from datetime import datetime

HOST = "0.0.0.0"
PORT = 8443

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))
server_socket.listen(10)

print("=== SECURE SERVER RUNNING ===")

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def generate_response(request):
    req = request.lower()

    if "nginx" in req:
        server = "nginx/1.18.0"
    elif "apache" in req:
        server = "Apache/2.4.41"
    else:
        server = "SecurePythonServer/5.0"

    return f"""HTTP/1.1 200 OK
Server: {server}
Content-Type: text/plain

Hello from Secure Server
"""


def handle_client(client_socket, addr):
    log(f"Connected: {addr}")

    try:
        secure_socket = context.wrap_socket(client_socket, server_side=True)

        request = secure_socket.recv(1024).decode(errors="ignore")
        log(f"Request:\n{request}")

        response = generate_response(request)
        secure_socket.send(response.encode())

        secure_socket.close()
        log(f"Disconnected: {addr}")

    except Exception as e:
        log(f"Error: {e}")


while True:
    client_socket, addr = server_socket.accept()
    threading.Thread(target=handle_client, args=(client_socket, addr)).start()