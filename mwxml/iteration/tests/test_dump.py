import io

import mwtypes
from nose.tools import assert_is_instance, eq_

from ..dump import Dump
from ..page import Page
from ..revision import Revision


SAMPLE_XML = """
<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.8/"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.8/
                               http://www.mediawiki.org/xml/export-0.8.xsd"
           version="0.8" xml:lang="en">
  <siteinfo>
    <sitename>Wikipedia</sitename>
    <base>http://en.wikipedia.org/wiki/Main_Page</base>
    <generator>MediaWiki 1.22wmf2</generator>
    <case>first-letter</case>
    <namespaces>
      <namespace key="0" case="first-letter" />
      <namespace key="1" case="first-letter">Talk</namespace>
    </namespaces>
  </siteinfo>
  <page>
    <title>Foo</title>
    <ns>0</ns>
    <id>1</id>
    <revision>
      <id>1</id>
      <timestamp>2004-08-09T09:04:08Z</timestamp>
    </revision>
    <revision>
      <id>2</id>
      <timestamp>2004-08-10T09:04:08Z</timestamp>
    </revision>
  </page>
  <page>
    <title>Talk:Bar</title>
    <ns>1</ns>
    <id>2</id>
    <redirect title="Computer accessibility" />
    <restrictions>edit=sysop:move=sysop</restrictions>
    <revision>
      <id>3</id>
      <timestamp>2004-08-11T09:04:08Z</timestamp>
    </revision>
    <revision>
      <id>4</id>
      <timestamp>2004-08-12T09:04:08Z</timestamp>
    </revision>
  </page>
</mediawiki>"""


def test_complete():
    f = io.StringIO(SAMPLE_XML)

    dump = Dump.from_file(f)
    eq_([0, 1], list(ns.id for ns in dump.site_info.namespaces))

    page = next(dump)
    eq_(page.title, "Foo")
    eq_(page.namespace, 0)
    eq_(page.id, 1)
    eq_(page.redirect, None)
    eq_(page.restrictions, [])

    revision = next(page)
    eq_(revision.id, 1)
    eq_(revision.timestamp, mwtypes.Timestamp("2004-08-09T09:04:08Z"))

    revision = next(page)
    eq_(revision.id, 2)
    eq_(revision.timestamp, mwtypes.Timestamp("2004-08-10T09:04:08Z"))

    page = next(dump)
    assert_is_instance(page, Page)
    eq_(page.title, "Bar")
    eq_(page.namespace, 1)
    eq_(page.id, 2)
    eq_(page.redirect, "Computer accessibility")
    eq_(page.restrictions, ["edit=sysop:move=sysop"])

    revision = next(page)
    assert_is_instance(revision, Revision)
    eq_(revision.id, 3)
    eq_(revision.timestamp, mwtypes.Timestamp("2004-08-11T09:04:08Z"))

    revision = next(page)
    assert_is_instance(revision, Revision)
    eq_(revision.id, 4)
    eq_(revision.timestamp, mwtypes.Timestamp("2004-08-12T09:04:08Z"))


def test_skipping():
    f = io.StringIO(SAMPLE_XML)

    dump = Dump.from_file(f)

    page = next(dump)
    eq_(page.title, "Foo")
    eq_(page.namespace, 0)
    eq_(page.id, 1)

    page = next(dump)
    eq_(page.title, "Bar")
    eq_(page.namespace, 1)
    eq_(page.id, 2)

    revision = next(page)
    eq_(revision.id, 3)
    eq_(revision.timestamp, mwtypes.Timestamp("2004-08-11T09:04:08Z"))


def test_from_page_xml():
    page_xml = """
    <page>
      <title>Foo</title>
      <ns>0</ns>
      <id>1</id>
      <revision>
        <id>1</id>
        <timestamp>2004-08-09T09:04:08Z</timestamp>
      </revision>
      <revision>
        <id>2</id>
        <timestamp>2004-08-10T09:04:08Z</timestamp>
      </revision>
    </page>
    """

    dump = Dump.from_page_xml(io.StringIO(page_xml))

    # You have a `namespaces`, but it's empty.
    eq_(dump.site_info.namespaces, None)

    page = next(dump)
    eq_(page.title, "Foo")
    eq_(page.namespace, 0)
    eq_(page.id, 1)

    revision = next(page)
    eq_(revision.id, 1)
    eq_(revision.timestamp, mwtypes.Timestamp("2004-08-09T09:04:08Z"))

    revision = next(page)
    eq_(revision.id, 2)
    eq_(revision.timestamp, mwtypes.Timestamp("2004-08-10T09:04:08Z"))


OLD_XML = """
<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.8/"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.8/
                               http://www.mediawiki.org/xml/export-0.8.xsd"
           version="0.8" xml:lang="en">
  <siteinfo>
    <sitename>Wikipedia</sitename>
    <base>http://en.wikipedia.org/wiki/Main_Page</base>
    <generator>MediaWiki 1.22wmf2</generator>
    <case>first-letter</case>
    <namespaces>
      <namespace key="0" case="first-letter" />
      <namespace key="1" case="first-letter">Talk</namespace>
    </namespaces>
  </siteinfo>
  <page>
    <title>Talk:Foo</title>
    <id>1</id>
    <revision>
      <id>1</id>
      <timestamp>2004-08-09T09:04:08Z</timestamp>
    </revision>
    <revision>
      <id>2</id>
      <timestamp>2004-08-10T09:04:08Z</timestamp>
    </revision>
  </page>
</mediawiki>"""


def test_old_dump():
    f = io.StringIO(OLD_XML)

    dump = Dump.from_file(f)

    page = next(dump)

    eq_(page.namespace, 1)


LOG_XML = """
<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.8/"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.8/
                               http://www.mediawiki.org/xml/export-0.8.xsd"
           version="0.8" xml:lang="en">
  <siteinfo>
    <sitename>Wikipedia</sitename>
    <base>http://en.wikipedia.org/wiki/Main_Page</base>
    <generator>MediaWiki 1.22wmf2</generator>
    <case>first-letter</case>
    <namespaces>
      <namespace key="0" case="first-letter" />
      <namespace key="1" case="first-letter">Talk</namespace>
    </namespaces>
  </siteinfo>
  <logitem>
    <id>1</id>
    <timestamp>2004-12-23T03:20:32Z</timestamp>
    <contributor>
      <username>Slowking Man</username>
      <id>56299</id>
    </contributor>
    <comment>content was: '[[Media:Example.og[http://www.example.com link title][http://www.example.com link title]''Italic text'''''Bold text'''jjhkjhkjhkjhkjhjggghg]]'</comment>
    <type>delete</type>
    <action>delete</action>
    <logtitle>Vivian Blaine</logtitle>
    <params xml:space="preserve" />
  </logitem>
  <logitem>
    <id>2</id>
    <timestamp>2004-12-23T03:24:26Z</timestamp>
    <contributor>
      <username>Fredrik</username>
      <id>26675</id>
    </contributor>
    <comment>{{GFDL}} {{cc-by-sa-2.0}}</comment>
    <type>upload</type>
    <action>upload</action>
    <logtitle>File:Mini Christmas tree.png</logtitle>
    <params xml:space="preserve" />
  </logitem>
</mediawiki>"""  # noqa


def test_log_dump():
    f = io.StringIO(LOG_XML)

    dump = Dump.from_file(f)

    log_item = next(dump)
    eq_(log_item.id, 1)

    log_item = next(dump)
    eq_(log_item.id, 2)
