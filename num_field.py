class num_field(object):

    def __init__(self):
        self.__could_be_number__ = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.is_soleved = False

    def __str__(self):
        if self.is_soleved:
            return str(self.__could_be_number__[0])
        else:
            return '*'
