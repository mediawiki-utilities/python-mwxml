MediaWiki XML Processing
========================
.. automodule:: mwxml


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


Authors
-------
* Aaron Halfaker -- https://github.com/halfak

Pull requests welcome @ https://github.com/halfak/python-mwxml


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
