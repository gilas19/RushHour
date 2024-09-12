"""Utility classes and functions for the GraphPlan module."""


class Pair(object):
    """
    A utility class to represent pairs (ordering of the objects in the pair does not matter).
    It is used to represent mutexes (for both actions and propositions)
    """

    def __init__(self, a, b):
        """
        Constructor
        """
        self.a = a
        self.b = b

    def __eq__(self, other):
        if (self.a == other.a) & (self.b == other.b):
            return True
        if (self.b == other.a) & (self.a == other.b):
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "(" + str(self.a) + "," + str(self.b) + ")"

    def __hash__(self):
        return hash(self.a) + hash(self.b)
