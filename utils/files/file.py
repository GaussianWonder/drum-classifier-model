import os


class File:
    path: str
    name: str

    def __init__(self, path: str, throw: bool = False):
        self.path = path
        if throw and not self.exists():
            raise Exception('File {path} does not exist!'.format(path=path))
        self.name = os.path.basename(path)

    def exists(self):
        return os.path.exists(self.path)
