import os
from string import digits, punctuation as special, ascii_letters as letters

charset = digits + special + letters

def random_int(x: int) -> int:
    return int.from_bytes(os.urandom(32))%x

def random_char() -> str:
    return charset[random_int(len(charset))]

def random_password(length: int) -> str:
    return str().join([random_char() for _ in range(length)])

print(random_password(20))