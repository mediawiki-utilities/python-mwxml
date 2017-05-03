"""
This library contains a collection of utilities for efficiently processing
MediaWiki's XML database dumps.  There are two important concerns that this
module intends to address: *performance* and the *complexity* of streaming
XML parsing.

:Complexity:
    Streaming XML parsing is gross.  XML dumps are (1) some site meta data, (2)
    a collection of pages that contain (3) collections of revisions.  The
    module allows you to think about dump files in this way and ignore the
    fact that you're streaming XML.  A :class:`mwxml.Dump` contains
    a :class:`mwxml.SiteInfo` and an iterator of :class:`mwxml.Page`'s and/or
    :class:`mwxml.LogItem`'s.  For dumps that contain ``<page>`` tags,
    a :class:`mwxml.Page` contains page meta data
    and an iterator of :class:`mwxml.Revision()`'s.
    A :class:`mwxml.Revision()` contains revision meta data and text.
    For dumps that contain ``<logitem>``, a :class:`mwxml.LogItem` contains
    meta data.

:Performance:
    Performance is a serious concern when processing large database XML dumps.
    Regretfully, python's Global Interpreter Lock prevents us from running
    threads on multiple CPUs.  This library provides :func:`mwxml.map`, a
    function that maps a dump processing over a set of dump files using
    :mod:`multiprocessing` to distribute the work over multiple CPUS

"""
from .map import map
from .iteration import Dump, Page, LogItem, Revision, SiteInfo, Namespace
from .about import (__name__, __version__, __author__, __author_email__,
                    __description__, __license__, __url__)

__all__ = [map, Dump, Page, LogItem, Revision, SiteInfo, Namespace,
           __name__, __version__, __author__, __author_email__,
           __description__, __license__, __url__]
