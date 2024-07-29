from mwtypes import Timestamp
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
    assert log_item.id == 6
    assert log_item.timestamp == Timestamp("2004-12-23T03:34:26Z")
    assert (log_item.comment ==
        "content was: '#redirect [[Template:UserBrockert]]', an old " +
        "experiment of mine, now being moved around by bots")
    assert log_item.user.id == 50095
    assert log_item.user.text == "Brockert"
    assert log_item.page.namespace == 10
    assert log_item.page.title == "UserBrockert"
    assert log_item.type == "delete"
    assert log_item.action == "delete"
    assert log_item.params == None
    assert log_item.deleted.action == None
    assert log_item.deleted.user == False
    assert log_item.deleted.comment == False
    assert log_item.deleted.restricted == None

    NULL_TITLE_XML = """
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
        <logtitle />
        <params xml:space="preserve" />
    </logitem>
    """  # noqa
    log_item = LogItem.from_element(
        ElementIterator.from_string(NULL_TITLE_XML))
    assert log_item.page.namespace == None
    assert log_item.page.title == None
