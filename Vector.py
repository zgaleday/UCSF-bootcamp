class Vector(object):
    """Naive implementation of vector operations using the python list interface"""
    def __init__(self, v0):
        """
        Takes as input the two vectors for which we will operate on.
        :param v0: A 3D vector as either a python list of [x_0, y_0, z_0] or tuple of same format
        """
        self.v0 = v0

    def add(self, other):
        """
        Adds two Vector objects.
        :param other: Another Vector object
        :return: A Vector equal to the vector sum of the current vector and other
        """