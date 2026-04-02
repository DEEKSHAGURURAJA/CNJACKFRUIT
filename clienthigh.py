import socket
import ssl
import threading
import time

results = []
lock = threading.Lock()


def identify_service(banner):
    banner = banner.lower()

    if "apache" in banner:
        return "Apache"
    elif "nginx" in banner:
        return "Nginx"
    elif "iis" in banner:
        return "Microsoft IIS"
    elif "securepythonserver" in banner:
        return "Custom Server"
    else:
        return "Unknown"


def guess_os(response_time):
    if response_time < 50:
        return "Linux/Unix"
    elif response_time < 150:
        return "Windows"
    else:
        return "Unknown"


def scan_port(host, port):
    start = time.time()

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)

        if port == 443 or port == 8443:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            sock = context.wrap_socket(sock, server_hostname=host)

        sock.connect((host, port))

        request = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        sock.send(request.encode())

        banner = sock.recv(4096).decode(errors="ignore")

        response_time = round((time.time() - start) * 1000, 2)

        service = identify_service(banner)
        os_guess = guess_os(response_time)

        print(f"{host}:{port} | {service} | {response_time} ms | {os_guess}")

        with lock:
            results.append((host, port, service, response_time, os_guess))

        sock.close()

    except:
        print(f"{host}:{port} | Failed")
        with lock:
            results.append((host, port, "Failed", 0, "Unknown"))


def scan_host(host, ports):
    threads = []

    for port in ports:
        t = threading.Thread(target=scan_port, args=(host, port))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


def save_results():
    with open("results.txt", "w") as f:
        for r in results:
            f.write(f"{r[0]}:{r[1]} -> {r[2]} ({r[3]} ms, {r[4]})\n")


def show_summary():
    total = len(results)
    detected = sum(1 for r in results if r[2] not in ["Unknown", "Failed"])
    failed = sum(1 for r in results if r[2] == "Failed")

    accuracy = (detected / total) * 100 if total else 0

    print("\n=== SUMMARY ===")
    print("Total:", total)
    print("Detected:", detected)
    print("Failed:", failed)
    print(f"Accuracy: {accuracy:.2f}%")


def main():
    print("=== WEB FINGERPRINTING TOOL ===")

    n = int(input("Enter number of hosts: "))
    hosts = [input(f"Host {i+1}: ") for i in range(n)]

    start_port = int(input("Start port: "))
    end_port = int(input("End port: "))

    ports = list(range(start_port, end_port + 1))

    start_time = time.time()

    for host in hosts:
        print(f"\nScanning {host}...")
        scan_host(host, ports)

    total_time = round(time.time() - start_time, 2)

    save_results()
    show_summary()

    print(f"\nCompleted in {total_time} sec")
    print("Saved to results.txt")


if __name__ == "__main__":
    main()