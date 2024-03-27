from ev3dev2.motor import MediumMotor, OUTPUT_C, SpeedPercent
from ev3dev2.sensor.lego import InfraredSensor

class Sensor:
    def __init__(self):
        self.ir = InfraredSensor()
        self.medium_motor = MediumMotor(OUTPUT_C)
        self.angle = 0
    
    def get_distances(self):
        """
        Returns the distances from the last scan
        """
        distances = []

        # Rotate medium_motor to start position
        self.medium_motor.on_to_position(SpeedPercent(10), 0)

        # Rotate the sensor 36 times by 10 degrees
        for _ in range(0, 360, 10):
            self.medium_motor.on_for_degrees(SpeedPercent(10), 10)
            distance = self.ir.proximity
            distances.append(distance)

        # Return medium_motor to start position
        self.medium_motor.on_for_degrees(SpeedPercent(10), -360)

        self.distances = distances

        max_index = distances.index(min(distances)) * 10
        self.angle = max_index

        return distances
    



