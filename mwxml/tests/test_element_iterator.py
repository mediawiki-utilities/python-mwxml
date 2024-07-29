import io

from ..element_iterator import ElementIterator, EventPointer


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

    assert pointer.tag_stack == []
    assert pointer.depth() == 0

    event, element = next(pointer)
    assert pointer.tag_stack == ["foo"]
    assert pointer.depth() == 1
    assert element.tag == "foo"
    assert event == "start"

    event, element = next(pointer)
    assert pointer.tag_stack == ["foo", "bar"]
    assert pointer.depth() == 2
    assert element.tag == "bar"
    assert event == "start"

    event, element = next(pointer)
    assert pointer.tag_stack == ["foo", "bar", "herp"]
    assert pointer.depth() == 3
    assert element.tag == "herp"
    assert event == "start"

    event, element = next(pointer)
    assert pointer.tag_stack == ["foo", "bar"]
    assert pointer.depth() == 2
    assert element.tag == "herp"
    assert event == "end"

    event, element = next(pointer)
    assert pointer.tag_stack == ["foo"]
    assert pointer.depth() == 1
    assert element.tag == "bar"
    assert event == "end"

    event, element = next(pointer)
    assert pointer.tag_stack == ["foo", "derp"]
    assert pointer.depth() == 2
    assert element.tag == "derp"
    assert event == "start"

    event, element = next(pointer)
    assert pointer.tag_stack == ["foo"]
    assert pointer.depth() == 1
    assert element.tag == "derp"
    assert event == "end"

    event, element = next(pointer)
    assert pointer.tag_stack == []
    assert pointer.depth() == 0
    assert element.tag == "foo"
    assert event == "end"

    try:
        event, element = next(pointer)
    except StopIteration:
        return None

    assert False, "Iteration did not stop as expected."


def test_iterator():
    foo_element = ElementIterator.from_file(io.StringIO(TEST_XML))
    foo_iterator = iter(foo_element)

    bar_element = next(foo_iterator)
    bar_iterator = iter(bar_element)
    assert bar_element.tag == "bar"

    herp_element = next(bar_iterator)
    assert herp_element.tag == "herp"
    assert herp_element.text == "content"

    derp_element = next(foo_iterator)
    assert derp_element.tag == "derp"
    assert derp_element.attr("foo") == "bar"


def test_skipping_iterator():
    foo_element = ElementIterator.from_file(io.StringIO(TEST_XML))
    foo_iterator = iter(foo_element)

    next(foo_iterator)

    derp_element = next(foo_iterator)
    assert derp_element.tag == "derp"
    assert derp_element.attr("foo") == "bar"
