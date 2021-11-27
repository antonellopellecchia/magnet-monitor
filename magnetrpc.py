import usbtmc
from xmlrpc.server import SimpleXMLRPCServer

class SensorTHM1176(usbtmc.Instrument):

    directions = ["X", "Y", "Z"]

    def reset(self):
        self.write("*RST")

    @property
    def id(self):
        return self.ask("*IDN?")
    
    def read_field(self, direction):
        field = self.ask(f"MEAS:{direction}?")
        return field.replace(" T", "")

    def read_time(self):
        return self.ask(f"TIM?")

    def read_fields(self):
        return tuple(self.read_field(d) for d in self.directions)

def main():
    server = SimpleXMLRPCServer(("localhost", 8000))
    
    print("Listing connected USB devices:")
    for usb_device in usbtmc.list_devices():
        print(
            usb_device.manufacturer,
            usb_device.product,
            hex(usb_device.idVendor),
            hex(usb_device.idProduct)
        )

    print("Connecting to THM1176-MF...")
    sensor = SensorTHM1176(0x1bfa,0x0498)
    print("Sending reset command...")
    sensor.reset()
    print("Reset command sent.")
    print("Connected to device:", sensor.id)
    print("Test measure:", sensor.read_fields())

    server.register_function(sensor.read_fields, "read_fields")
    
    print("Listening on port 8000...")
    server.serve_forever()

if __name__=='__main__': main()