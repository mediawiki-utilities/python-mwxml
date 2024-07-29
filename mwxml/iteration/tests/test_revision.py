import mwtypes
from ...element_iterator import ElementIterator
from ..revision import Revision


def test_old_revision():
    XML = """
    <revision>
      <id>233192</id>
      <timestamp>2001-01-21T02:12:21Z</timestamp>
      <contributor>
        <username>RoseParks</username>
        <id>99</id>
      </contributor>
      <comment>*</comment>
      <minor />
      <model>wikitext</model>
      <format>text/x-wiki</format>
      <text xml:space="preserve">Text of rev 233192</text>
      <sha1>8kul9tlwjm9oxgvqzbwuegt9b2830vw</sha1>
    </revision>
    """
    revision = Revision.from_element(ElementIterator.from_string(XML))
    assert revision.id == 233192
    assert revision.timestamp == mwtypes.Timestamp("2001-01-21T02:12:21Z")
    assert revision.user.id == 99
    assert revision.user.text == "RoseParks"
    assert revision.comment == "*"
    assert revision.minor == True
    assert revision.model == "wikitext"
    assert revision.format == "text/x-wiki"
    assert revision.text == "Text of rev 233192"
    assert revision.sha1 == "8kul9tlwjm9oxgvqzbwuegt9b2830vw"
    assert revision.deleted.text == False
    assert revision.deleted.comment == False
    assert revision.deleted.user == False

    XML = """
    <revision>
      <id>233192</id>
      <timestamp>2001-01-21T02:12:21Z</timestamp>
      <contributor deleted="deleted"></contributor>
      <comment deleted="deleted" />
      <minor />
      <model>wikitext</model>
      <format>text/x-wiki</format>
      <text xml:space="preserve" deleted="deleted" />
      <sha1>8kul9tlwjm9oxgvqzbwuegt9b2830vw</sha1>
    </revision>
    """
    revision = Revision.from_element(ElementIterator.from_string(XML))
    assert revision.user == None
    assert revision.comment == None
    assert revision.text == None
    assert revision.deleted.text == True
    assert revision.deleted.comment == True
    assert revision.deleted.user == True


def test_new_revision():
    XML = """
    <revision>
      <id>233192</id>
      <timestamp>2001-01-21T02:12:21Z</timestamp>
      <contributor>
        <username>RoseParks</username>
        <id>99</id>
      </contributor>
      <comment>*</comment>
      <minor />
      <model>wikitext</model>
      <format>text/x-wiki</format>
      <text sha1="8kul9tlwjm9oxgvqzbwuegt9b2830vw" deleted="deleted" xml:space="preserve">Text of rev 233192</text>
      <sha1>93284629347293</sha1>
      <content>
        <role>label_data</role>
        <origin>123</origin>
        <model>JadeEntity</model>
        <format>text/json</format>
        <id>1234</id>
        <text deleted="deleted" location="file://dev/null" bytes="234" sha1="ahgsvdjasvbdj3723">{"i_am": "json"}</text>
      </content>
    </revision>
    """  # noqa
    revision = Revision.from_element(ElementIterator.from_string(XML))
    assert revision.id == 233192
    assert revision.timestamp == mwtypes.Timestamp("2001-01-21T02:12:21Z")
    assert revision.user.id == 99
    assert revision.user.text == "RoseParks"
    assert revision.comment == "*"
    assert revision.minor == True
    assert revision.model == "wikitext"
    assert revision.format == "text/x-wiki"
    assert revision.text == "Text of rev 233192"
    assert revision.sha1 == "8kul9tlwjm9oxgvqzbwuegt9b2830vw"
    assert revision.deleted.text == True
    assert revision.deleted.comment == False
    assert revision.deleted.user == False
    assert revision.slots.sha1 == "93284629347293"
    assert (revision.slots['main'].sha1 ==
        "8kul9tlwjm9oxgvqzbwuegt9b2830vw")
    assert revision.slots['main'].text == "Text of rev 233192"
    assert revision.slots['main'].format == "text/x-wiki"
    assert revision.slots['label_data'].role == "label_data"
    assert revision.slots['label_data'].origin == 123
    assert revision.slots['label_data'].model == "JadeEntity"
    assert revision.slots['label_data'].format == "text/json"
    assert revision.slots['label_data'].id == "1234"
    assert revision.slots['label_data'].deleted == True
    assert revision.slots['label_data'].location == "file://dev/null"
    assert revision.slots['label_data'].bytes == 234
    assert revision.slots['label_data'].sha1 == "ahgsvdjasvbdj3723"
