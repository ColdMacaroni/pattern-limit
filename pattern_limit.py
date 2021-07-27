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

    @staticmethod
    def is_positive(xy):
        """
        Checks if the point is in the positive side of the xy axes (axii)
        """
        return xy[0] >= 0 and xy[1] >= 0

    @staticmethod
    def reverse_point(xy):
        """
        Reverse the x and y coordinates of the point given
        :param xy: (x, y)
        :return: (y, x)
        """
        return xy[1], xy[0]

    @staticmethod
    def mirror_shape(shape):
        """
        Mirror shape yay!
        :param shape: A list of (x, y)
        :return: The points are mirrored along the x axis!
        """
        width = max([pt[0] for pt in shape])

        # This should mirror the points along the x axis, moving em to 0,0
        new_shape = [(width - x, y) for x, y in shape]
        new_shape.reverse()

        return new_shape

    @staticmethod
    def remove_repeated_shapes(shapes, rotate=True, mirror=True):
        """
        Remove all repeated shapes in the list
        NO SUPPORT FOR SHAPES INCLUDING NEGATIVE COORDS
        :param shapes: A list of lists of (x, y)
        :param rotate: Also remove rotated rotated
        :param mirror: Also remove mirrored shapes
        :return: List of lists of (x, y)
        """
        # To store
        new_shapes = list()

        for shape in shapes:
            # To store modified shapes that can then be compared
            tmp_shape_ls = [shape]

            if rotate:
                # Rotate along the y=x line
                tmp_shape_ls.append([PointUtils.reverse_point(pt) for pt in shape])

            if mirror:
                tmp_shape_ls.append(PointUtils.mirror_shape(shape))

            if mirror and rotate:
                tmp_shape_ls.append([PointUtils.reverse_point(pt) for pt in PointUtils.mirror_shape(shape)])

            # Check that the shape hasn't been added to either
            # Must use count so that it ignores itself
            repeated = list()
            for tmp_shape in tmp_shape_ls:
                repeated.append(shapes.count(tmp_shape) > 1 or tmp_shape in new_shapes)

            if not any(repeated):
                new_shapes.append(shape)

        return new_shapes


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
        new_shapes = list()
        for shape in current_shapes:
            last_pt = shape[-1]

            # These functions are used to calculate the next point.
            next_pt_functions = (PointUtils.left,
                                 PointUtils.right,
                                 PointUtils.up,
                                 PointUtils.down)

            # I'd use list comprehension but i want to avoid three function calls
            new_pts = list()
            for f in next_pt_functions:
                new_pt = f(last_pt)

                # Check that the point doesnt already exist and that it is positive
                # I think that only allowing positive ones will reduce the likelihood of rotated repeats
                if new_pt not in shape and PointUtils.is_positive(new_pt):
                    new_pts.append(new_pt)

            # Extend the list of shapes with the new ones!
            new_shapes += [[*shape, next_pt] for next_pt in new_pts]

        # Remove duplicates

        # In place list update from https://stackoverflow.com/a/51336327
        # Update the current shapes

        current_shapes[:] = PointUtils.remove_repeated_shapes(new_shapes)

        # We have placed one more point
        return generate_pattern(points_left - 1, current_shapes)


def pass_function():
    """
    Passes. Approved by kan
    """
    pass  #it passes- kan


def main(size=None, print_out=True):
    """
    Generate a shape of the given number of points and returns how many unique combinations it has
    :param size: the number of points
    :param print_out: Bool. Whether to print the number or not
    :return: The list of shapes
    """
    # Ask user for input in integers above zero. Natural numbers?
    if size is None:
        valid_input = False
        while not valid_input:
            try:
                size = int(input("How many points should this shape have? ").strip())
                if size < 0:
                    print("Number must be positive\n")
                else:
                    valid_input = True

            except ValueError:
                print("Please enter an int\n")

    patterns = generate_pattern(size)

    if print_out:
        print("There are", len(patterns), "unique patterns")

    return patterns


if __name__ == "__main__":
    main()
