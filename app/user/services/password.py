import base64
import hashlib
import hmac
import secrets


_SCHEME = "scrypt"
_N = 2**14
_R = 8
_P = 1
_DKLEN = 32


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    derived = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=_N,
        r=_R,
        p=_P,
        dklen=_DKLEN,
    )
    encode = lambda value: base64.b64encode(value).decode("ascii")
    return f"{_SCHEME}${_N}${_R}${_P}${encode(salt)}${encode(derived)}"


def verify_password(password: str, stored_password: str) -> tuple[bool, bool]:
    """Return (valid, needs_rehash), accepting the legacy plain value once."""
    if not stored_password or not stored_password.startswith(f"{_SCHEME}$"):
        return hmac.compare_digest(password, stored_password or ""), True

    try:
        _, n, r, p, encoded_salt, encoded_hash = stored_password.split("$", 5)
        salt = base64.b64decode(encoded_salt)
        expected = base64.b64decode(encoded_hash)
        derived = hashlib.scrypt(
            password.encode("utf-8"),
            salt=salt,
            n=int(n),
            r=int(r),
            p=int(p),
            dklen=len(expected),
        )
    except (TypeError, ValueError):
        return False, False

    return hmac.compare_digest(derived, expected), False
