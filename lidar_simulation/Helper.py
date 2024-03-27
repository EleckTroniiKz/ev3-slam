from fractions import Fraction
import math
import numpy as np

class Helper:
    def __init__(self):
        pass

    # get the distance between two points
    def euclidean_distance(self, point1, point2):
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    # get the distance between a line and a point (orthogonally)
    def distance_from_point_to_line(self, line_parameters, points):
        a, b, c = line_parameters # ax + by + c = 0
        distance = abs(a * points[0] + b * points[1] + c) / math.sqrt(a**2 + b**2)
        return distance
    
    # turn general line to slope intercept form
    def general_line_to_slope_intercept(self, a, b, c):
        m = -a / b
        b = -c / b
        return m, b
    
    # turn slope intercept line to general form
    def slope_intercept_to_general_line(self, m, b):
        a, b, c = -m, 1, -b
        if a < 0:
            a, b, c = -a, -b, -c
        den_a = Fraction(a).limit_denominator(1000).as_integer_ratio()[1]
        den_c = Fraction(c).limit_denominator(1000).as_integer_ratio()[1]

        gcd = np.gcd(den_a, den_c)
        lcm = den_a * den_c // gcd

        a = a * lcm
        b = b * lcm
        c = c * lcm
        return a, b, c

    # get the intersection point of two lines
    def get_line_intersection_general(self, parameters1, parameters2):
        a1, b1, c1 = parameters1
        a2, b2, c2 = parameters2

        if b1 == 0 and b2 == 0 or -a1 / b1 == -a2 / b2: # Lines don't intersect
            return None, None

        x = (c1 * b2 - b1 * c2) / (b1 * a2 - a1 * b2)
        y = (a1 * c2 - a2 * c1) / (b1 * a2 - a1 * b2)
        return x, y
    
    def get_slope_intercept_line_from_two_points(self, point1, point2):
        m ,b = 0, 0
        if point1[0] - point2[0] != 0:# line is vertical if this is false
            m = (point2[1] - point1[1]) / (point2[0] - point1[0])
            b = point2[1] - m * point2[0]            
        return m, b

    def project_point_onto_line(self, point, m, b):
        x, y = point
        m2 = -1 / m
        c2 = y - m2 * x
        intersect_x = - (b - c2) / (m - m2)
        intersect_y = m2 * intersect_x + c2
        return intersect_x, intersect_y
    
    def get_point_with_position_distance_angle(self, position, distance, angle):
        x = distance * math.cos(angle) + position[0]
        y = -distance * math.sin(angle) + position[1]
        return int(x), int(y)
    