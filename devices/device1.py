import socket
import json
import os
import platform
import time
import subprocess
from generic_device import GeniricDevice as GenericDevice


class Device(GenericDevice):

    def __init__(self, device_name, num_hints):
        super().__init__(device_name=device_name, num_hints=num_hints)
        self.server_host = os.getenv("SERVER_HOST", "192.168.16.240")
        self.server_port = int(os.getenv("SERVER_PORT", 65432))
        self.device_id = os.uname().nodename  # hostname inside container

    def get_device_info(self, status="idle", output=None):
        return {
            "device_id": self.device_id,
            "status": status,
            "output": output,
        }

    def connect(self):
        """
        Connect to the server and handle communication (commands, file transfers).
        """
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.server_host, self.server_port))
                    print(f"[CLIENT {self.device_id}] Connected to server")

                    # Send initial device info
                    s.sendall(json.dumps(self.get_device_info()).encode("utf-8"))

                    buffer = b""
                    while True:
                        data = s.recv(4096)
                        if not data:
                            break
                        buffer += data

                        # Process messages separated by newline
                        while b"\n" in buffer:
                            header_raw, buffer = buffer.split(b"\n", 1)
                            header = json.loads(header_raw.decode("utf-8"))

                            if header["type"] == "command":
                                cmd = header["data"]
                                print(f"[CLIENT {self.device_id}] Command: {cmd}")

                                try:
                                    # Run the command and capture output
                                    result = subprocess.check_output(
                                        cmd, shell=True, stderr=subprocess.STDOUT, text=True
                                    )
                                except subprocess.CalledProcessError as e:
                                    # Command failed → capture error output
                                    result = e.output

                                # Send result back to server
                                s.sendall(
                                    json.dumps(
                                        self.get_device_info(status=f"executed {cmd}", output=result)
                                    ).encode("utf-8")
                                )

                            elif header["type"] == "file":
                                filename = header["filename"]
                                filesize = header["size"]
                                print(f"[CLIENT {self.device_id}] Receiving file {filename} ({filesize} bytes)")

                                # Receive file bytes (consider leftover in buffer)
                                filedata = buffer[:filesize]
                                buffer = buffer[filesize:]

                                while len(filedata) < filesize:
                                    chunk = s.recv(4096)
                                    filedata += chunk

                                with open(filename, "wb") as f:
                                    f.write(filedata)

                                print(f"[CLIENT {self.device_id}] File saved: {filename}")
                                s.sendall(
                                    json.dumps(self.get_device_info(status=f"received {filename}")).encode("utf-8")
                                )

            except Exception as e:
                print(f"[CLIENT {self.device_id}] Error: {e}, retrying...")
                time.sleep(5)

    # Keep original methods for device lifecycle
    def start(self):
        self.device_info["status"] = "active"
        print(f"{self.device_info['device_name']} started.")

    def stop(self):
        self.device_info["status"] = "inactive"
        print(f"{self.device_info['device_name']} stopped.")

    def reset(self):
        self.device_info["status"] = "inactive"
        print(f"{self.device_info['device_name']} reset.")

    def finish(self):
        self.device_info["status"] = "finished"
        print(f"{self.device_info['device_name']} finished.")

    # User hints (to be implemented later)
    def hint1(self): pass
    def hint2(self): pass
    def hint3(self): pass
    def hint4(self): pass
    def hint5(self): pass
    def hint6(self): pass
    def hint7(self): pass
    def hint8(self): pass
    def hint9(self): pass
    def hint10(self): pass


if __name__ == "__main__":
    device = Device(device_name="Device1", num_hints=10)
    device.connect()
