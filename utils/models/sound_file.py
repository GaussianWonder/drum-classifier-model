from utils.files.file import File
from sqlalchemy import Column, Integer, String

from utils.models import Base

"""
The SoundFileModel is an unloaded SoundFile. Managed with SqlAlchemy ORM.
It is mappable to the SoundFile class, which can be used to perform algorithms on.
This intermediate step helps with caching, memory issues, and async processing.
"""


class SoundFileModel(Base):
    __tablename__ = "sound_files"

    # Identifier
    id = Column(Integer, primary_key=True)
    # File identifier
    path = Column(String(260))
    # File content identifier
    md5 = Column(String(255))
    sha1 = Column(String(255))
    sha256 = Column(String(255))

    # TODO relation with sound_file_result which stores paths to exported calculations

    def __init__(self, path: str, md5: str, sha1: str, sha256: str):
        self.path = path
        self.md5 = md5
        self.sha1 = sha1
        self.sha256 = sha256

    @classmethod
    def from_file(cls, file: File):
        identity = file.identity()
        return cls(file.path, identity.md5, identity.sha1, identity.sha256)

    def __repr__(self):
        return f"SoundFileModel(" \
               f"id={self.id!r}," \
               f"path={self.path!r}," \
               f"md5={self.md5!r}," \
               f"sha1={self.sha1!r}," \
               f"sha256={self.sha256!r})"
