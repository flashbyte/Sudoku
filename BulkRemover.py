import threading


class BulkRemover (threading.Thread):
    """
    Removes all possibilities from a bulk where bulk could be a row, a col or a block
    """

    def __init__(self, bulk):
        threading.Thread.__init__(self)

        self.bulk = bulk
        self.changed = False

    def run(self):

        for element in self.bulk:
            if element.is_solved():
                for element_remove in self.bulk:
                    if element_remove.remove_posibility(element.get_num()):
                        self.changed = True