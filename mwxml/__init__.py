"""
This module is a collection of utilities for efficiently processing MediaWiki's
XML database dumps.  There are two important concerns that this module intends
to address: *performance* and the *complexity* of streaming XML parsing.

Performance
    Performance is a serious concern when processing large database XML dumps.
    Regretfully, the Global Intepreter Lock prevents us from running threads on
    multiple CPUs.  This library provides a :func:`map`, a function
    that maps a dump processing over a set of dump files using
    :class:`multiprocessing` to distribute the work over multiple CPUS

Complexity
    Streaming XML parsing is gross.  XML dumps are (1) some site meta data, (2)
    a collection of pages that contain (3) collections of revisions.  The
    module allows you to think about dump files in this way and ignore the
    fact that you're streaming XML.  An :class:`Dump` contains
    :class:`SiteInfo` and an iterator of :class:`Page`'s.  A
    :class:`Page` contains page meta data and an iterator of
    :class:`Revision`'s.  A :class:`Revision` contains revision meta data
    including a :class:`User` (if one a contributor was specified in the
    XML).

"""
from .map import map
from .iteration import *
__version__ = "0.0.4"
