import socket

# function to fingerprint server
def fingerprint(host, port):

    try:
        # create TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # set timeout
        sock.settimeout(5)

        print("Connecting to server...")

        # connect to server
        sock.connect((host, port))

        print("Connected!")

        # send HTTP request
        request = "HEAD / HTTP/1.1\r\nHost: {}\r\n\r\n".format(host)
        sock.send(request.encode())

        # receive response
        response = sock.recv(4096)

        response_text = response.decode()

        print("\nServer Response:\n")
        print(response_text)

        # find server banner
        for line in response_text.split("\n"):
            if "Server:" in line:
                print("\nDetected Server:", line)

        sock.close()

    except Exception as e:
        print("Error:", e)


# user input
host = input("Enter website: ")
port = int(input("Enter port (80 for HTTP): "))

fingerprint(host, port)