import functools

from . import ops


def _unwrap(value):
    # Let a Chef be passed wherever an operation expects bytes
    return value.data if isinstance(value, Chef) else value


def _chain(fn):
    # Turn an operation into a method that returns a new Chef
    @functools.wraps(fn)
    def method(self, *args, **kwargs):
        args = [_unwrap(a) for a in args]
        kwargs = {k: _unwrap(v) for k, v in kwargs.items()}
        return type(self)(fn(self.data, *args, **kwargs))
    return method


class Chef:
    def __init__(self, data: bytes | str = b""):
        self.data = data.encode() if isinstance(data, str) else bytes(data)

    xor = _chain(ops.xor)
    to_base64 = _chain(ops.to_base64)
    from_base64 = _chain(ops.from_base64)
    clean = _chain(ops.clean)
    from_hex = _chain(ops.from_hex)
    to_hex = _chain(ops.to_hex)
    u_shift = _chain(ops.u_shift)

    @property
    def o(self) -> bytes:
        return self.data

    def __bytes__(self) -> bytes:
        return self.data

    def __str__(self) -> str:
        return self.data.decode(errors="replace")

    def __repr__(self) -> str:
        return f"Chef({self.data!r})"


def patch_builtins():
    # Add every Chef operation to bytes and str, so b"4142".from_hex() works.
    # Hack: needs the forbiddenfruit package and only works on CPython.
    try:
        from forbiddenfruit import curse
    except ImportError:
        raise ImportError("patch_builtins needs forbiddenfruit: pip install forbiddenfruit") from None
    for name, attr in vars(Chef).items():
        if callable(attr) and not name.startswith("_"):
            for t in (bytes, str):
                curse(t, name, lambda self, *a, _n=name, **k: getattr(Chef(self), _n)(*a, **k))
