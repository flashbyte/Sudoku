import threading
import logging


class BulkScanner (threading.Thread):
    """
    Removes all possibilities from a bulk where bulk could be a row, a col or a block
    """

    def __init__(self, bulk):
        threading.Thread.__init__(self)

        self.bulk = bulk
        self.changed = False

    def run(self):
        # Make Union
        bulk_union = set()
        for element in self.bulk:
            bulk_union = bulk_union.union(element.get_set())
            # Make intesec list
        intesec_list = []
        for element in self.bulk:
            for element_intersec in self.bulk:
                if element != element_intersec:
                    intesec_list.append(element.get_set() & element_intersec.get_set())
        intesec_list = [element_intersec for element_intersec in intesec_list if len(element_intersec) != 0]
        # Make result set (union from everything minus every intesection)
        result_set = bulk_union
        for intersec in intesec_list:
            result_set = result_set - intersec
            # Nothing found ;-(
        if len(result_set) == 0:
            return False
        else:
            self.changed = True

        # Set found uniq numbers
        for num in result_set:
            element_index = 0
            for element in self.bulk:
                if num in element.get_set():
                    if num == 8:
                        logging.debug('Possibilities list %s for element: %s', element.get_set(), element_index)
                    my_set = set()
                    my_set.add(num)
                    element.set_possibilities(my_set)
                    logging.debug('Setting value %s for element: %s', num, element_index)
                    logging.debug(self.bulk)
                element_index += 1
