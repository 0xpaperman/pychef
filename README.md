# pychef

CyberChef-style chainable byte operations for Python.

```python
from pychef import Chef

Chef("0x41 0x42 0x43").from_hex().xor(0x13).to_base64()   # Chef(b'UlFQ')
```

## Install

```
pip install git+https://github.com/YOURNAME/pychef
```

For development, clone the repo and run `pip install -e ".[dev]"` so edits take effect immediately.

## Usage

Every operation returns a new `Chef`, so you can chain them and branch from any point:

```python
from pychef import Chef

b1 = Chef("6a63...").from_hex()
b2 = Chef("1a14...").from_hex()

b1.xor(b2)        # another Chef works as an argument
b1.xor(0x13)      # so does an int ...
b1.xor("key")     # ... a str ...
b1.xor(b"\x13")   # ... or bytes

result = b1.xor(b2)
result.o          # raw bytes
print(result)     # decoded as text
```

The operations are also plain functions in `pychef.ops` that take and return bytes:

```python
from pychef import ops

ops.xor(b"data", b"key")
```

## Operations

| Operation | What it does |
|---|---|
| `from_hex()` | Parse hex in most formats: `abab`, `0xabab`, `ab:ab`, `0xab, 0xab`, `\xab\xab` |
| `to_hex()` | Bytes to a hex string |
| `from_base64()` / `to_base64()` | Base64 decode / encode |
| `xor(key)` | Repeating-key XOR; key can be bytes, str, int or a Chef |
| `clean()` | Remove all whitespace |
| `u_shift(charset, keep)` | Map each unique symbol to a letter, for symbol/emoji substitution ciphers |

## Adding an operation

1. Write a bytes-in, bytes-out function in `pychef/ops.py`.
2. Add `name = _chain(ops.name)` to the `Chef` class in `pychef/chef.py`.
3. Add a test in `tests/test_ops.py`.

## Methods directly on bytes and str (optional hack)

```python
from pychef import patch_builtins
patch_builtins()

b"4142".from_hex().xor("1313".from_hex())
```

Needs `pip install forbiddenfruit`, works only on CPython, and changes `bytes` and `str` for the whole program. Fine for quick scripts; avoid it in anything you share.

## Tests

```
pytest
```
