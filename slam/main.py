#!/usr/bin/env python3

import time
from hardware.robot import Robot
from hardware.sensor import Sensor
from particle_filter import ParticleFilter
from map.map import Map
from vo.pose import Pose

class SLAM:
    def __init__(self, particle_number: int = 50, grid_size: int = 300, max_minutes: int = 15):
        self.robot = Robot(max_minutes)
        self.sensor = Sensor()
        self.particle_filter = ParticleFilter(particle_number)
        self.map = Map(grid_size)

        self.timeStamp = None
        self.map.update_map(self.sensor.get_distances(), Pose(grid_size // 2, grid_size // 2 , 0))
    
    def execute_phase_two(self):
        self.robot.rotate_robot(self.sensor.angle)
        sensor_data = self.sensor.get_distances()

        while self.sensor.ir.proximity > 15:

            # Get Sensor Data
            sensor_data = self.sensor.get_distances()

            # Estimate Position
            timeDifference = time.time() - self.timeStamp 
            pose = self.particle_filter.particle_filter_process(sensor_data, timeDifference, self.map, self.sensor.angle)
            self.timeStamp = time.time()

            # Update Map
            self.map.update_map(sensor_data, pose)

            # Move Robot Forward
            self.robot.move_forward()

    def execute_phase_four(self):
        while True: 

            # Get Sensor Data
            sensor_data = self.sensor.get_distances()

            # Estimate Position
            timeDifference = time.time() - self.timeStamp 
            pose = self.particle_filter.particle_filter_process(sensor_data, timeDifference, self.map, self.sensor.angle)
            self.timeStamp = time.time()

            # Update Map
            self.map.update_map(sensor_data, pose)
            self.map.save_map()

            # Move Robot
            if self.sensor.ir.proximity < 15: # turn left
                self.robot.rotate_robot(-45)

            elif sensor_data[9] > 15: # turn right
                self.robot.rotate_robot(45)
                self.robot.move_forward()

            else: # move forward
                self.robot.move_forward()

            # Check Time Limit
            if self.robot.time_limit_exceeded(): # check time limit
                print('SLAM completed!')
                break

    def mainloop(self):

        """ Phase 1: Get Sensor Data"""
        sensor_data = self.sensor.get_distances()

        if self.timeStamp is None:
            self.timeStamp = time.time()

        """ Phase 2: Move to closest wall"""
        self.execute_phase_two()


        """ Phase 3: Rotate Robot left"""
        self.robot.rotate_robot(-90)


        """Phase 4: Move Robot around the room"""
        self.execute_phase_four()
            

        """Phase 5: Save Map and Tree"""
        self.map.save_map()
        self.map.save_tree("tree.pickle")

if __name__ == '__main__':
    slam = SLAM()
    slam.mainloop()