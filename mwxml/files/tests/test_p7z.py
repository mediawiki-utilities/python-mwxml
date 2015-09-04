import os.path

from nose.tools import eq_

from .. import p7z
from ..functions import normalize_path


def test_open_file_7z():
    path = os.path.join(os.path.dirname(__file__), "test.7z")
    f = p7z.open(normalize_path(path))
    eq_(f.read(), b"foobartest\n")
