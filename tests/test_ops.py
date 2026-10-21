import pytest

from pychef import Chef, ops


@pytest.mark.parametrize("text", [
    b"abab", b"0xabab", b"0x abab", b"ab ab", b"AB:AB",
    b"0xab, 0xab", b"\\xab\\xab", b"0XABAB", b"ab-ab\n",
])
def test_from_hex_formats(text):
    assert ops.from_hex(text) == b"\xab\xab"


def test_from_hex_odd_token_is_padded():
    assert ops.from_hex(b"0xa 0xb") == b"\x0a\x0b"


def test_from_hex_rejects_garbage():
    with pytest.raises(ValueError):
        ops.from_hex(b"hello")


def test_to_hex():
    assert ops.to_hex(b"\xab\x01") == b"ab01"


def test_base64_roundtrip():
    assert ops.to_base64(b"hello") == b"aGVsbG8="
    assert ops.from_base64(b"aGVsbG8=") == b"hello"


@pytest.mark.parametrize("key", [b"!$(#&#!!)&", "!$(#&#!!)&"])
def test_xor_bytes_and_str_keys(key):
    assert ops.xor(b"JtysDOQnNk", key) == b"kPQPblpOgM"


def test_xor_int_keys():
    assert ops.xor(b"AB", 0x13) == b"RQ"
    assert ops.xor(b"AB", 0x1337) == bytes([0x41 ^ 0x13, 0x42 ^ 0x37])


def test_clean():
    assert ops.clean(b" a b\n\tc ") == b"abc"


def test_u_shift():
    assert ops.u_shift("🔥🌊 🌊🔥🔥 é".encode()) == b"ab baa c"
    assert ops.u_shift("éa".encode()) == b"ab"


def test_u_shift_charset_too_small():
    with pytest.raises(ValueError):
        ops.u_shift(b"abc", charset="xy")


def test_chain():
    assert Chef("0x41 0x42 0x43").from_hex().xor(0x13).to_base64().o == b"UlFQ"


def test_chef_argument_is_unwrapped():
    a = Chef("4142").from_hex()
    b = Chef("1313").from_hex()
    assert a.xor(b).o == a.xor(b.o).o == a.xor(key=b).o == b"RQ"


def test_branching_does_not_mutate():
    d = Chef("4142").from_hex()
    d.xor(0x01)
    assert d.o == b"AB"


def test_output_helpers():
    c = Chef("hi")
    assert bytes(c) == b"hi"
    assert str(c) == "hi"
    assert repr(c) == "Chef(b'hi')"
