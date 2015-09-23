from nose.tools import eq_

from ...element_iterator import ElementIterator
from ..namespace import Namespace
from ..page import Page


def test_page():
    XML = """
    <page>
        <title>AccessibleComputing</title>
        <ns>0</ns>
        <id>10</id>
        <redirect title="Computer accessibility" />
        <revision>
          <id>233192</id>
          <timestamp>2001-01-21T02:12:21Z</timestamp>
          <contributor>
            <username>RoseParks</username>
            <id>99</id>
          </contributor>
          <comment>*</comment>
          <model>wikitext</model>
          <format>text/x-wiki</format>
          <text xml:space="preserve">Text of rev 233192</text>
          <sha1>8kul9tlwjm9oxgvqzbwuegt9b2830vw</sha1>
        </revision>
        <revision>
          <id>862220</id>
          <parentid>233192</parentid>
          <timestamp>2002-02-25T15:43:11Z</timestamp>
          <contributor>
            <username>Conversion script</username>
            <id>0</id>
          </contributor>
          <minor />
          <comment>Automated conversion</comment>
          <model>wikitext</model>
          <format>text/x-wiki</format>
          <text xml:space="preserve">Text of rev 862220</text>
          <sha1>i8pwco22fwt12yp12x29wc065ded2bh</sha1>
        </revision>
    </page>
    """
    page = Page.from_element(ElementIterator.from_string(XML))
    eq_(page.id, 10)
    eq_(page.title, "AccessibleComputing")
    eq_(page.namespace, 0)
    eq_(page.redirect, "Computer accessibility")
    eq_(page.restrictions, [])  # Should be known to be empty

    revision = next(page)
    eq_(revision.id, 233192)
    eq_(revision.page, page)

    revision = next(page)
    eq_(revision.id, 862220)

def test_old_page():
    XML = """
    <page>
        <title>Talk:AccessibleComputing</title>
        <id>10</id>
        <redirect title="Computer accessibility" />
        <revision>
          <id>233192</id>
          <timestamp>2001-01-21T02:12:21Z</timestamp>
          <contributor>
            <username>RoseParks</username>
            <id>99</id>
          </contributor>
          <comment>*</comment>
          <model>wikitext</model>
          <format>text/x-wiki</format>
          <text xml:space="preserve">Text of rev 233192</text>
          <sha1>8kul9tlwjm9oxgvqzbwuegt9b2830vw</sha1>
        </revision>
    </page>
    """
    page = Page.from_element(ElementIterator.from_string(XML),
                             {"Talk": Namespace(1, "Talk")})
    eq_(page.namespace, 1)
