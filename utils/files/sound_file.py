import numpy as np
from numpy import number
import librosa
import librosa.display
import matplotlib.pyplot as plt

from utils.files.file import File


class SoundFile(File):
    samples: np.ndarray = []
    sample_rate: number = 22050

    def __init__(self, path: str, throw: bool = True):
        super().__init__(path, throw)
        samples, sample_rate = librosa.load(self.path, sr=None)
        self.samples = samples
        self.sample_rate = sample_rate

    def plot_sound_wave(self):
        plt.figure(figsize=(14, 5))
        librosa.display.waveshow(self.samples, sr=self.sample_rate)
        plt.show()
