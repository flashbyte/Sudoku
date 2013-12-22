import logging
import sys
import threading
import BulkRemover

class Solver(object):

    def __init__(self, field):
        self.field = field

    def _update_possibilities(self):
        solver_remover_list = [
            self._remove_possibilities_from_rows,
            self._remove_possibilities_from_cols,
            self._remove_possibilities_from_blocks,
            ]
        changed = True
        while (changed):
            changed = False
            for solver in solver_remover_list:
                if solver():
                    changed = True
                logging.debug("*** debug after solver %s ***" % (solver))
                logging.debug(self.field)
                logging.debug("*** debug end ***")
                if not self.field.validate():
                    logging.error('%s medded up %s', solver)
                    sys.exit(2)
        return changed

    def _scanning(self):
        """
        asdfasdf asdfasdf
        """
        solver_scanner_list = [
            self._scanning_rows,
            self._scanning_cols,
            self._scanning_blocks,
            ]
        for solver in solver_scanner_list:
            if solver():
                logging.debug('Solver %s changed something', solver.__func__)
                if not self.field.validate():
                    logging.error('Solver %s messed up', solver.__func__)
                    logging.debug(self.field)
                    sys.exit(2)
                return True
        return False

    """ Solver functions sould only work on posibilities NOT on the number value
    the number value is updated by self._update_field """
    def solve(self):
        success = False
        changed = True
        while changed:
            changed = False
            self._update_possibilities()
            logging.debug("*** debug after update_possibilities() ***")
            logging.debug(self.field)
            logging.debug("*** debug end after possibilities ***")
            if self._scanning():
                changed = True
            if self.field.is_solved():
                success = True

        return success

    # -------- Remover algorithems --------

    def _remove_possibilites_from_bulk(self, bulk):
        changed = False
        bulk_removers = []
        for element in bulk:
            bulk_remover = BulkRemover.BulkRemover(element)
            bulk_removers.append(bulk_remover)
            bulk_remover.start()

        for bulk_remover in bulk_removers:
            bulk_remover.join()
            changed = changed or bulk_remover.changed

        return changed

    def _remove_possibilities_from_rows(self):
        return self._remove_possibilites_from_bulk(self.field._field)

    def _remove_possibilities_from_cols(self):
        columns = [self.field._get_col_as_list(columnIndex) for columnIndex in range(9)]

        return self._remove_possibilites_from_bulk(columns)

    def _remove_possibilities_from_blocks(self):
        blocks = [self.field._get_block_as_list(blockIndex) for blockIndex in range(1, 10)]

        return self._remove_possibilites_from_bulk(blocks)

    # -------- Scanner algorithmes --------
    def _scanning_bulk(self, bulk):
        changed = False
        # Make Union
        bulk_union = set()
        for element in bulk:
            bulk_union = bulk_union.union(element.get_set())
            # Make intesec list
        intesec_list = []
        for element in bulk:
            for element_intersec in bulk:
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
            changed = True

        # Set found uniq numbers
        for num in result_set:
            element_index = 0
            for element in bulk:
                if num in element.get_set():
                    if num == 8:
                        logging.debug('Possibilities list %s for element: %s', element.get_set(), element_index)
                    my_set = set()
                    my_set.add(num)
                    element.set_possibilities(my_set)
                    logging.debug('Setting value %s for element: %s', num, element_index)
                    logging.debug(self.field)
                element_index += 1
        return changed

    def _scanning_rows(self):
        changed = False
        row_index = 0
        for row in self.field._field:
            logging.debug('Scanning row: %s', row_index)
            if self._scanning_bulk(row):
                changed = True
            row_index += 1
        return changed

    def _scanning_cols(self):
        changed = False
        for col in range(9):
            col_list = self.field._get_col_as_list(col)
            if self._scanning_bulk(col_list):
                changed = True
        return changed

    def _scanning_blocks(self):
        changed = False
        for block_id in range(1, 10):
            block = self.field._get_block_as_list(block_id)
            if self._scanning_bulk(block):
                changed = True
        return changed
