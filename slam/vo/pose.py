class Pose:
    def __init__(self, x: int, y: int, angle: int):
        self.x = x
        self.y = y
        self.angle = angle
    
    def get_as_list(self):
        return [self.x, self.y, self.angle]

    def __repr__(self):
        return 'Pose(x={}, y={}, angle={})'.format(self.x, self.y, self.angle)

    def __str__(self):
        return '({}, {}, {})'.format(self.x, self.y, self.angle)