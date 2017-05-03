from mwtypes import Timestamp
from nose.tools import eq_

from ...element_iterator import ElementIterator
from ..log_item import LogItem
from ..namespace import Namespace


def test_log_item():
    XML = """
    <logitem>
        <id>6</id>
        <timestamp>2004-12-23T03:34:26Z</timestamp>
        <contributor>
            <username>Brockert</username>
            <id>50095</id>
        </contributor>
        <comment>content was: '#redirect [[Template:UserBrockert]]', an old experiment of mine, now being moved around by bots</comment>
        <type>delete</type>
        <action>delete</action>
        <logtitle>Template:UserBrockert</logtitle>
        <params xml:space="preserve" />
    </logitem>
    """  # noqa
    namespace_map = {
        "Template": Namespace(10, "Template")}
    log_item = LogItem.from_element(
        ElementIterator.from_string(XML), namespace_map)
    eq_(log_item.id, 6)
    eq_(log_item.timestamp, Timestamp("2004-12-23T03:34:26Z"))
    eq_(log_item.comment,
        "content was: '#redirect [[Template:UserBrockert]]', an old " +
        "experiment of mine, now being moved around by bots")
    eq_(log_item.user.id, 50095)
    eq_(log_item.user.text, "Brockert")
    eq_(log_item.page.namespace, 10)
    eq_(log_item.page.title, "UserBrockert")
    eq_(log_item.type, "delete")
    eq_(log_item.action, "delete")
    eq_(log_item.params, None)
    eq_(log_item.deleted.action, None)
    eq_(log_item.deleted.user, False)
    eq_(log_item.deleted.comment, False)
    eq_(log_item.deleted.restricted, None)
