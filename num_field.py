class num_field(object):

    def __init__(self):
        self.__could_be_number__ = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.is_solved = False

    def __str__(self):
        if self.is_solved:
            return str(self.__could_be_number__[0])
        else:
            return '*'
