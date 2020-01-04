from msg_types import *
from pytest import raises


def test_type_is_default():
    # create int
    echo_int = MsgType("int")
    assert echo_int.size_in_bytes(5) == 4


def test_type_is_string():
    # create string
    echo_string = MsgType("string")
    assert echo_string.size_in_bytes("hello") == 5


def test_type_is_wrong():
    # create undefined msg_type
    with raises(AttributeError):
        MsgType("undef")
