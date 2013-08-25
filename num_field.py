import logging
class num_field(object):

    def __init__(self):
        self._could_be_number = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self._is_solved = False
        self._value = 0

    def __str__(self):
        if self._is_solved:
            return str(self._value)
        return '*'

    def set_num(self, value):
        self._could_be_number = set()
        self._is_solved = True
        self._value = value

    def remove_posibility(self, value):
        if value in self._could_be_number:
            self._could_be_number.remove(value)
            if len(self._could_be_number) == 1:
                self.set_num(self._could_be_number.pop())
            return True
        return False

    def get_set(self):
        return self._could_be_number

    def get_num(self):
        return self._value

    def is_solved(self):
        return self._is_solved
