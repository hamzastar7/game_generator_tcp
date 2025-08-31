import socket
import threading
import json
import redis
import time
import os

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 65432      # Port to listen on
connected_devices = {}

# Redis client
r = redis.Redis(host='redis', port=6379, decode_responses=True)


def send_file(client_socket, filename):
    """Send a file to the client over the same socket using JSON header + raw bytes"""
    try:
        filesize = os.path.getsize(filename)
        header = {
            "type": "file",
            "filename": os.path.basename(filename),
            "size": filesize,
        }
        # Send header first, terminated by newline
        client_socket.sendall((json.dumps(header) + "\n").encode("utf-8"))

        with open(filename, "rb") as f:
            while chunk := f.read(4096):
                client_socket.sendall(chunk)

        print(f"[+] Sent {filename} ({filesize} bytes)")
    except Exception as e:
        print(f"[!] Error sending file: {e}")


def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)  # Allow up to 5 pending connections
    print(f"Listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()


def handle_client(client_socket, addr):
    device_id = f"{addr[0]}:{addr[1]}"
    print(f"Accepted connection from {addr}")
    try:
        device_info = json.loads(client_socket.recv(1024).decode('utf-8'))
        update_device_info(device_id, device_info)
    except Exception as e:
        print(f"[!] Error receiving initial device info: {e}")
        return

    while True:
        try:
            if command := get_device_command(device_id):
                print(f"Got command for {device_id}: {command}")

                # Check if command is a SEND_FILE
                if command.startswith("SEND_FILE"):
                    _, filename = command.split(maxsplit=1)
                    send_file(client_socket, filename)
                else:
                    # Wrap generic command in JSON header
                    header = {"type": "command", "data": command}
                    client_socket.sendall((json.dumps(header) + "\n").encode("utf-8"))

                    # Wait for updated device info response
                    device_info = json.loads(client_socket.recv(1024).decode('utf-8'))
                    update_device_info(device_id, device_info)

                time.sleep(1)
        except Exception as e:
            print(f"An error occurred: {e}")
            revove_device(device_id)
            break


def get_device_command(device_id):
    """
    Retrieve the next command for a specific device from Redis.
    """
    return r.lpop(f"{device_id}:commands")


def update_device_info(device_id, device_info):
    """
    Update the device information in the connected_devices dictionary.
    """
    connected_devices[device_id] = device_info
    print(f"Updated device info: {connected_devices}")
    r.set(name="connected_devices", value=str(connected_devices))


def revove_device(device_id):
    """
    Remove the device from the connected_devices dictionary and Redis.
    """
    if device_id in connected_devices:
        del connected_devices[device_id]
        r.set(name="connected_devices", value=str(connected_devices))
        print(f"Removed device {device_id} from connected devices.")
    else:
        print(f"Device {device_id} not found in connected devices.")


if __name__ == "__main__":
    try:
        start_server(HOST, PORT)
    except Exception as e:
        print(f"An error occurred while starting the server: {e}")
        connected_devices = {}
        r.set(name="connected_devices", value=str(connected_devices))
        print("Server stopped.")
