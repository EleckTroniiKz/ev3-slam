#!/usr/bin/env pybricks-micropython
from LegoEV3Interface import LegoEV3Interface
from pybricks.tools import wait

ev3_interface = LegoEV3Interface()
print("Started")
ev3_interface.start_gyro_sensor()
ev3_interface.move_forward(100)
wait(5000)
ev3_interface.stop_motors()
print(ev3_interface.read_gyro_sensor())
print("turning")
ev3_interface.turn_left()
wait(5000)
ev3_interface.turn_right()
wait(5000)
ev3_interface.move_backward(100)
wait(5020)
# Perform further actions based on sensor readings
ev3_interface.stop_motors()
