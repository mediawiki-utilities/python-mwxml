import io

from nose.tools import eq_
from ..element_iterator import EventPointer, ElementIterator


TEST_XML = """
<foo>
    <bar>
        <herp>content</herp>
    </bar>
    <derp foo="bar"></derp>
</foo>
"""


def test_pointer():
    pointer = EventPointer.from_file(io.StringIO(TEST_XML))

    eq_(pointer.tag_stack, [])
    eq_(pointer.depth(), 0)

    event, element = next(pointer)
    eq_(pointer.tag_stack, ["foo"])
    eq_(pointer.depth(), 1)
    eq_(element.tag, "foo")
    eq_(event, "start")

    event, element = next(pointer)
    eq_(pointer.tag_stack, ["foo", "bar"])
    eq_(pointer.depth(), 2)
    eq_(element.tag, "bar")
    eq_(event, "start")

    event, element = next(pointer)
    eq_(pointer.tag_stack, ["foo", "bar", "herp"])
    eq_(pointer.depth(), 3)
    eq_(element.tag, "herp")
    eq_(event, "start")

    event, element = next(pointer)
    eq_(pointer.tag_stack, ["foo", "bar"])
    eq_(pointer.depth(), 2)
    eq_(element.tag, "herp")
    eq_(event, "end")

    event, element = next(pointer)
    eq_(pointer.tag_stack, ["foo"])
    eq_(pointer.depth(), 1)
    eq_(element.tag, "bar")
    eq_(event, "end")

    event, element = next(pointer)
    eq_(pointer.tag_stack, ["foo", "derp"])
    eq_(pointer.depth(), 2)
    eq_(element.tag, "derp")
    eq_(event, "start")

    event, element = next(pointer)
    eq_(pointer.tag_stack, ["foo"])
    eq_(pointer.depth(), 1)
    eq_(element.tag, "derp")
    eq_(event, "end")

    event, element = next(pointer)
    eq_(pointer.tag_stack, [])
    eq_(pointer.depth(), 0)
    eq_(element.tag, "foo")
    eq_(event, "end")

    try:
        event, element = next(pointer)
    except StopIteration:
        return True

    assert False, "Iteration did not stop as expected."


def test_iterator():
    foo_element = ElementIterator.from_file(io.StringIO(TEST_XML))
    foo_iterator = iter(foo_element)

    bar_element = next(foo_iterator)
    bar_iterator = iter(bar_element)
    eq_(bar_element.tag, "bar")

    herp_element = next(bar_iterator)
    eq_(herp_element.tag, "herp")
    eq_(herp_element.text, "content")

    derp_element = next(foo_iterator)
    eq_(derp_element.tag, "derp")
    eq_(derp_element.attr("foo"), "bar")


def test_skipping_iterator():
    foo_element = ElementIterator.from_file(io.StringIO(TEST_XML))
    foo_iterator = iter(foo_element)

    bar_element = next(foo_iterator)

    derp_element = next(foo_iterator)
    eq_(derp_element.tag, "derp")
    eq_(derp_element.attr("foo"), "bar")
