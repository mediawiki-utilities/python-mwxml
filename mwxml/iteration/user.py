import mwtypes

from .util import consume_tags


class User(mwtypes.User):
    """
    User `id` and `text`.  See :class:`mwtypes.Revision.User` for a
    description of fields.
    """
    TAG_MAP = {
        'id': lambda e: int(e.text),
        'username': lambda e: str(e.text),
        'ip': lambda e: str(e.text)
    }

    @classmethod
    def from_element(cls, element):
        values = consume_tags(cls.TAG_MAP, element)

        return cls(
            values.get('id'),
            values.get('username', values.get('ip'))
        )
