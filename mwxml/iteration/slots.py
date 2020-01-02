import logging

import mwtypes

from ..errors import MalformedXML

logger = logging.getLogger(__name__)


class Slots(mwtypes.Slots):
    pass


class Content(mwtypes.Content):
    """
    Content metadata and text.  See :class:`mwtypes.Content` for a
    description of fields.
    """

    @classmethod
    def from_element(cls, element):
        role = None
        origin = None
        model = None
        format = None
        deleted = None
        id = None
        location = None
        bytes = None
        sha1 = None
        text = None

        for sub_element in element:
            tag = sub_element.tag
            if tag == "role":
                role = sub_element.text
            elif tag == "origin":
                origin = sub_element.text
            elif tag == "model":
                model = sub_element.text
            elif tag == "format":
                format = sub_element.text
            elif tag == "id":
                id = sub_element.text
            elif tag == "text":
                deleted = sub_element.attr('deleted') is not None
                location = sub_element.attr('location')
                bytes = sub_element.attr('bytes')
                sha1 = sub_element.attr('sha1')
                text = sub_element.text or None
            else:
                raise MalformedXML("Unexpected tag found when processing " +
                                   "a <revision>: '{0}'".format(tag))

        return cls(
            role=role,
            origin=origin,
            model=model,
            format=format,
            deleted=deleted,
            location=location,
            id=id,
            bytes=bytes,
            sha1=sha1,
            text=text)
