import mwtypes

from ..errors import MalformedXML
from .user import User


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
        comment = None
        comment_deleted = False
        text = None
        text_deleted = False
        bytes = None
        sha1 = None
        parent_id = None
        model = None
        format = None

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
                if not text_deleted:
                    text = sub_element.text
                bytes = sub_element.attr('bytes')
            else:
                raise MalformedXML("Unexpected tag found when processing " +
                                   "a <revision>: '{0}'".format(tag))

        deleted = cls.Deleted(comment=comment_deleted, text=text_deleted,
                              user=user_deleted)

        return cls(
            id, timestamp,
            user=user,
            minor=minor,
            bytes=bytes,
            sha1=sha1,
            parent_id=parent_id,
            model=model,
            format=format,
            comment=comment,
            text=text,
            deleted=deleted
        )
