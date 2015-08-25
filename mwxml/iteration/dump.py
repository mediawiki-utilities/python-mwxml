import io
import logging

import jsonable

from .. import files
from ..element_iterator import ElementIterator
from ..errors import MalformedXML
from .page import Page
from .site_info import SiteInfo

logger = logging.getLogger(__name__)

class Dump:
    """
    XML Dump Iterator. Dump file meta data and a
    :class:`~mw.xml_dump.Page` iterator.  Instances of this class can be
    called as an iterator directly.  E.g.::

        from mw.xml_dump import Iterator

        # Construct dump file iterator
        dump = Iterator.from_file(open("example/dump.xml"))

        # Iterate through pages
        for page in dump:

            # Iterate through a page's revisions
            for revision in page:

                print(revision.id)

    """

    def __init__(self, site_info, pages):

        self.site_info = SiteInfo(site_info)

        # Should be a lazy generator of page info
        self.pages = pages or range(0)

    def __iter__(self):
        return self.pages

    def __next__(self):
        return next(self.pages)

    @classmethod
    def load_pages(cls, first_page, element):
        if first_page is not None:
            yield Page.from_element(first_page)

        for sub_element in element:
            tag = sub_element.tag

            if tag == "page":
                yield Page.from_element(sub_element)
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



        # Consume all <page>
        pages = cls.load_pages(first_page, element)

        return cls(site_info, pages)

    @classmethod
    def from_file(cls, f):
        element = ElementIterator.from_file(f)
        assert element.tag == "mediawiki"
        return cls.from_element(element)

    @classmethod
    def from_page_xml(cls, page_xml):
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

        return cls.from_file(files.concat(header, page_xml, footer))
