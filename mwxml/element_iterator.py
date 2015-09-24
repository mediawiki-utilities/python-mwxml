import io
from xml.etree.ElementTree import ParseError

from .errors import MalformedXML

try:
    import xml.etree.cElementTree as etree
except ImportError:
    import xml.etree.ElementTree as etree


def trim_ns(tag):
    return tag[tag.find("}") + 1:]


class EventPointer:
    def __init__(self, etree_events):
        self.tag_stack = []
        self.etree_events = etree_events

    def __next__(self):
        event, element = next(self.etree_events)

        tag = trim_ns(element.tag)

        if event == "start":
            self.tag_stack.append(tag)
        else:
            if self.tag_stack[-1] == tag:
                self.tag_stack.pop()
            else:
                raise MalformedXML("Expected {0}, but saw {1}.".format(
                    self.tag_stack[-1],
                    tag)
                )

        return event, element

    def depth(self):
        return len(self.tag_stack)

    @classmethod
    def from_file(cls, f):
        return EventPointer(etree.iterparse(f, events=("start", "end")))


class ElementIterator:
    def __init__(self, element, pointer):
        self.pointer = pointer
        self.element = element
        self.depth = pointer.depth() - 1

        self.done = False

    def __iter__(self):

        while not self.done and self.pointer.depth() > self.depth:
            event, element = next(self.pointer)

            if event == "start":
                sub_iterator = ElementIterator(element, self.pointer)

                yield sub_iterator

                sub_iterator.clear()

        self.done = True

    def complete(self):

        while not self.done and self.pointer.depth() > self.depth:
            event, element = next(self.pointer)
            if self.pointer.depth() > self.depth:
                element.clear()

        self.done = True

    def clear(self):
        self.complete()
        self.element.clear()

    def attr(self, key, alt=None):
        return self.element.attrib.get(key, alt)

    def __getattr__(self, attr):
        if attr == "tag":
            return trim_ns(self.element.tag)
        elif attr == "text":
            self.complete()
            return self.element.text
        else:
            raise AttributeError("{0} has no attribute {1}"
                                 .format(self.__class__.__name__, attr))

    @classmethod
    def from_file(cls, f):

        try:
            pointer = EventPointer.from_file(f)
            event, element = next(pointer)
            return cls(element, pointer)
        except ParseError as e:
            raise ParseError("{0}: {1}..."
                             .format(str(e),
                                     f.read(500)))

    @classmethod
    def from_string(cls, string):
        f = io.StringIO(string)

        return cls.from_file(f)
