import mwtypes


class Namespace(mwtypes.Namespace):
    """
    See :class:`mwtypes.Namespace` for a description of fields
    """
    @classmethod
    def from_element(cls, element):
        return cls(
            element.attr('key'),
            element.text or "",
            case=element.attr('case')
        )
