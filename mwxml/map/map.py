import logging
import traceback
from multiprocessing import Queue, Value, cpu_count
from queue import Empty

from .. import files
from .processor import DONE, Processor

logger = logging.getLogger("mw.dump.map")


def re_raise(error, path):
    raise error



def map(paths, process_dump, handle_error=re_raise,
        threads=cpu_count(), output_buffer=100):
    """
    Maps a function across a set of dump files and returns
    an (order not guaranteed) iterator over the output.

    The `process_dump` function must return an iterable object (such as a
    generator).  If your process_dump function does not need to produce
    output, make it return an empty `iterable` upon completion (like an empty
    list).

    :Parameters:
        paths : iter( str )
            a list of paths to dump files to process
        process_dump : function( dump : :class:`~mw.xml_dump.Iterator`, path : str)
            a function to run on every :class:`~mw.xml_dump.Iterator`
        threads : int
            the number of individual processing threads to spool up
        output_buffer : int
            the maximum number of output values to buffer.

    :Returns:
        An iterator over values yielded by calls to `process_dump()`
    :Example:
        .. code-block:: python

            from mw import xml_dump

            files = ["examples/dump.xml", "examples/dump2.xml"]

            def page_info(dump, path):
                for page in dump:

                    yield page.id, page.namespace, page.title


            for page_id, page_namespace, page_title in xml_dump.map(files, page_info):
                print("\t".join([str(page_id), str(page_namespace), page_title]))
    """
    paths = list(paths)
    pathsq = queue_files(paths)
    outputq = Queue(maxsize=output_buffer)
    running = Value('i', 0)
    threads = max(1, min(int(threads), pathsq.qsize()))

    processors = []

    for i in range(0, threads):
        processor = Processor(
            pathsq,
            outputq,
            process_dump
        )
        processor.start()
        processors.append(processor)

    # output while processes are running
    done = 0
    while done < len(paths):
        try:
            error, item = outputq.get(timeout=.25)
        except Empty:
            continue

        if not error:
            if item is DONE:
                done += 1
            else:
                yield item
        else:
            error, path = item
            re_raise(error, path)


def queue_files(paths):
    """
    Produces a `multiprocessing.Queue` containing path for each value in
    `paths` to be used by the `Processor`s.

    :Parameters:
        paths : iterable
            the paths to add to the processing queue
    """
    q = Queue()
    for path in paths:
        if isinstance(path, str):
            q.put(files.normalize_path(path))
        else:
            q.put(path) # Probably a file already
    return q
