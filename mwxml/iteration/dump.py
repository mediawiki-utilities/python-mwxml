import logging

import mwtypes.files

from ..element_iterator import ElementIterator
from ..errors import MalformedXML
from .log_item import LogItem
from .page import Page
from .site_info import SiteInfo

logger = logging.getLogger(__name__)


class Dump:
    """
    XML Dump Iterator. Dump file meta data and a
    :class:`~mwxml.iteration.page.Page` iterator.  Instances of this class can
    be called as an iterator directly.  Usually, you'll want to construct this
    class using :func:`~mwxml.iteration.dump.Dump.from_file`.

    :Parameters:
        site_info : :class:`~mwxml.iteration.site_info.SiteInfo`
            The data from the <siteinfo> block
        pages : `iterable`
            An `iterable` of :class:`~mwxml.iteration.page.Page` in the order
            they appear in the XML

    :Example:
        .. code-block:: python

            from mwxml import Dump, Page

            # Construct dump file iterator
            dump = Dump.from_file(open("example/dump.xml"))

            # Iterate through pages
            for page in dump.pages:
                # Iterate through a page's revisions
                for revision in page:
                    print(revision.id)
    :Attributes:

        .. autoattribute:: mwxml.Dump.site_info
            :annotation: = Information from the <siteinfo> block :
                           mwxml.SiteInfo

        .. autoattribute:: mwxml.Dump.pages
            :annotation: = The mwxml.Page that appear in the dump : iterator

        .. autoattribute:: mwxml.Dump.items
            :annotation: = The mwxml.Page and/or mwxml.LogItem that appear in
                           the dump : iterator

        .. autoattribute:: mwxml.Dump.log_items
            :annotation: = The mwxml.LogItem that appear in the dump : iterator
    """
    __slots__ = ('site_info', 'items', 'pages', 'log_items')

    def __init__(self, site_info, items):

        self.site_info = SiteInfo(site_info)
        """
        Metadata from the <siteinfo> tag :
        :class:`~mwxml.iteration.site_info.SiteInfo`
        """

        # Should be a lazy generator of page info
        self.items = items or range(0)
        """
        An iterator of :class:`mwxml.Page` and/or
        :class:`mwxml.LogItem` elements
        """
        self.pages = (item for item in items if isinstance(item, Page))
        "An iterator of :class:`mwxml.Page` elements"
        self.log_items = (item for item in items if isinstance(item, LogItem))
        "An iterator of :class:`mwxml.LogItem` elements"

    def __iter__(self):
        return self.items

    def __next__(self):
        return next(self.items)

    @classmethod
    def load_items(cls, first_item_element, element, namespace_map):
        if first_item_element is not None:
            yield cls.process_item(first_item_element, namespace_map)
            # Ensure that we completely current tag block
            first_item_element.clear()

        for item_element in element:
            yield cls.process_item(item_element, namespace_map)

    @classmethod
    def process_item(cls, item_element, namespace_map):
        if item_element.tag == "page":
            return Page.from_element(item_element, namespace_map)
        elif item_element.tag == "logitem":
            return LogItem.from_element(item_element, namespace_map)
        else:
            raise MalformedXML("Expected to see <page> or <logitem>.  " +
                               "Instead saw <{0}>".format(item_element.tag))

    @classmethod
    def from_element(cls, element):

        site_info = None
        first_item_element = None

        # Consume <siteinfo>
        for sub_element in element:
            if sub_element.tag == "siteinfo":
                site_info = SiteInfo.from_element(sub_element)
            elif sub_element.tag in ("page", "logitem"):
                first_item_element = sub_element
                break
            # Assuming that the first <page> seen marks the end of dump
            # metadata.  I'm not too keen on this assumption, so I'm leaving
            # this long comment to warn whoever ends up maintaining this.
            else:
                raise MalformedXML("Unexpected tag found when processing " +
                                   "a <mediawiki>: '{0}'".format(tag))

        namespace_map = None
        if site_info.namespaces is not None:
            namespace_map = {}
            for namespace in site_info.namespaces:
                namespace_map[namespace.name] = namespace

        # Consume all <page> and <logitem>
        items = cls.load_items(first_item_element, element, namespace_map)

        return cls(site_info, items)

    @classmethod
    def from_file(cls, f):
        """
        Constructs a :class:`~mwxml.iteration.dump.Dump` from a `file` pointer.

        :Parameters:
            f : `file`
                A plain text file pointer containing XML to process
        """
        element = ElementIterator.from_file(f)
        assert element.tag == "mediawiki"
        return cls.from_element(element)

    @classmethod
    def from_page_xml(cls, page_xml):
        """
        Constructs a :class:`~mwxml.iteration.dump.Dump` from a <page> block.

        :Parameters:
            page_xml : `str` | `file`
                Either a plain string or a file containing <page> block XML to
                process
        """
        header = """
        <mediawiki xmlns="http://www.mediawiki.org/xml/export-0.5/"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.5/
                     http://www.mediawiki.org/xml/export-0.5.xsd" version="0.5"
                   xml:lang="en">
        <siteinfo>
        </siteinfo>
        """

        footer = "</mediawiki>"

        return cls.from_file(mwtypes.files.concat(header, page_xml, footer))
