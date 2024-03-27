import numpy as np
import random
import math
from vo.pose import Pose
from vo.particle import Particle
from map.map import Map

class ParticleFilter:
    def __init__(self, num_particles: int):
        self.num_particles = num_particles
        self.particles = None

    def initialize_particles_and_weights(self):
        """
        Initialize the particles and weights when the first sensor reading is received.
        """
        if self.particles is None:
            self.particles = [Particle(random.uniform(0, 10), random.uniform(0, 10), random.uniform(0, 2*math.pi), 1/self.num_particles) for _ in range(self.num_particles)]
    
    def particle_filter_process(self, sensor_data, dt: float, map: Map, angle):
        """
        Perform the particle filter algorithm to estimate the pose of the robot based on the sensor data, time difference, map information, and control inputs.
        """
        
        self.initialize_particles_and_weights() # initialize particles and weights, if not done before

        # update every particle, based on sensor data -> applies motion update and measurement update
        self.particles = [self.update_particle(particle, dt, angle, sensor_data, map) for particle in self.particles] 

        # normalize weights
        weights = [particle.weight for particle in self.particles]
        sum_weights = sum(weights)
        self.particles = [Particle(particle.pose.x, particle.pose.y, particle.pose.angle, particle.weight / sum_weights) for particle in self.particles]

        # resample particles based on weights -> survival of the fittest
        indices = self.resample_particles()
        self.particles = [Particle(self.particles[i].pose.x, self.particles[i].pose.y, self.particles[i].pose.angle, 1/self.num_particles) for i in indices]

        # approximate pose with particle average considering weights
        particles = [particle.pose.get_as_list() for particle in self.particles]
        weights = [particle.weight for particle in self.particles]
        approximation = np.average(particles, weights=weights, axis=0)

        return Pose(approximation[0], approximation[1], approximation[2])

    def update_particle(self, particle, time_duration: float, angle, sensor_data, map: Map, noise: float = 0.1):
        particle_x, particle_y, particle_angle = particle.pose.x, particle.pose.y, particle.pose.angle

        angle += np.random.normal(0, noise)
        time_duration += np.random.normal(0, noise)

        radian = np.radians(angle)
        
        dx, dy = time_duration * np.cos(particle_angle + radian), time_duration * np.sin(particle_angle + radian)
        
        particle_x += dx
        particle_y += dy 

        particle.pose = Pose(particle_x, particle_y, particle_angle + radian)

        object_positions = self.calculate_detected_object_positions(sensor_data, particle.pose)

        # Calculate the weights of the particles based on map_obj information
        particle_weight_sum = 0
        weights = [particle.weight for particle in self.particles]
        for particle_index, particle in enumerate(self.particles):
            particle_weight = 1.0
            for object_pos in object_positions:
                if object_pos[0] >= 0 and object_pos[0] < map.grid_width and object_pos[1] >= 0 and object_pos[1] < map.grid_width:
                    particle_weight = particle_weight / 10 if map.map[object_pos[0], object_pos[1]] != 1 else particle_weight * 1.0/(1.0 + math.sqrt((object_pos[0]-particle.pose.x)**2 + (object_pos[1]-particle.pose.y)**2))
            particle_weight_sum += particle_weight * weights[particle_index]

        particle.weight = particle_weight_sum

        return particle
    
    def calculate_detected_object_positions(self, sensor_data, pose: Pose):
        """
        Generate the positions of objects detected by the sensor based on the sensor data and the pose of the robot.
        """
        measurements = np.array(sensor_data)

        angle_data = np.arange(0, 360, 10)
        object_positions = []
        for i in range(len(measurements)):
            angle = math.radians(angle_data[i] + pose.angle)
            delta_x, delta_y = int(measurements[i] * math.sin(angle)), int(measurements[i] * math.cos(angle))
            object_x, object_y = int(delta_x + pose.x), int(delta_y + pose.y)
            object_positions.append((object_x, object_y))
        return object_positions
    
    def resample_particles(self):
        weights = [particle.weight for particle in self.particles]
        cumulative_sum = np.cumsum(weights)
        step = 1.0 / self.num_particles
        uniform_distribution = np.random.uniform(0, step, self.num_particles) + np.arange(self.num_particles) * step
        indexes = np.searchsorted(cumulative_sum, uniform_distribution, side='right')
        return indexes
    