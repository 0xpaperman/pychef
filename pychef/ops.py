import base64
import re
import string
from itertools import cycle


def _to_key(key: bytes | str | int) -> bytes:
    # Accept 0x13, "secret" or b"\x13" as a key
    if isinstance(key, int):
        return key.to_bytes(max(1, (key.bit_length() + 7) // 8), "big")
    if isinstance(key, str):
        return key.encode()
    return bytes(key)


def xor(data: bytes, key: bytes | str | int) -> bytes:
    # Pairs bytes with zip and repeats the key as needed
    return bytes(b1 ^ b2 for b1, b2 in zip(data, cycle(_to_key(key))))


def to_base64(data: bytes) -> bytes:
    return base64.b64encode(data)


def from_base64(data: bytes) -> bytes:
    return base64.b64decode(data)


def clean(data: bytes) -> bytes:
    # Removes all whitespace
    return b"".join(data.split())


_HEX_PREFIX = re.compile(rb"0x|\\x", re.IGNORECASE)
_SEPARATORS = re.compile(rb"[\s,:;-]+")
_HEX_TOKEN = re.compile(rb"[0-9a-fA-F]+")


def from_hex(data: bytes) -> bytes:
    # Turn 0x / \x prefixes into separators, then parse each token
    data = _HEX_PREFIX.sub(b" ", data)
    out = bytearray()
    for token in _SEPARATORS.split(data):
        if not token:
            continue
        if not _HEX_TOKEN.fullmatch(token):
            raise ValueError(f"not valid hex: {token!r}")
        if len(token) % 2:  # "0xa" -> "0a"
            token = b"0" + token
        out += bytes.fromhex(token.decode())
    return bytes(out)


def to_hex(data: bytes) -> bytes:
    return data.hex().encode()


def u_shift(data: bytes, charset: str = string.ascii_letters, keep: str = string.whitespace) -> bytes:
    # Map each unique symbol to a letter from charset, in order of first appearance.
    # Characters in `keep` (whitespace by default) are left as they are.
    text = data.decode()
    symbols = [c for c in dict.fromkeys(text) if c not in keep]
    if len(symbols) > len(charset):
        raise ValueError(f"Not enough chars in charset to represent {len(symbols)} unique symbols")
    table = str.maketrans(dict(zip(symbols, charset)))
    return text.translate(table).encode()
