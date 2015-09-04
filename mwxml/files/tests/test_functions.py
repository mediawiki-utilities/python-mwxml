import io
import os

from nose.tools import eq_, raises

from ...errors import FileTypeError
from ..functions import concat, extract_extension, normalize_path, open


def test_concat():
    start = "Foobar1"
    f = io.StringIO("Foobar2")
    end = "Foobar3"

    eq_(concat(start, f, end).read(), "Foobar1Foobar2Foobar3")


def test_extract_extension():
    eq_(extract_extension("foo"), None)
    eq_(extract_extension("foo.xml"), "xml")
    eq_(extract_extension("foo.xml.gz"), "gz")
    eq_(extract_extension("foo.xml.bz2"), "bz2")
    eq_(extract_extension("foo.xml-p10001p10200.7z"), "7z")


@raises(FileNotFoundError)
def test_normalize_path_noexist():
    normalize_path("IDONTEXIST!!!")


@raises(IsADirectoryError)
def test_normalize_path_directory():
    normalize_path(os.path.dirname(__file__))


@raises(FileTypeError)
def test_normalize_path_bad_extension():
    normalize_path(__file__)


def test_open():
    f = io.StringIO()
    eq_(f, open(f))
