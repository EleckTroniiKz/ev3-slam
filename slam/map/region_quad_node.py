from collections import Counter
import quads
from .enumerations import Observation


class RegionQuadNode(quads.QuadNode):

    POINT_CAPACITY = 1
    MIN_SIZE = 8

    def __init__(self, center, width, height, capacity=None, min_size=None):
        super().__init__(center, width, height, capacity=capacity)

        if min_size is None:
            min_size = self.MIN_SIZE

        self.min_size = min_size

    def get_data_value(self):
        if self.points is None or len(self.points) == 0:
            return Observation.UNDISCOVERED

        data_values = [point.data for point in self.points]
        most_common_data_value = Counter(data_values).most_common(1)[0][0]

        return most_common_data_value

    def subdivide(self):
        """
                Subdivides an existing node into the node + children.

                Returns:
                    None: Nothing to see here. Please go about your business.
                """
        half_width = self.width / 2
        half_height = self.height / 2
        quarter_width = half_width / 2
        quarter_height = half_height / 2

        ul_center = self.point_class(
            self.center.x - quarter_width, self.center.y + quarter_height
        )
        self.ul = self.__class__(
            ul_center, half_width, half_height, capacity=self.capacity
        )

        ur_center = self.point_class(
            self.center.x + quarter_width, self.center.y + quarter_height
        )
        self.ur = self.__class__(
            ur_center, half_width, half_height, capacity=self.capacity
        )

        ll_center = self.point_class(
            self.center.x - quarter_width, self.center.y - quarter_height
        )
        self.ll = self.__class__(
            ll_center, half_width, half_height, capacity=self.capacity
        )

        lr_center = self.point_class(
            self.center.x + quarter_width, self.center.y - quarter_height
        )
        self.lr = self.__class__(
            lr_center, half_width, half_height, capacity=self.capacity
        )

        # Redistribute the points.
        # calling `.insert()` is fine because of the changed subdivide condition.
        # A minimum size eliminates the risk of infinite recursion.
        for pnt in self.points:
            if self.is_ul(pnt):
                self.ul.insert(pnt)
            elif self.is_ur(pnt):
                self.ur.insert(pnt)
            elif self.is_ll(pnt):
                self.ll.insert(pnt)
            else:
                self.lr.insert(pnt)

        self.points = []

    def insert(self, point):
        """
        Inserts a `Point` into the node.

        If the node exceeds the maximum capacity, it will subdivide itself
        & redistribute its points before adding the new one. This means there
        can be some variance in the performance of this method.

        Args:
            point (Point): The point to insert.

        Returns:
            bool: `True` if insertion succeeded, otherwise `False`.
        """

        if not self.contains_point(point):
            raise ValueError(
                "Point {} is not within this node ({} - {})".format(
                    point, self.center, self.bounding_box
                )
            )

        # check to ensure we're not going over capacity
        if (len(self.points) + 1) > self.capacity and self.width >= self.min_size * 2 and self.height >= self.min_size * 2:
            self.subdivide()

        if self.ul is not None:
            if self.is_ul(point):
                return self.ul.insert(point)
            elif self.is_ur(point):
                return self.ur.insert(point)
            elif self.is_ll(point):
                return self.ll.insert(point)
            elif self.is_lr(point):
                return self.lr.insert(point)

        # There are no child nodes & we're under capacity. Add it to `points`.
        self.points.append(point)
        if len(self.points) > 5:
            self.points = self.points[:5]

        return True
