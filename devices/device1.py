from generic_device import GenericDevice

class Device(GenericDevice):

    def __init__(self, device_name, num_hints):
        super().__init__(device_name=device_name, num_hints=num_hints)

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
    
device = Device(device_name="Device1", num_hints=10)
device.connect()