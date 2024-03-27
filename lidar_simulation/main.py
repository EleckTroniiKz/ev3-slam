import math
import pygame
import numpy as np

"""
    In this code I implemented, that you can reference a floorplan and the lidar will sense the obstacles. For that move the mouse over the floorplan and the lidar will sense the obstacles.
    The lidar shoots will shoot rays around the mouse and it will do it everytime the mouse cursor moves. Maybe it might be helpful.
"""


def add_uncertainty(distance, angle, sigma):
    mean = np.array([distance, angle])
    covariance = np.diag(sigma ** 2)

    distance, angle = np.random.multivariate_normal(mean, covariance)
    distance = max(distance, 0)
    angle = max(angle, 0)
    
    return [distance, angle]

class Lidar:
    def __init__(self, range, map, uncertainty):
        self.range = range
        self.speed = 4
        self.sigma = np.array([uncertainty[0], uncertainty[1]])
        self.position = (0, 0)
        self.map = map
        self.width, self.height = pygame.display.get_surface().get_size()
        self.sensedObstacles = []
    
    def getDistance(self, obstacePosition):
        px = (obstacePosition[0] - self.position[0]) ** 2
        py = (obstacePosition[1] - self.position[1]) ** 2
        return math.sqrt(px + py)
    
    def sense_obstacles(self):
        data = []
        x1, y1 = self.position[0], self.position[1]

        for angle in np.linspace(0, 2**math.pi, 60, False):
            x2, y2 = (x1 + self.range * math.cos(angle), y1 - self.range * math.sin(angle))
            for i in range(0, 100):
                u = i / 100
                x = int(x2 * u + x1 * (1 - u))
                y = int(y2 * u + y1 * (1 - u))
                if 0 < x < self.width and 0 < y < self.height:
                    color = self.map.get_at((x, y))
                    if (color[0], color[1], color[2]) == (0, 0, 0):
                        distance = self.getDistance((x, y))
                        output = add_uncertainty(distance, angle, self.sigma)
                        output.append(self.position)

                        # Store the measurement
                        data.append(output)
                        break
        if len(data) > 0:
            return data
        else:
            return False

class EnvironmentBuilder:
    def __init__(self, dimensions):
        pygame.init()
        self.pointCloud = []
        """
        Achtet drauf das der floorplan auf WEIßEM HINTERGRUND IST und die Hindernisse SCHWARZ sind
        und es muss PNG sein
        """
        self.externalMap = pygame.image.load('./LidarSimulation/images/field_five.png')
        self.mapHeight, self.mapWidth = dimensions
        self.map = pygame.display.set_mode((self.mapWidth, self.mapHeight))
        self.map.blit(self.externalMap, (0, 0))

        # Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 128)
        self.grey = (128, 128, 128)
    
    def AD2pos(self, distance, angle, robotPosition):
        x = distance * math.cos(angle) + robotPosition[0]
        y = -distance * math.sin(angle) + robotPosition[1]
        return (int(x), int(y))
    
    def dataStorage(self, data):
        print(len(self.pointCloud))
        for element in data:
            point = self.AD2pos(element[0], element[1], element[2])
            if point not in self.pointCloud:
                self.pointCloud.append(point)
    
    def show_sensorData(self):
        self.infomap = self.map.copy()
        for point in self.pointCloud:
            self.infomap.set_at((int(point[0]), int(point[1])), (255, 0, 0))

environment = EnvironmentBuilder((1256, 1270))
environment.originalMap = environment.map.copy()
laser = Lidar(200, environment.originalMap, uncertainty=(0.5, 0.01))
environment.map.fill(environment.black)
environment.infomap = environment.map.copy()

running = True
while running:
    sensorOn = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_focused():
            sensorOn = True
        elif not pygame.mouse.get_focused():
            sensorOn = False
        
    if sensorOn:
        position = pygame.mouse.get_pos()
        laser.position = position
        sensor_data = laser.sense_obstacles()
        if not sensor_data:
            continue
        environment.dataStorage(sensor_data)
        environment.show_sensorData()
    environment.map.blit(environment.infomap, (0, 0))
    pygame.display.update()
