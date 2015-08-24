import os.path

from nose.tools import eq_, raises

from .. import p7z
from ..functions import normalize_path


def test_open_file_7z():
    path = os.path.join(os.path.dirname(__file__), "test.7z")
    print(path)
    f = p7z.open(normalize_path(path)[0])
    eq_(f.read(), b"foobartest\n")
