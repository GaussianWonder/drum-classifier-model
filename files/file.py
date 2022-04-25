import os
import hashlib
from typing import TypeVar, Callable, AnyStr

# Types to be used inside the File class
T = TypeVar("T")

"""
The File class defines a file and provides useful properties for a file.
"""


class File:
    path: str = ''
    name: str = ''
    ext: str = ''

    def __init__(self, path: str = '', throw: bool = False):
        self.path = path
        if throw and not self.exists():
            raise Exception('File {path} does not exist!'.format(path=path))

        name, ext = os.path.splitext(path)
        self.name = name
        self.ext = ext

    @classmethod
    def safe_load(cls, path: str):
        return cls(path, throw=True)

    @classmethod
    def unsafe_load(cls, path: str):
        return cls(path, throw=False)

    def exists(self) -> bool:
        return os.path.exists(self.path)

    def chunk_reducer(self, reducer: Callable[[T, AnyStr], T], init: T, chunk_size: int = 1024) -> T:
        if not self.exists():
            return init

        next_iter: T = init
        with open(self.path, 'rb') as file:
            chunk: AnyStr = b'?'
            while chunk != b'':
                chunk = file.read(chunk_size)
                next_iter = reducer(next_iter, chunk)
        return next_iter

    def file_hash(self, hash_function) -> str:
        reduced = self.chunk_reducer(
            reducer=lambda hasher, chunk: hasher.update(chunk),
            init=hash_function
        )
        return reduced.hexdigest()

    def sha1(self):
        return self.file_hash(hashlib.sha1())

    def sha256(self):
        return self.file_hash(hashlib.sha256())

    def md5(self):
        return self.file_hash(hashlib.md5())

    def identity(self):
        return {
            "md5": self.md5(),
            "sha1": self.sha1(),
            "sha256": self.sha256(),
        }
