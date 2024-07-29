from ...element_iterator import ElementIterator
from ..namespace import Namespace


def test_namespace():
    XML = '<namespace key="0" case="first-letter" />'
    namespace = Namespace.from_element(ElementIterator.from_string(XML))
    assert namespace.id == 0
    assert namespace.name == ""
    assert namespace.aliases == None
    assert namespace.case == "first-letter"
    assert namespace.canonical == None

    XML = '<namespace key="711" case="first-letter">TimedText talk</namespace>'
    namespace = Namespace.from_element(ElementIterator.from_string(XML))
    assert namespace.id == 711
    assert namespace.name == "TimedText talk"
    assert namespace.aliases == None
    assert namespace.case == "first-letter"
    assert namespace.canonical == None
