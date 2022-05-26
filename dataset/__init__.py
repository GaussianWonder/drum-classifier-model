from typing import Any

from torch.utils.data import Dataset

from files import get_files, SoundFile, CATEGORIES


class AudioAssets(Dataset):
    files: list[tuple[Any, Any]]
    path: str

    def __init__(self, path: str):
        super().__init__()
        self.path = path
        self.files = get_files(path)

    def __len__(self):
        # TODO extract from sqlite
        # return number_of_sound_files()
        return len(self.files)

    def __getitem__(self, index):
        # TODO extract from sqlite, and get the preprocessed mel_spectrogram
        category, file = self.files[index]
        with SoundFile.from_file(file) as sound:
            return sound.mel_spectrogram(), CATEGORIES.index(category)
        # sound_file = find_sound_file_by_index(item
        # self.files[item]
        # return sound_file
