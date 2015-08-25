import logging
import time
import traceback
from multiprocessing import Process, Queue, cpu_count
from queue import Empty
from threading import Thread

from .. import files
from ..iteration import Dump

logger = logging.getLogger(__name__)

def map(process, paths, threads=None):
    threads = min(max(1, threads or cpu_count()), len(paths))

    # Load paths into the queue
    paths = enqueue(files.normalize_path(path) for path in paths)

    # Prepare the output queue
    output = Queue()

    # Prepare the logs queue
    qlogger = QueueLogger()
    qlogger.start()

    # Prepare the mappers and start them
    mappers = [Mapper(process, paths, output, qlogger, str(i))
               for i in range(threads)]
    for mapper in mappers:
        mapper.start()

    # Read from the output queue while there's still a mapper alive or something
    # in the queue to read.
    while sum(m.is_alive() for m in mappers) > 0 or not output.empty():
        try:
            # if there's nothing in the queue for 0.1 seconds, check if the
            # any mappers are still alive
            error, value = output.get(timeout=0.1)

            if error is None:
                yield value
            else:
                raise error

        except Empty:
            # This is going to happen when mappers aren't adding values to the
            # queue fast enough
            pass


def enqueue(items):
    queue = Queue()
    for item in items:
        queue.put(item)

    return queue


class Mapper(Process):

    def __init__(self, process, paths, output, logger, name=None):
        super().__init__(name="XML Dump Mapper {0}".format(name), daemon=True)
        self.process = process
        self.paths = paths
        self.output = output
        self.logger = logger
        self.stats = []

    def run(self):
        logger.info("{0}: Starting up.".format(self.name))
        try:
            while True:
                path = self.paths.get(timeout=0.05) # Get a path
                self.logger.info("{0}: Processing {1}".format(self.name, path))
                try:
                    start_time = time.time()
                    dump = Dump.from_file(files.open(path))
                    count = 0
                    for value in self.process(dump, path):
                        self.output.put((None, value))
                        count += 1
                    self.stats.append((path, count, time.time() - start_time))
                except Exception as e:
                    self.logger.error(
                        "{0}: An error occured while processing {1}"
                        .format(self.name, path)
                    )
                    formatted = traceback.format_exc(chain=False)
                    self.logger.error("{0}: {1}".format(self.name, formatted))
                    self.output.put((e, None))
                    return # Exits without polluting stderr
        except Empty:
            self.logger.info("{0}: No more paths to process".format(self.name))
            self.logger.info("\n" + "\n".join(self.format_stats()))

    def format_stats(self):
        for path, outputs, duration in self.stats:
            yield "{0}: - Extracted {1} values from {2} in {3} seconds" \
                        .format(self.name, outputs, path, duration)


class QueueLogger(Thread):

    def __init__(self, logger=None):
        super().__init__(daemon=True)
        self.queue = Queue()

    def debug(self, message):
        self.queue.put((logging.DEBUG, message))

    def info(self, message):
        self.queue.put((logging.INFO, message))

    def warning(self, message):
        self.queue.put((logging.WARNING, message))

    def error(self, message):
        self.queue.put((logging.ERROR, message))

    def run(self):
        while True:
            try:
                level, message = self.queue.get(timeout=0.1)
                logger.log(level, message)
            except Empty:
                continue
