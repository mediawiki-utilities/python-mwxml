"""
This library contains a collection of utilities for efficiently processing
MediaWiki's XML database dumps.  There are two important concerns that this
module intends to address: *performance* and the *complexity* of streaming
XML parsing.

Complexity
    Streaming XML parsing is gross.  XML dumps are (1) some site meta data, (2)
    a collection of pages that contain (3) collections of revisions.  The
    module allows you to think about dump files in this way and ignore the
    fact that you're streaming XML.  A `Dump()` contains
    a `SiteInfo()` and an iterator of `Page()`'s.  A
    `Page()` contains page meta data and an iterator of
    `Revision()`'s.  A `Revision()` contains revision meta data and text.

Performance
    Performance is a serious concern when processing large database XML dumps.
    Regretfully, python's Global Intepreter Lock prevents us from running
    threads on multiple CPUs.  This library provides `map()`, a
    function that maps a dump processing over a set of dump files using
    `multiprocessing` to distribute the work over multiple CPUS

"""
from .map import map
from .iteration import Dump, Page, Revision, SiteInfo, Namespace

__all__ = [map, Dump, Page, Revision, SiteInfo, Namespace]

__version__ = "0.2.2"
