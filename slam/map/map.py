import numpy as np
import math
import pickle


from .enumerations import Observation, QuadPosition
from .region_quad_tree import RegionQuadTree


class Map:

    def __init__(self, grid_width):
        # self.grid_size = 1
        self.grid_width = grid_width
        self.map = np.zeros((self.grid_width, self.grid_width))
        self.tree = RegionQuadTree((self.grid_width / 2, self.grid_width / 2), self.grid_width, self.grid_width, 1)

    def extend_map_matrix(self, extend_size=5):
        self.map = np.pad(self.map, pad_width=extend_size, mode='constant', constant_values=0)

    def extend_map(self, object_x, object_y):
        if object_x > self.tree.bb.max_x:
            if object_y > self.tree.bb.max_y:
                self.tree.expand(QuadPosition.LOWER_LEFT)
            else:
                self.tree.expand(QuadPosition.UPPER_LEFT)

        elif object_x < self.tree.bb.min_x:
            if object_y > self.tree.bb.max_y:
                self.tree.expand(QuadPosition.LOWER_RIGHT)
            else:
                self.tree.expand(QuadPosition.UPPER_RIGHT)

        if object_y > self.tree.bb.max_y:
            self.tree.expand(QuadPosition.LOWER_LEFT)
        elif object_y < self.tree.bb.min_y:
            self.tree.expand(QuadPosition.UPPER_LEFT)
    
    def update_map(self, distance_data, robot_position):

        datapoints = len(distance_data)
        for i in range(datapoints):
            angle = math.radians(360 * i / datapoints + robot_position.angle)
            delta_x = int(distance_data[i] * math.sin(angle))
            delta_y = int(distance_data[i] * math.cos(angle))

            object_x = int(round(delta_x + robot_position.x))
            object_y = int(round(delta_y + robot_position.y))
            if 0 <= object_x < self.grid_width and 0 <= object_y < self.grid_width:
                self.map[object_x, object_y] = 1

            self.extend_map(object_x, object_y)

            if not (self.tree.bb.min_x <= robot_position.x <= self.tree.bb.max_x) or \
               not (self.tree.bb.min_y <= robot_position.y <= self.tree.bb.max_y):
                self.extend_map(robot_position.x, robot_position.y)

            self.tree.insert((object_x, object_y), data=Observation.OCCUPIED)
            self._add_free_points(object_x, object_y, robot_position)

        print("Done updating map")

    def _add_free_points(self, target_x, target_y, robot_position):
        start_x, start_y = robot_position.x, robot_position.y
        end_x, end_y = target_x, target_y

        distance = 8
        total_distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
        steps = int(total_distance / distance)

        for i in range(steps):
            point_x = int(start_x + i * (end_x - start_x) / steps)
            point_y = int(start_y + i * (end_y - start_y) / steps)
            self.tree.insert((point_x, point_y), data=Observation.FREE)

    def get_map(self):
        return self.map
    
    def save_map(self):
        np.save("map.npy", self.map)

    def save_tree(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.tree, file)

    def load_tree(self,filename):
        with open(filename, "rb") as file:
            self.tree = pickle.load(file)
            self.grid_width = self.tree.width



def visualize(tree: RegionQuadTree, size=10):
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    def draw_all_nodes(node):
        if node.ul is not None:
            draw_lines(node)
        else:
            draw_rects(node)

        if node.ul:
            draw_all_nodes(node.ul)
        if node.ur:
            draw_all_nodes(node.ur)
        if node.ll:
            draw_all_nodes(node.ll)
        if node.lr:
            draw_all_nodes(node.lr)

        # if not node.ul and not node.ur and not node.ll and not node.lr:
        #     draw_rects(node)

    def draw_rects(node):
        bb = node.bounding_box

        rect = patches.Rectangle((bb.min_x, bb.min_y), bb.width, bb.height)

        if node.get_data_value() == Observation.FREE:
            rect.set_facecolor("green")
        elif node.get_data_value() == Observation.OCCUPIED:
            rect.set_facecolor("red")
        elif node.get_data_value() == Observation.UNDISCOVERED:
            rect.set_facecolor("white")

        plt.gca().add_patch(rect)


    def draw_lines(node):
        bb = node.bounding_box

        # The scales for axhline & axvline are 0-1, so we have to convert
        # our values.
        x_offset = -tree._root.bounding_box.min_x
        min_x = (bb.min_x + x_offset) / tree.width
        max_x = (bb.max_x + x_offset) / tree.width

        y_offset = -tree._root.bounding_box.min_y
        min_y = (bb.min_y + y_offset) / tree.height
        max_y = (bb.max_y + y_offset) / tree.height

        plt.axhline(
            node.center.y, min_x, max_x, color="grey", linewidth=0.5
        )
        plt.axvline(
            node.center.x, min_y, max_y, color="grey", linewidth=0.5
        )

    plt.figure(figsize=(size, size))

    # Draw the axis first.
    half_width = tree.width / 2
    half_height = tree.height / 2
    min_x, max_x = tree.center.x - half_width, tree.center.x + half_width
    min_y, max_y = (
        tree.center.y - half_height,
        tree.center.y + half_height,
    )
    plt.axis([min_x, max_x, min_y, max_y])

    draw_all_nodes(tree._root)
    plt.show()
