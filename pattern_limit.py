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
    def surrounding_points(xy):
        """
        Returns the 8 points around the one given
        :param xy: (x, y)
        :return: list of (x, y)
        """
        # /shrug
        x, y = xy
        return [(x - 1, y + 1),
                (x, y + 1),
                (x + 1, y + 1),
                (x - 1, y),
                (x + 1, y),
                (x - 1, y - 1),
                (x, y - 1),
                (x + 1, y - 1)]

    @staticmethod
    def make_shape_positive(shape):
        """
        Move shape to the first quadrant
        """
        all_x, all_y = zip(*shape)



    @staticmethod
    def rotate_shape(shape):
        """
        Rotates a shape in 90°, 180°, and 270°.
        :param shape: A list of (x, y)
        :return: A list of lists of (x, y)
        """
        # zip trick from https://www.geeksforgeeks.org/python-unzip-a-list-of-tuples/
        # Acquire width and height to reposition from negatives
        all_x, all_y = zip(*shape)

        width = max(all_x)
        height = max(all_y)

        rotations = list()

        # On these its important to subtract them from width or height to avoid negatives
        # Degrees counter-clockwise
        # 90 degrees
        # It actually works i figured it out myself. Make y negative and then reverse the points
        rotations.append(list(map(lambda xy: PointUtils.reverse_point((xy[0], height - xy[1])), shape)))

        # 180 degrees
        # https://www.mathwarehouse.com/transformations/rotations-in-math.php
        rotations.append(list(map(lambda xy: (width - xy[0], height - xy[1]), shape)))

        # 270
        rotations.append(list(map(lambda xy: PointUtils.reverse_point((width - xy[0], xy[1])), shape)))

        return rotations

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
        # TODO: FIX. REMOVES SHAPES THAT SHOULD NOT BE REMOVED
        # To store
        new_shapes = list()

        # MUST sort so that differently positioned x,y coordinates do not affect this stuff
        # do NOT sort the actual shape, they must be left intact so the algorithm doesnt break
        sorted_shapes = [sorted(s_shape) for s_shape in shapes]

        for shape in shapes:
            # To store modified shapes that can then be compared
            tmp_shape_ls = [shape]

            if rotate:
                tmp_shape_ls += PointUtils.rotate_shape(shape)

            if mirror:
                tmp_shape_ls += [PointUtils.mirror_shape(s) for s in tmp_shape_ls]

            # Check that the shape hasn't been added to either
            # Must use count so that it ignores itself
            repeated = list()

            shape_exists = lambda to_check: sorted(to_check) in [sorted(s_shape) for s_shape in new_shapes]
            for tmp_shape in tmp_shape_ls:
                repeated.append(shape_exists(tmp_shape))

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

            # I'd use list comprehension but i want to avoid three function calls
            new_pts = list()

            # The possible points MUST have a point connected (i.e. Not diagonal)
            possible_next_pts = PointUtils.surrounding_points(last_pt)
            connected_pt_functions = (PointUtils.left,
                                      PointUtils.right,
                                      PointUtils.up,
                                      PointUtils.down)

            # Check that all of the possible points (The 8 around the last pt) have one of the points in the main shape
            # connected to them.
            for possible_pt in possible_next_pts:
                connections = [connected_pt in shape
                               for connected_pt in [f(possible_pt) for f in connected_pt_functions]]

                if any(connections) and PointUtils.is_positive(possible_pt):
                    new_pts.append(possible_pt)

            # To store the points which follow all rules
            next_pts = list()
            for new_pt in new_pts:
                # Check that the point doesnt already exist and that it is positive
                # I think that only allowing positive ones will reduce the likelihood of rotated repeats
                if new_pt not in shape:
                    next_pts.append(new_pt)

            # Extend the list of shapes with the new ones!
            new_shapes += [[*shape, next_pt] for next_pt in next_pts]

        # In place list update from https://stackoverflow.com/a/51336327
        # Update the current shapes without repeats
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
    print(main())
