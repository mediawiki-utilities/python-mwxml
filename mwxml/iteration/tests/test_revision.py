import mwtypes
from nose.tools import eq_

from ...element_iterator import ElementIterator
from ..revision import Revision


def test_revision():
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
