import mwtypes

from ..errors import MalformedXML
from .revision import Revision


class Page(mwtypes.Page):
    """
    Page meta data and a :class:`~mw.xml_dump.Revision` iterator.  Instances of
    this class can be called as iterators directly. See :class:`mwtypes.Page`
    for a description of fields.

    :Example:
        .. code-block:: python

            page = mwxml.Page( ... )

            for revision in page:
                print("{0} {1}".format(revision.id, page_id))
    """
    def initialize(self, *args, revisions=None, **kwargs):
        super().initialize(*args, **kwargs)

        # Should be a lazy generator
        self.__revisions = revisions

    def __iter__(self):
        return self.__revisions

    def __next__(self):
        return next(self.__revisions)

    @classmethod
    def load_revisions(cls, first_revision, element):
        if first_revision is not None:
            yield Revision.from_element(first_revision)

        for sub_element in element:
            tag = sub_element.tag

            if tag == "revision":
                yield Revision.from_element(sub_element)
            else:
                raise MalformedXML("Expected to see <revision>.  " +
                                   "Instead saw <{0}>".format(tag))

    @classmethod
    def from_element(cls, element):
        title = None
        namespace = None
        id = None
        redirect = None
        restrictions = []

        first_revision = None

        # Consume each of the elements until we see <revision> which should
        # signal the start of revision data
        for sub_element in element:
            tag = sub_element.tag
            if tag == "title":
                title = sub_element.text
            elif tag == "ns":
                namespace = int(sub_element.text)
            elif tag == "id":
                id = int(sub_element.text)
            elif tag == "redirect":
                redirect = sub_element.attr('title')
            elif tag == "restrictions":
                restrictions.append(sub_element.text)
            elif tag == "revision":
                first_revision = sub_element
                break
            # Assuming that the first revision seen marks the end of page
            # metadata.  I'm not too keen on this assumption, so I'm leaving
            # this long comment to warn whoever ends up maintaining this.
            else:
                raise MalformedXML("Unexpected tag found when processing " +
                                   "a <page>: '{0}'".format(tag))

        # Assuming that I got here by seeing a <revision> tag.  See verbose
        # comment above.
        revisions = cls.load_revisions(first_revision, element)


        # Normalize title
        title = normalize_title(title, namespace)

        # Construct class
        return cls(id, title, namespace, redirect=redirect,
                   restrictions=restrictions, revisions=revisions)


def normalize_title(title, namespace):
    title_parts = title.split(":", 1)
    if namespace == 0 or len(title_parts) == 1:
        return title.replace("_", " ")
    else:
        return title_parts[1].replace("_", " ")
