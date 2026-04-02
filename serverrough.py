import socket
import ssl
import threading

HOST = "0.0.0.0"
PORT = 8443

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(5)

print("Secure Server running on port", PORT)

# SSL Context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")


def handle_client(client_socket, addr):

    print("Connection from:", addr)

    secure_socket = context.wrap_socket(client_socket, server_side=True)

    request = secure_socket.recv(1024).decode()

    print("\nEncrypted request received:")
    print(request)

    response = """HTTP/1.1 200 OK
Server: SecurePythonServer/1.0
Content-Type: text/plain

Secure Server Response
"""

    secure_socket.send(response.encode())

    secure_socket.close()


while True:

    client_socket, addr = server_socket.accept()

    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()