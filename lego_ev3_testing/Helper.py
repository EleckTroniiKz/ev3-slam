import json
from pybricks.parameters import Port


def getPortFromDevice(device):
    # Load the configuration file
    with open('PortConfiguration.json') as config_file:
        config = json.load(config_file)

    # Search the device in the motors and sensors
    for section in ['motors', 'sensors']:
        if device in config[section]:
            port_string = config[section][device]
            break
    else:
        raise ValueError("Device not found: {}".format(device))

    # Convert the port string into a port object
    if port_string == "A":
        return Port.A
    elif port_string == "B":
        return Port.B
    elif port_string == "C":
        return Port.C
    elif port_string == "D":
        return Port.D
    elif port_string == "1":
        return Port.S1
    elif port_string == "2":
        return Port.S2
    elif port_string == "3":
        return Port.S3
    elif port_string == "4":
        return Port.S4
    else:
        raise ValueError("Invalid port: {}".format(port_string))