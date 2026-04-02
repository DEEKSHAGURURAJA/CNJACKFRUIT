import socket
import ssl


def fingerprint(host, port):

    try:
        print("\nStarting fingerprint scan...")
        print("Target:", host)
        print("Port:", port)

       
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)


        if port == 443:
            context = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=host)

        
        print("\nConnecting to server...")
        sock.connect((host, port))
        print("Connection successful!")

        
        request = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        sock.send(request.encode())

       
        response = sock.recv(4096).decode(errors="ignore")

        print("\n----- Server Response -----\n")
        print(response)

       
        server_found = False

        for line in response.split("\n"):
            if "Server:" in line:
                server_name = line.split(":",1)[1].strip()
                print("\nDetected Server:", server_name)
                server_found = True

        if not server_found:
            print("\nServer header not found.")

        sock.close()

    except Exception as e:
        print("\nError occurred:", e)



host = input("Enter website/domain: ")
port = int(input("Enter port (80 for HTTP, 443 for HTTPS): "))

fingerprint(host, port)