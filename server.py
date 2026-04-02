import socket

HOST = "127.0.0.1"
PORT = 8080

# Create TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind socket to IP and port
server.bind((HOST, PORT))

# Listen for incoming connections
server.listen(5)

print("Server running on", HOST, "port", PORT)

while True:
    # Accept connection from client
    conn, addr = server.accept()
    print("\nConnection received from:", addr)

    # Receive data from client
    request = conn.recv(1024).decode()
    print("\nClient request:\n", request)

    # Fake HTTP response with server banner
    response = """HTTP/1.1 200 OK
Server: CustomPythonServer/1.0
Content-Type: text/plain

Hello from the test server
"""

    # Send response
    conn.send(response.encode())

    # Close connection
    conn.close()