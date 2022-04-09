import os


class File:
    path: str

    def __init__(self, path: str, throw: bool = False):
        self.path = path
        if throw and not self.exists():
            raise Exception('File {path} does not exist!'.format(path=path))

    def exists(self):
        return os.path.exists(self.path)
