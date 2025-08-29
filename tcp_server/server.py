import socket
import threading
import json
import redis
import time


HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
connected_devices = {}


r = redis.Redis(host='redis', port=6379, decode_responses=True)


def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5) # Allow up to 5 pending connections
    print(f"Listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()


def handle_client(client_socket, addr):
    device_id = f"{addr[0]}:{addr[1]}"
    print(f"Accepted connection from {addr}")
    device_info = json.loads(client_socket.recv(1024).decode('utf-8'))
    update_device_info(device_id, device_info)

    while True:
        try:
            if command:=get_device_command(device_id):
                print(f"Got command {command}")
                client_socket.sendall(command)
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
