import sys
from xml.etree import ElementTree

from more_itertools import peekable


def strip_tag(tag):
    return tag.split("}")[1]

class Dump:
    __slots__ = ('siteinfo', 'pages')

    def __init__(self, siteinfo=None, pages=None):
        self.siteinfo = siteinfo

        if pages is None:
            self.pages = range(0)
        else:
            self.pages = pages

    def iter(self):
        return self.pages

    @classmethod
    def from_events(cls, events):
        event, elem = next(events)
        assert event == "start" and strip_tag(elem.tag) == "mediawiki"


        kwargs = {}
        while events:
            event, elem = events.peek()

            # Inner loop stuff
            if event == "start" and strip_tag(elem.tag) == "siteinfo":
                kwargs['siteinfo'] = SiteInfo.from_events(events)
            elif event == "end" and strip_tag(elem.tag) == "siteinfo":
                #kwargs['pages'] = Page.read_from(events)
                next(event)
                break
            else:
                next(event)

        return cls(**kwargs)

    @classmethod
    def from_file(cls, f):
        events = ElementTree.iterparse(f, events=('start', 'end'));

        return cls.from_events(peekable(events))



class SiteInfo:
    __slots__ = ('sitename', 'dbname', 'base', 'generator', 'case',
                 'namespaces')

    def __init__(self, sitename=None, dbname=None, base=None, generator=None,
                       case=None, namespaces=None):
        self.sitename = str(sitename) if sitename is not None else None
        self.base = str(base) if base is not None else None
        self.dbname = str(dbname) if dbname is not None else None
        self.generator = str(generator) if generator is not None else None
        self.case = str(case) if case is not None else None
        self.namespaces = namespaces

    @classmethod
    def from_events(cls, events):
        event, elem = next(events)
        assert event == "start" and strip_tag(elem.tag) == "siteinfo"

        kwargs = {}
        while events:
            event, elem = events.peek()

            if event == "end":
                if strip_tag(elem.tag) == "sitename":
                    kwargs['sitename'] = elem.text
                elif strip_tag(elem.tag) == "dbname":
                    kwargs['dbname'] = elem.text
                elif strip_tag(elem.tag) == "base":
                    kwargs['base'] = elem.text
                elif strip_tag(elem.tag) == "generator":
                    kwargs['generator'] = elem.text
                elif strip_tag(elem.tag) == "case":
                    kwargs['case'] = elem.text

                next(events)

            elif event == "start" and strip_tag(elem.tag) == "namespaces":
                kwargs['namespaces'] = Namespaces.from_events(events)

            elif event == "end" and strip_tag(elem.tag) == "siteinfo":
                next(events)
                break
            else:
                next(events)

        return cls(**kwargs)




class Namespaces(list):

    def init(self, namespaces):
        super().__init__(namespace)

    @classmethod
    def from_events(cls, events):
        event, elem = next(events)
        assert event == "start" and strip_tag(elem.tag) == "namespaces"

        namespaces = cls()
        while events:
            event, elem = events.peek()

            # Inner tag stuff
            if event == "start" and strip_tag(elem.tag) == "namespace":
                namespaces.append(Namespace.from_events(events))
            elif event == "end" and strip_tag(elem.tag) == "namespaces":
                next(events)
                break
            else:
                next(events)

        return namespaces


class Namespace:
    __slots__ = ('key', 'case', 'text')

    def __init__(self, key=None, case=None, text=None):
        self.key = int(key) if key is not None else None
        self.case = str(case) if case is not None else None
        self.text = str(text) if text is not None else None

    @classmethod
    def from_events(cls, events):
        event, elem = next(events)
        assert event == "start" and strip_tag(elem.tag) == "namespace"

        event, elem = next(events)
        assert event == "end" and strip_tag(elem.tag) == "namespace"

        return cls(
            elem.attrib.get('key'),
            elem.attrib.get('case'),
            elem.text
        )

dump = Dump.from_file(sys.stdin)
for ns in dump.siteinfo.namespaces:
    print(ns.key)
