from .pose import Pose

class Particle:

    def __init__(self, x, y, orientation, weight):
        self.pose = Pose(x, y, orientation)
        self.weight = weight
    
    def get_as_list(self):
        return [self.pose.x, self.pose.y, self.pose.angle, self.weight]