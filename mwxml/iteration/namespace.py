import mwtypes


class Namespace(mwtypes.Namespace):
    @classmethod
    def from_element(cls, element):
        return cls(
            element.attr('key'),
            element.text or "",
            case=element.attr('case')
        )
