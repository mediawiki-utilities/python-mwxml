import logging

import mwtypes.files

from ..element_iterator import ElementIterator
from ..errors import MalformedXML
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

            from mwxml import Dump

            # Construct dump file iterator
            dump = Dump.from_file(open("example/dump.xml"))

            # Iterate through pages
            for page in dump:

                # Iterate through a page's revisions
                for revision in page:

                    print(revision.id)

    """

    def __init__(self, site_info, pages):

        self.site_info = SiteInfo(site_info)
        """
        Metadata from the <siteinfo> tag :
        :class:`~mwxml.iteration.site_info.SiteInfo`
        """

        # Should be a lazy generator of page info
        self.pages = pages or range(0)

    def __iter__(self):
        return self.pages

    def __next__(self):
        return next(self.pages)

    @classmethod
    def load_pages(cls, first_page, element, namespace_map):
        if first_page is not None:
            yield Page.from_element(first_page, namespace_map)

        for sub_element in element:
            tag = sub_element.tag

            if tag == "page":
                yield Page.from_element(sub_element, namespace_map)
            else:
                assert MalformedXML("Expected to see <page>.  " +
                                    "Instead saw <{0}>".format(tag))

    @classmethod
    def from_element(cls, element):

        site_info = None
        first_page = None

        # Consume <siteinfo>
        for sub_element in element:
            tag = sub_element.tag
            if tag == "siteinfo":
                site_info = SiteInfo.from_element(sub_element)
            elif tag == "page":
                first_page = sub_element
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

        # Consume all <page>
        pages = cls.load_pages(first_page, element, namespace_map)

        return cls(site_info, pages)

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
