from ...element_iterator import ElementIterator
from ..user import User


def test_user():
    XML = """
    <contributor>
      <username>Gen0cide</username>
      <id>92182</id>
    </contributor>
    """
    user = User.from_element(ElementIterator.from_string(XML))
    assert user.id == 92182
    assert user.text == "Gen0cide"

    XML = """
    <contributor>
      <ip>192.168.0.1</ip>
    </contributor>
    """
    user = User.from_element(ElementIterator.from_string(XML))
    assert user.id == None
    assert user.text == "192.168.0.1"

    XML = """
    <contributor>
      <username></username>
      <id></id>
    </contributor>
    """
    user = User.from_element(ElementIterator.from_string(XML))
    assert user.id == 0
    assert user.text == "None"
