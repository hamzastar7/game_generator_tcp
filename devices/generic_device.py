import socket
import json

class GeniricDevice():
    HOST = "tcp_server"  # The server's hostname or IP address
    PORT = 65432
    def __init__(self, device_name, num_hints):
        self.device_info = {
            "device_name": device_name,
            "num_hints": num_hints,
            "status": "inactive"
        }

    def start(self):
        self.device_info["status"] = "active"

    def stop(self):
        self.device_info["status"] = "inactive"

    def reset(self):
        self.device_info["status"] = "active"

    def finish(self):
        self.device_info["status"] = "finished"

    def hint1(self):
        # to be implemented by the user
        pass

    def hint2(self):
        # to be implemented by the user
        pass

    def hint3(self):
        # to be implemented by the user
        pass

    def hint4(self):
        # to be implemented by the user
        pass

    def hint5(self):
        # to be implemented by the user
        pass

    def hint6(self):
        # to be implemented by the user
        pass

    def hint7(self):
        # to be implemented by the user
        pass

    def hint8(self):
        # to be implemented by the user
        pass

    def hint9(self):
        # to be implemented by the user
        pass

    def hint10(self):
        # to be implemented by the user
        pass
    
    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            s.sendall(json.dumps(self.device_info).encode('utf-8'))
            while True:
                command = s.recv(1024).decode('utf-8')
                print(f"Received command: {command}")
                if command == "activate":
                    self.device_info["status"] = "active"
                elif command == "reset":
                    self.reset()
                elif command == "finish":
                    self.finish()
                elif command == "hint1":
                    self.hint1()
                elif command == "hint2":
                    self.hint2()
                elif command == "hint3":
                    self.hint3()
                elif command == "hint4":
                    self.hint4()
                elif command == "hint5":
                    self.hint5()
                elif command == "hint6":
                    self.hint6()
                elif command == "hint7":
                    self.hint7()
                elif command == "hint8":
                    self.hint8()
                elif command == "hint9":
                    self.hint9()
                elif command == "hint10":
                    self.hint10()
                s.sendall(json.dumps(self.device_info).encode('utf-8'))

if __name__ == "__main__":
    device = GeniricDevice("Device2", 2)
    device.connect()