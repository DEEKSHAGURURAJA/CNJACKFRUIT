import socket
import ssl


def fingerprint(host, port):

    try:
        print("\nStarting fingerprint scan...")
        print("Target:", host)
        print("Port:", port)

        # Create TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)

        # If HTTPS use SSL
        if port == 443 or port == 8443:
            context = ssl.create_default_context()

            # Disable verification for self-signed certificate (your server)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            sock = context.wrap_socket(sock, server_hostname=host)

        print("\nConnecting to server...")
        sock.connect((host, port))
        print("Connection successful!")

        # HTTP Request
        request = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

        sock.send(request.encode())

        # Receive banner
        response = sock.recv(4096).decode(errors="ignore")

        print("\n----- Server Response -----\n")
        print(response)

        # Identify server
        server_found = False

        for line in response.split("\n"):

            if "Server:" in line:

                server_name = line.split(":", 1)[1].strip()

                print("\nDetected Server:", server_name)

                server_found = True

        if not server_found:
            print("\nServer header not found.")

        sock.close()

    except Exception as e:
        print("\nError occurred:", e)


# Multiple server testing
servers = [
    ("example.com", 80),
    ("nginx.org", 80),
    ("127.0.0.1", 8443)   # your local secure server
]


print("WEB SERVER FINGERPRINTING TOOL")

for host, port in servers:
    fingerprint(host, port)