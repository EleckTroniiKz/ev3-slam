from map import Map, visualize
from Slam.vo.pose import Pose
import pygame
import numpy as np


class MapTester_QuadTree:
    def test(self, distance, pose, map_size):
        distances = [distance] * 36
        map = Map(map_size)
        map.update_map(distances, pose)

        visualize(map.tree)


class MapTester_NPY:
    
    def map_to_grayscale(self, val, max_val):
        return 255 - int((val / max_val) * 255)

    def generate_distances(self, robot_pose, map_size, distance):
        distances = [distance] * 36
        map = Map(map_size)
        map.update_map(distances, robot_pose)
        return map.map
    
    def display_array(self, arr):
        pygame.init()
        screen = pygame.display.set_mode((arr.shape[0], arr.shape[1]))
    
        max_val = np.max(arr)
    
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
    
            for i in range(arr.shape[0]):
                for j in range(arr.shape[1]):
                    grayscale_val = self.map_to_grayscale(arr[i, j], max_val)
                    pygame.draw.rect(screen, (grayscale_val, grayscale_val, grayscale_val), pygame.Rect(i, j, 1, 1))
    
            pygame.display.flip()
            pygame.time.wait(30)
    
        pygame.quit()


if __name__ == "__main__":
    
    # uncomment the following lines to test the MapTester_QuadTree class
    
    map_tester = MapTester_QuadTree()
    robot_pose = Pose(0, 0, 0)
    map_tester.test(50, robot_pose, 128)
    

    # uncomment the following lines to test the MapTester_NPY class
    """
    map_tester = MapTester_NPY()
    #map_data = np.load('Map.npy')
    map_data = map_tester.generate_distances(Pose(0, 0, 0), 100, 50)
    map_tester.display_array(map_data)
    """