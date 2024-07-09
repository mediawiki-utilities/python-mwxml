import logging

import mwtypes

from ..errors import MalformedXML
from .slots import Content, Slots
from .user import User

logger = logging.getLogger(__name__)


class Revision(mwtypes.Revision):
    """
    Revision metadata and text.  See :class:`mwtypes.Revision` for a
    description of fields.
    """

    @classmethod
    def from_element(cls, element):

        id = None
        timestamp = None
        user = None
        user_deleted = False
        minor = False
        origin = None
        comment = None
        comment_deleted = False
        text = None
        text_deleted = False
        text_sha1 = None
        text_bytes = None
        text_id = None
        text_location = None
        sha1 = None
        parent_id = None
        model = None
        format = None
        contents = []

        for sub_element in element:
            tag = sub_element.tag
            if tag == "id":
                id = int(sub_element.text)
            elif tag == "timestamp":
                timestamp = mwtypes.Timestamp(sub_element.text)
            elif tag == "contributor":
                user_deleted = sub_element.attr('deleted') is not None
                if not user_deleted:
                    user = User.from_element(sub_element)
            elif tag == "minor":
                minor = True
            elif tag == "origin":
                origin = sub_element.text
            elif tag == "sha1":
                sha1 = sub_element.text
            elif tag == "parentid":
                parent_id = sub_element.text
            elif tag == "model":
                model = sub_element.text
            elif tag == "format":
                format = sub_element.text
            elif tag == "comment":
                comment_deleted = sub_element.attr('deleted') is not None
                if not comment_deleted:
                    comment = sub_element.text
            elif tag == "text":
                text_deleted = sub_element.attr('deleted') is not None
                text = sub_element.text or None
                text_sha1 = sub_element.attr('sha1')
                text_bytes = sub_element.attr('bytes')
                text_id = sub_element.attr('id')
                text_location = sub_element.attr('location')
            elif tag == "content":
                contents.append(Content.from_element(sub_element))
            else:
                raise MalformedXML("Unexpected tag found when processing " +
                                   "a <revision>: '{0}'".format(tag))

        deleted = cls.Deleted(comment=comment_deleted, text=text_deleted,
                              user=user_deleted)

        if text_sha1 is not None:
            # We are working with the new format
            contents.insert(0, Content(
                role="main", model=model, deleted=text_deleted,
                format=format, bytes=text_bytes, sha1=text_sha1, id=text_id,
                location=text_location, text=text))
        elif len(contents) == 0:
            # We are working with the old format
            contents.insert(0, Content(
                role="main", model=model, deleted=text_deleted,
                format=format, bytes=text_bytes, sha1=sha1, text=text))
        else:
            logger.warning("Found a <content> tag but no sha1 attribute " +
                           "on the <text> tag.  Should be impossible.")

        slots = Slots(sha1=sha1, contents={content.role: content
                                           for content in contents})

        return cls(
            id, timestamp,
            user=user,
            minor=minor,
            parent_id=parent_id,
            comment=comment,
            deleted=deleted,
            slots=slots
        )
