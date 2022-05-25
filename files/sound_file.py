import torch
import torchaudio

import numpy as np
from numpy import number
from torchaudio.transforms import MelSpectrogram

import prefferences
from files.file import File
import os.path
from typing import List


"""
The class which is able to load the sound from and perform several calculations on
It can be constructed from `path`, `File` or `SoundFileModel`
"""


class SoundFile(File):
    # Sound data
    samples: np.ndarray = []
    sample_rate: number = -1

    # Sound info
    duration: number = -1

    def __init__(self, path: str):
        super().__init__(path, True)

    @classmethod
    def from_path(cls, path: str):
        return cls(path)

    @classmethod
    def from_file(cls, file: File):
        return cls(file.path)

    """
    Return the most significant label, least significant label, and all the others, in this order
    """
    def get_path_labels(self) -> (str, str, List[str]):
        relpath = os.path.relpath(self.path, "./assets")
        labels = os.path.dirname(relpath).split('/')
        return labels[0], labels[-1], labels[1:-1]

    """
    To load the sound automatically use the `with as` syntax
    """
    def load_sound(self):
        samples, sample_rate = torchaudio.load(self.path)
        samples = samples.to(prefferences.PROCESSING_DEVICE)
        p_samples, p_sr = prefferences.uniform_transformation(samples, sample_rate)
        self.samples = p_samples
        self.sample_rate = p_sr
        self.duration = float(len(p_samples)) / p_sr

    # This is always true when using `with as` syntax
    def is_loaded(self):
        return not(self.sample_rate < 0 or self.duration < 0 or not self.samples or len(self.samples) == 0)

    def mel_spectrogram(self):
        return prefferences.MEL_SPEC_TRANSFORM(self.samples)

    def __enter__(self):
        self.load_sound()
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_type is not None or exception_type is not None:
            print("Error thrown when dealing with SoundFile")
            print(exception_type)
            print(exception_value)
            print(exception_traceback)
