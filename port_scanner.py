import socket
import threading
from datetime import datetime

# Lock for synchronized printing
print_lock = threading.Lock()

# Log file
LOG_FILE = "scan_results.txt"

def scan_port(host, port, timeout=1):
    """Scan a single TCP port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))

        if result == 0:
            status = "OPEN"
        else:
            status = "CLOSED"

        sock.close()

    except socket.gaierror:
        status = "INVALID HOST"
    except socket.timeout:
        status = "TIMEOUT"
    except Exception as e:
        status = f"ERROR: {e}"

    # Thread-safe print and log
    with print_lock:
        output = f"Port {port}: {status}"
        print(output)
        log_result(output)

def log_result(text):
    """Write results to log file"""
    with open(LOG_FILE, "a") as file:
        file.write(text + "\n")

def main():
    print("=== TCP Port Scanner ===")

    host = input("Enter target host (IP or domain): ").strip()
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))

    try:
        target_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print("Invalid host. Exiting.")
        return

    print(f"\nScanning target: {target_ip}")
    print(f"Port range: {start_port} - {end_port}\n")

    # Write header to log file
    with open(LOG_FILE, "w") as file:
        file.write(f"Port Scan Results\n")
        file.write(f"Target: {target_ip}\n")
        file.write(f"Time: {datetime.now()}\n")
        file.write("-" * 30 + "\n")

    threads = []

    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(target_ip, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\nScan completed.")
    print(f"Results saved in '{LOG_FILE}'")

if __name__ == "__main__":
    main()
