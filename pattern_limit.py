##
# pattern_limit.py

class PointUtils:
    """
    Small little functions for working with points (i.e., xy coordinates)
    """
    @staticmethod
    def right(xy):
        """
        Returns the point 1 unit to the right of given point
        :param xy: (x, y)
        :return: (x + 1, y)
        """
        return xy[0] + 1, xy[1]

    @staticmethod
    def left(xy):
        """
        Returns the point 1 unit to the left of given point
        :param xy: (x, y)
        :return: (x - 1, y)
        """
        return xy[0] - 1, xy[1]

    @staticmethod
    def up(xy):
        """
        Returns the point 1 unit above of given point
        :param xy: (x, y)
        :return: (x, y + 1)
        """
        return xy[0], xy[1] + 1

    @staticmethod
    def down(xy):
        """
        Returns the point 1 unit below given point
        :param xy: (x, y)
        :return: (x, y - 1)
        """
        return xy[0], xy[1] - 1


def generate_pattern(points_left, current_shapes=None):
    """
    Recursively create all possible patterns without repetition
    :param current_shapes: A list of lists of (x, y) tuples
    :param points_left: Number of points left to create
    :return: List of lists of (x, y) tuples
    """
    # This to avoid default arg being mutable
    if current_shapes is None:
        current_shapes = list()

    # Exit if there are no more points to create. Basically stops the recursion
    if points_left == 0:
        return current_shapes

    # Create the first point (0, 0) when the list is empty
    elif not current_shapes:
        current_shapes.append([(0, 0)])
        return generate_pattern(points_left - 1, current_shapes)

    else:
        for shape in current_shapes:
            last_pt = shape[-1]





def pass_function():
    """
    Passes
    """
    pass  #it passes- kan


def main():
    ...


if __name__ == "__main__":
    main()
