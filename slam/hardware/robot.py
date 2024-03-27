from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveTank, SpeedPercent
import time

class Robot:

    def __init__(self, max_minutes=5):
        self.tank = MoveTank(OUTPUT_A, OUTPUT_B)

        self.timestamp = None
        self.minutes = max_minutes
    
    def move_forward(self):    
        self.tank.on_for_seconds(SpeedPercent(15), SpeedPercent(15), 1)

    def rotate_robot(self, angle):
        self.timestamp = time.perf_counter() if self.timestamp is None else self.timestamp
        
        if angle > 0:
            self.tank.on_for_degrees(50, -50, angle)
        else:
            self.tank.on_for_degrees(-50, 50, abs(angle))

    def time_limit_exceeded(self):
        return (time.perf_counter() - self.timestamp) >= 60 * self.minutes
