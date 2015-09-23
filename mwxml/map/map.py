import logging

import mwtypes.files
import para

from ..iteration import Dump

logger = logging.getLogger(__name__)


def map(process, paths, threads=None):
    """
    Implements a distributed stategy for processing XML files.  This
    function constructs a set of py:mod:`multiprocessing` threads (spread over
    multiple cores) and uses an internal queue to aggregate outputs.  To use
    this function, implement a `process()` function that takes two arguments
    -- a :class:`mwxml.Dump` and the path the dump was loaded
    from. Anything that this function ``yield``s will be `yielded` in turn
    from the :func:`mwxml.map` function.

    :Parameters:
        paths : `iterable` ( `str` | `file` )
            a list of paths to dump files to process
        process : `func`
            A function that takes a :class:`~mwxml.iteration.dump.Dump` and the
            path the dump was loaded from and yields
        threads : int
            the number of individual processing threads to spool up

    :Example:

        >>> import mwxml
        >>> files = ["examples/dump.xml", "examples/dump2.xml"]
        >>>
        >>> def page_info(dump, path):
        ...     for page in dump:
        ...         yield page.id, page.namespace, page.title
        ...
        >>> for id, namespace, title in mwxml.map(page_info, files):
        ...     print(id, namespace, title)
        ...
    """
    paths = [mwtypes.files.normalize_path(path) for path in paths]

    def process_path(path):
        dump = Dump.from_file(mwtypes.files.reader(path))
        yield from process(dump, path)

    yield from para.map(process_path, paths, mappers=threads)
