# MediaWiki XML dump processing

This library provides a set of utilities for efficiently processing MediaWiki's
XML dump output  

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
