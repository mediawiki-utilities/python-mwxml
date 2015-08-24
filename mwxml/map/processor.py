import logging
import traceback
from collections import namedtuple
from multiprocessing import Process
from queue import Empty

from .. import files
from ..iteration import Dump

logger = logging.getLogger("mw.dump.processor")

ErrorItem = namedtuple("ErrorItem", ['error', 'item'])

class DONE: pass


class Processor(Process):
    def __init__(self, pathq, outputq, process_dump, logger=logger):
        self.pathq = pathq
        self.outputq = outputq
        self.process_dump = process_dump
        self.logger = logger
        Process.__init__(self)

    def run(self):
        try:
            while True:

                # Force the queue to reset & behave reasonably
                foo = self.pathq.qsize()
                path = self.pathq.get(block=False)
                dump = Dump.from_file(files.open(path))
                logger.info("Beginning to process {0}.".format(repr(path)))
                try:
                    for out in self.process_dump(dump, path):
                        self.outputq.put(ErrorItem(False, out))
                except Exception as error:
                    logger.error(
                        "Failed while processing dump " +
                        "{0}: {1}".format(repr(path),
                                          "\n" + traceback.format_exc()))
                    self.outputq.put(ErrorItem(True, (error, path)))
        except Empty:
            self.logger.info("Nothing left to do.  Shutting down thread.")
        finally:
            self.outputq.put(ErrorItem(False, DONE))
