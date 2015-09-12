# MediaWiki XML

This library contains a collection of utilities for efficiently 
processing MediaWiki’s XML database dumps. There are two 
important concerns that this module intends to address: 
complexity and performance of streaming XML parsing.  This library
enables memory efficent stream processing of XML dumps with 
a simple [`iterator`](https://pythonhosted.org/mwxml/iteration.html) 
strategy.  This library also implements a distributed
processing strategy (see 
[`map()`](https://pythonhosted.org/mwxml/map.html)) that enables parallel
processing of many XML dump files at the same time. 

* **Installation:** ``pip install mwxml``
* **Documentation:** https://pythonhosted.org/mwxml
* **Repositiory:** https://github.com/mediawiki-utilities/python-mwxml
* **License:** MIT

## Example

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
    
## Author
* Aaron Halfaker -- https://github.com/halfak

## See also 
* http://dumps.wikimedia.org/
* http://community.wikia.com/wiki/Help:Database_download
