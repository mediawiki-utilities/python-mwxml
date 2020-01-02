import mwtypes
from nose.tools import eq_

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
    eq_(revision.id, 233192)
    eq_(revision.timestamp, mwtypes.Timestamp("2001-01-21T02:12:21Z"))
    eq_(revision.user.id, 99)
    eq_(revision.user.text, "RoseParks")
    eq_(revision.comment, "*")
    eq_(revision.minor, True)
    eq_(revision.model, "wikitext")
    eq_(revision.format, "text/x-wiki")
    eq_(revision.text, "Text of rev 233192")
    eq_(revision.sha1, "8kul9tlwjm9oxgvqzbwuegt9b2830vw")
    eq_(revision.deleted.text, False)
    eq_(revision.deleted.comment, False)
    eq_(revision.deleted.user, False)

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
    eq_(revision.user, None)
    eq_(revision.comment, None)
    eq_(revision.text, None)
    eq_(revision.deleted.text, True)
    eq_(revision.deleted.comment, True)
    eq_(revision.deleted.user, True)


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
    eq_(revision.id, 233192)
    eq_(revision.timestamp, mwtypes.Timestamp("2001-01-21T02:12:21Z"))
    eq_(revision.user.id, 99)
    eq_(revision.user.text, "RoseParks")
    eq_(revision.comment, "*")
    eq_(revision.minor, True)
    eq_(revision.model, "wikitext")
    eq_(revision.format, "text/x-wiki")
    eq_(revision.text, "Text of rev 233192")
    eq_(revision.sha1, "8kul9tlwjm9oxgvqzbwuegt9b2830vw")
    eq_(revision.deleted.text, True)
    eq_(revision.deleted.comment, False)
    eq_(revision.deleted.user, False)
    eq_(revision.slots.sha1, "93284629347293")
    eq_(revision.slots['main'].sha1,
        "8kul9tlwjm9oxgvqzbwuegt9b2830vw")
    eq_(revision.slots['main'].text, "Text of rev 233192")
    eq_(revision.slots['main'].format, "text/x-wiki")
    eq_(revision.slots['label_data'].role, "label_data")
    eq_(revision.slots['label_data'].origin, 123)
    eq_(revision.slots['label_data'].model, "JadeEntity")
    eq_(revision.slots['label_data'].format, "text/json")
    eq_(revision.slots['label_data'].id, "1234")
    eq_(revision.slots['label_data'].deleted, True)
    eq_(revision.slots['label_data'].location, "file://dev/null")
    eq_(revision.slots['label_data'].bytes, 234)
    eq_(revision.slots['label_data'].sha1, "ahgsvdjasvbdj3723")
