import logging
import sys
import BulkRemover
import BulkScanner

class Solver(object):

    def __init__(self, field):
        self.field = field

    def solve(self):
        """
        Solver functions should only work on possibilities NOT on the number value
        the number value is updated by self._update_field
        """
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
        bulk_scanners = []
        for element in bulk:
            bulk_scanner = BulkScanner.BulkScanner(element)
            bulk_scanners.append(bulk_scanner)
            bulk_scanner.start()

        for bulk_scanner in bulk_scanners:
            bulk_scanner.join()
            changed = changed or bulk_scanner.changed

        return changed

    def _scanning_rows(self):

        return self._scanning_bulk(self.field._field)
        #
        # changed = False
        # row_index = 0
        #
        #
        #
        # for row in self.field._field:
        #     logging.debug('Scanning row: %s', row_index)
        #     if self._scanning_bulk(row):
        #         changed = True
        #     row_index += 1
        # return changed

    def _scanning_cols(self):

        columns = [self.field._get_col_as_list(columnIndex) for columnIndex in range(9)]

        return self._scanning_bulk(columns)
        #
        # changed = False
        # for col in range(9):
        #     col_list = self.field._get_col_as_list(col)
        #     if self._scanning_bulk(col_list):
        #         changed = True
        # return changed

    def _scanning_blocks(self):

        blocks = [self.field._get_block_as_list(blockIndex) for blockIndex in range(1, 10)]

        return self._scanning_bulk(blocks)

        # changed = False
        # for block_id in range(1, 10):
        #     block = self.field._get_block_as_list(block_id)
        #     if self._scanning_bulk(block):
        #         changed = True
        # return changed
