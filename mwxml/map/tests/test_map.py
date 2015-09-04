import io

from nose.tools import eq_, raises

from ..map import map


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
    <title>Foo:Bar</title>
    <ns>1</ns>
    <id>2</id>
    <revision>
      <id>3</id>
      <timestamp>2004-08-11T09:04:08Z</timestamp>
    </revision>
  </page>
</mediawiki>"""


def test_map():
    f = io.StringIO(SAMPLE_XML)

    def process_dump(dump, path):
        for page in dump:
            revisions = sum(1 for rev in page)
            yield {'page_id': page.id, 'revisions': revisions}

    pages = 0
    for doc in map(process_dump, [f]):
        page_id = doc['page_id']
        revisions = doc['revisions']
        if page_id == 1:
            eq_(revisions, 2)
        elif page_id == 2:
            eq_(revisions, 1)
        else:
            assert False

        pages += 1

    eq_(pages, 2)


@raises(TypeError)
def test_map_error():
    f = io.StringIO(SAMPLE_XML)

    def process_dump(dump, path):
        for page in dump:

            if page.id == 2:
                raise TypeError("Fake error")

    for doc in map([f], process_dump):
        assert 'page_id' in doc


def test_map_error_handler():
    f = io.StringIO(SAMPLE_XML)

    def process_dump(dump, path):
        for page in dump:
            count = 0

            for rev in page:
                count += 1

            if count > 2:
                raise TypeError("Fake type error.")

            yield {'page_id': page.id, 'revisions': count}

    pages = 0
    for doc in map(process_dump, [f]):
        page_id = doc['page_id']
        revisions = doc['revisions']
        if page_id == 1:
            eq_(revisions, 2)
        elif page_id == 2:
            eq_(revisions, 1)
        else:
            assert False

        pages += 1

    eq_(pages, 2)


@raises(ValueError)
def test_complex_error_handler():
    f_clean = io.StringIO("""
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
        </mediawiki>
    """)
    f_messy = io.StringIO("""
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
            <title>Bar</title>
            <ns>0</ns>
            <id>2</id>
            <revision>
              <id>3</id>
              <timestamp>MESSY</timestamp>
            </revision>
            <revision>
              <id>4</id>
              <timestamp>2004-08-10T09:04:08Z</timestamp>
            </revision>
          </page>
        </mediawiki>
    """)

    def process_dump(dump, path):
        for page in dump:
            for revision in page:
                yield revision

    for rev in map(process_dump, [f_messy, f_clean], threads=1):
        print(rev.to_json())
