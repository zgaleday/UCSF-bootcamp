class Vector(object):
    """Naive implementation of vector operations using the python list interface"""
    def __init__(self, v0):
        """
        Takes as input the two vectors for which we will operate on.
        :param v0: A 3D vector as either a python list of [x_0, y_0, z_0] or tuple of same format
        """
        self.v0 = v0

    def get(self, index):
        """
        Gets the desired x, y, z coordinate
        :param index: 0 == x, 1 == y, 2 == z (int)
        :return: the value of the specified dimension
        """
        if (index > 2 or index < 0):
            raise ValueError("Please input a valid index [0-2]")
        return self.v0[index]

    def add(self, other):
        """
        Adds two Vector objects.
        :param other: Another Vector object
        :return: A Vector equal to the vector sum of the current vector and other
        """
        return Vector([self.v0[i] + other.get(i) for i in range(3)])

    def subtract(self, other):
        """
        Subtract two Vector objects
        :param other: Another vector object to be subtracted
        :return: A Vector equal to the vector subtraction of the current vector and other
        """
        return Vector([self.v0[i] - other.get(i) for i in range(3)])

    def normalize(self):
        """
        Returns the unit vector of the current vector
        :return: A new vector object == the unit vector of the current vector
        """
        magnitude = self.dot_product(self) ** .5
        return Vector([self.v0[i] / magnitude for i in range(3)])

    def dot_product(self, other):
        """
        Returns the dot product of the current vector and the other Vector
        :param other: Another instance of the vector class
        :return:
        """
        return sum([self.v0[i] * other.get(i) for i in range(3)])

    def cross_product(self, other):
        """
        Returns the cross product of the current vector and other
        :param other: A Vector object
        :return: The cross product of the two Vectors as a new Vector object
        """
        x0, y0, z0 = self.v0
        x1, y1, z1 = other.get(0), other.get(1), other.get(2)
        # Calculate the new vector componants for readability
        x2 = y0 * z1 - z0 * y1
        y2 = z0 * x1 - x0 * z1
        z2 = x0 * y1 - y0 * x1
        return Vector([x2, y2, z2])

    def __str__(self):
        return self.v0.__str__()


if __name__ == "__main__":
    v0 = Vector([1, 2, 3])
    v1 = Vector([3, 4, 5])
    print("Adding " + str(v0) + "and " + str(v1) + "yields: " + str(v0.add(v1)))
    print("Subtracting " + str(v0) + "and " + str(v1) + "yields: " + str(v0.subtract(v1)))
    print("Normalizing  " + str(v0) + "yields: " + str(v0.normalize()))
    print("Dotting " + str(v0) + "and " + str(v1) + "yields: " + str(v0.dot_product(v1)))
    print("Crossing " + str(v0) + "and " + str(v1) + "yields: " + str(v0.cross_product(v1)))