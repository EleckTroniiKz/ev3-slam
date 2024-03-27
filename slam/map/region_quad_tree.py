import quads
from .enumerations import QuadPosition
from .region_quad_node import RegionQuadNode


class RegionQuadTree(quads.QuadTree):

    node_class = RegionQuadNode

    def __init__(self, center, width, height, capacity=None, min_size=None):
        """
                Constructs a `QuadTree` object.

                Args:
                    center (tuple|Point): The center point of the quadtree.
                    width (int|float): The width of the point space.
                    height (int|float): The height of the point space.
                    capacity (int): Optional. The number of points per quad before
                        subdivision occurs. Default is `None`.
                """
        self.width = width
        self.height = height
        self.center = self.convert_to_point(center)
        self._root = self.node_class(
            self.center, self.width, self.height, capacity=capacity, min_size=min_size
        )

        self.bb = self._root.bounding_box

    def expand(self, position: QuadPosition) -> None:
        center_offset_x = self.width / 2 if position == QuadPosition.UPPER_LEFT or position == QuadPosition.LOWER_LEFT else -self.width / 2
        center_offset_y = self.height / 2 if position == QuadPosition.LOWER_LEFT or position == QuadPosition.LOWER_RIGHT else -self.height / 2

        new_center = self.convert_to_point((self.center.x + center_offset_x, self.center.y + center_offset_y))

        new_root = self.node_class(
            new_center, self.width * 2, self.height * 2, capacity=self._root.capacity
        )

        new_root.subdivide()

        if position == QuadPosition.UPPER_LEFT:
            new_root.ul = self._root
        elif position == QuadPosition.UPPER_RIGHT:
            new_root.ur = self._root
        elif position == QuadPosition.LOWER_LEFT:
            new_root.ll = self._root
        elif position == QuadPosition.LOWER_RIGHT:
            new_root.lr = self._root

        self.width *= 2
        self.height *= 2
        self.center = new_center
        self._root = new_root
        self.bb = self._root.bounding_box

    def contains_point(self, point) -> bool:
        point = self.convert_to_point(point)

        return self._root.contains_point(point)
