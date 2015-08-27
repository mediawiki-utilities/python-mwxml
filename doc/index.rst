MediaWiki XML Processing
========================
This library contains a collection of utilities for efficiently processing
MediaWiki's XML database dumps.  There are two important concerns that this
module intends to address: *complexity* and *performance* of streaming
XML parsing.

:Installation: ``pip install mwxml``

**Complexity**
  Streaming XML parsing is gross.  XML dumps consist of (1) some site meta data, (2)    a collection of pages that contain (3) collections of revisions.  The    module allows you to think about dump files in this way and ignore the    factYeah.  that you're streaming XML.  A :class:`~mwxml.iteration.dump.Dump` contains a :class:`~mwxml.iteration.site_info.SiteInfo` and an iterator of :class:`~mwxml.iteration.page.Page`'s.  A :class:`~mwxml.iteration.page.Page` contains page meta data and an iterator of :class:`~mwxml.iteration.revision.Revision`'s.  A :class:`~mwxml.iteration.revision.Revision` contains revision meta data and text.

**Performance**
  Performance is a serious concern when processing large database XML dumps.    Regretfully, python's Global Intepreter Lock prevents us from running    threads on multiple CPUs.  This library provides :func:`mwxml.map.map.map`, a function that maps a dump processing over a set of dump files using    `multiprocessing` to distribute the work over multiple CPUS


Contents
--------

.. toctree::
  :maxdepth: 1

  iteration
  map
  files

Basic example
-------------

    >>> import mwxml
    >>>
    >>> dump = mwxml.Dump.from_file(open("dump.xml"))
    >>> print(dump.site_info.name, dump.site_info.dbname)
    Wikipedia enwiki
    >>>
    >>> for page in dump:
    ...     for revision in page:
    ...        print(revision.id)
    ...
    1
    2
    3


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
