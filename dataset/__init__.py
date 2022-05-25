from torchaudio.transforms import MelSpectrogram
from numpy import number
from torch.utils.data import Dataset

from utils import number_of_sound_files, find_sound_file_by_index
from files import get_files, SoundFile


class AudioAssets(Dataset):
    files = get_files()

    # def __init__(self):
    #     pass

    def __len__(self):
        # TODO extract from sqlite
        # return number_of_sound_files()
        print(self.files)
        return len(self.files)

    def __getitem__(self, item):
        # TODO extract from sqlite, and get the preprocessed mel_spectrogram
        category, path = self.files[item]
        with SoundFile.from_file(path) as sound:
            return sound.mel_spectrogram(), category
        # sound_file = find_sound_file_by_index(item
        # self.files[item]
        # return sound_file
