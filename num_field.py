class num_field(object):

    def __init__(self):
        self._could_be_number_ = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.is_solved = False

    def __str__(self):
        if self.is_solved:
            return str(self.__could_be_number__[0])
        else:
            return '*'

    def set_num(self, value):
        self._could_be_number_ = [value]
        self.is_solved = True

    def remove_posibility(self, value):
        self._could_be_number_.remove(value)
        if len(self._could_be_number_) == 1:
            self.is_solved = True
