"""
Test suite for StopIteration bug fix (PEP 479 compatibility).

This module tests that the mwxml library properly handles StopIteration
exceptions in Python 3.7+ where PEP 479 converts StopIteration raised
inside generators to RuntimeError.
"""

import io
import pytest
import sys

from ..dump import Dump


# Sample XML with valid MediaWiki structure
MINIMAL_XML = """
<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/">
  <siteinfo>
    <sitename>Wikipedia</sitename>
    <dbname>enwiki</dbname>
  </siteinfo>
  <page>
    <title>Test Page</title>
    <ns>0</ns>
    <id>1</id>
    <revision>
      <id>100</id>
      <timestamp>2021-01-01T00:00:00Z</timestamp>
      <text>Test content</text>
    </revision>
  </page>
</mediawiki>
"""

MULTI_PAGE_XML = """
<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/">
  <siteinfo>
    <sitename>Wikipedia</sitename>
    <dbname>enwiki</dbname>
  </siteinfo>
  <page>
    <title>Page 1</title>
    <ns>0</ns>
    <id>1</id>
    <revision>
      <id>100</id>
      <timestamp>2021-01-01T00:00:00Z</timestamp>
      <text>Content 1</text>
    </revision>
  </page>
  <page>
    <title>Page 2</title>
    <ns>0</ns>
    <id>2</id>
    <revision>
      <id>200</id>
      <timestamp>2021-01-02T00:00:00Z</timestamp>
      <text>Content 2</text>
    </revision>
  </page>
</mediawiki>
"""


@pytest.mark.skipif(sys.version_info < (3, 7), 
                    reason="Bug only affects Python 3.7+")
def test_stopiteration_bug_reproduction():
    """
    Reproduce the StopIteration RuntimeError bug in Python 3.7+.
    
    This test demonstrates the bug that occurs when the XML stream is
    exhausted and StopIteration propagates through a generator, which
    PEP 479 converts to RuntimeError.
    
    NOTE: This test is expected to FAIL before the fix is applied and
    PASS after the fix is applied.
    """
    dump = Dump.from_file(io.StringIO(MINIMAL_XML))
    
    # Before the fix, this should raise RuntimeError in Python 3.7+
    # After the fix, this should complete normally
    try:
        pages = list(dump)
        # If we get here, the fix is working
        assert len(pages) == 1
        assert pages[0].title == "Test Page"
    except RuntimeError as e:
        if "generator raised StopIteration" in str(e):
            pytest.fail(
                "Bug reproduced: RuntimeError raised due to StopIteration in generator. "
                "The fix has not been applied yet."
            )
        else:
            # Some other RuntimeError, re-raise it
            raise


def test_iteration_completes_normally():
    """
    Verify iteration completes without RuntimeError after fix.
    
    This test verifies that the fix properly handles stream exhaustion
    and allows iteration to complete normally.
    """
    dump = Dump.from_file(io.StringIO(MINIMAL_XML))
    
    # Should complete without raising RuntimeError
    pages = list(dump)
    
    # Verify the page was extracted
    assert len(pages) == 1
    assert pages[0].title == "Test Page"
    assert pages[0].id == 1
    assert pages[0].namespace == 0


def test_multiple_pages_iteration():
    """
    Verify iteration works correctly with multiple pages.
    
    Tests that the fix doesn't break normal iteration over multiple
    pages in the XML dump.
    """
    dump = Dump.from_file(io.StringIO(MULTI_PAGE_XML))
    
    # Should complete without raising RuntimeError
    pages = list(dump)
    
    # Verify all pages were extracted
    assert len(pages) == 2
    assert pages[0].title == "Page 1"
    assert pages[0].id == 1
    assert pages[1].title == "Page 2"
    assert pages[1].id == 2


def test_iteration_with_generator_pattern():
    """
    Verify the fix works with generator iteration pattern.
    
    This tests that the fix works when using the dump as a generator
    rather than converting to a list.
    """
    dump = Dump.from_file(io.StringIO(MULTI_PAGE_XML))
    
    # Iterate using generator pattern
    page_titles = []
    for page in dump:
        page_titles.append(page.title)
    
    # Should have collected all pages
    assert page_titles == ["Page 1", "Page 2"]


def test_empty_dump_iteration():
    """
    Verify iteration handles empty dumps correctly.
    
    Tests edge case where there are no pages in the dump.
    """
    empty_xml = """
    <mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/">
      <siteinfo>
        <sitename>Wikipedia</sitename>
        <dbname>enwiki</dbname>
      </siteinfo>
    </mediawiki>
    """
    
    dump = Dump.from_file(io.StringIO(empty_xml))
    
    # Should complete without error
    pages = list(dump)
    
    # Should have no pages
    assert len(pages) == 0


def test_partial_iteration():
    """
    Verify partial iteration doesn't cause issues.
    
    Tests that breaking out of iteration early doesn't cause problems
    with the StopIteration handling.
    """
    dump = Dump.from_file(io.StringIO(MULTI_PAGE_XML))
    
    # Only iterate over first page
    first_page = None
    for page in dump:
        first_page = page
        break
    
    # Should have gotten the first page
    assert first_page is not None
    assert first_page.title == "Page 1"


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
