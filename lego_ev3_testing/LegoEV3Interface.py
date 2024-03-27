from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from Helper import getPortFromDevice
from pybricks.tools import wait, StopWatch, DataLog

class LegoEV3Interface:
    def __init__(self):
        # Initialize connection with the EV3 brick and motors/sensors
        self.ev3 = EV3Brick()
        self.sonic = UltrasonicSensor(getPortFromDevice("ultrasonic_sensor")) 
        self.gyro = GyroSensor(getPortFromDevice("gyro_sensor"))
        self.motor_left = Motor(getPortFromDevice("left_motor"))
        self.motor_right = Motor(getPortFromDevice("right_motor"))
        self.motor_top = Motor(getPortFromDevice("arm_motor"))

    def move_forward(self, speed):
        self.motor_left.run(speed)
        self.motor_right.run(speed)

    def move_backward(self, speed):
        self.motor_right.run(-speed,)
        self.motor_left.run(-speed)


    def turn_left(self):
        self.gyro.reset_angle(0)
        while abs(self.gyro.angle()) < 87:
            self.motor_left.run(-100)
            self.motor_right.run(100)
            print(self.gyro.angle())

        while abs(self.gyro.angle()) < 88:
            self.motor_left.run(-1)
            self.motor_right.run(1)
            print(self.gyro.angle())

        print(self.gyro.angle())
        self.gyro.reset_angle(0)
        self.motor_left.stop()
        self.motor_right.stop()

    def turn_right(self):
        self.gyro.reset_angle(0)
        while abs(self.gyro.angle()) < 87:
            self.motor_left.run(100)
            self.motor_right.run(-100)
            print(self.gyro.angle())

        while abs(self.gyro.angle()) < 88:
            self.motor_left.run(1)
            self.motor_right.run(-1)
            print(self.gyro.angle())

        print(self.gyro.angle())
        self.gyro.reset_angle(0)
        self.motor_left.stop()
        self.motor_right.stop()

    def stop_motors(self):
        self.motor_left.stop()
        self.motor_right.stop()

    def read_ultrasonic_sensor(self):
        return self.sonic

    def read_gyro_sensor(self):
        return self.gyro.angle()

    def start_gyro_sensor(self):
        self.gyro.reset_angle(0)



# Example usage:
if __name__ == "__main__":
    ev3_interface = LegoEV3Interface()
    print("Started")
    ev3_interface.move_forward(50)
    wait(500)
    ev3_interface.stop_motors()
    ev3_interface.turn_left()
    ev3_interface.move_forward(50)
    # Perform further actions based on sensor readings
    ev3_interface.stop_motors()