import numpy as np
from numpy import number
import librosa
import librosa.display
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from utils.files.file import File

"""
The class which is able to load the sound from and perform several calculations on
It can be constructed from `path`, `File` or `SoundFileModel`
"""


class SoundFile(File):
    samples: np.ndarray = []
    sample_rate: number = -1
    duration: number

    def __init__(self, path: str):
        super().__init__(path, True)

    @classmethod
    def from_path(cls, path: str):
        return cls(path)

    @classmethod
    def from_file(cls, file: File):
        return cls(file.path)

    """
    To load the sound automatically use the `with as` syntax
    """
    def load_sound(self):
        samples, sample_rate = librosa.load(self.path, sr=None)
        self.samples = samples
        self.sample_rate = sample_rate
        self.duration = librosa.get_duration(y=samples, sr=sample_rate)

    # This is always true when using `with as` syntax
    def is_loaded(self):
        return self.sample_rate < 0 or not self.samples or len(self.samples) == 0

    def plot_name(self, plot_type: str):
        return '{type} {name} {rate}Hz'.format(type=plot_type, name=self.name, rate=self.sample_rate)

    def plot_prepare(self, plot_type: str, fig_size: (number, number) = (14, 5)):
        figure: Figure = plt.figure(figsize=fig_size)
        plt.title(self.plot_name(plot_type))
        return figure

    def spectrogram(self):
        # TODO calculate n_fft
        return librosa.stft(self.samples)

    def db_spectrogram(self):
        return librosa.amplitude_to_db(self.spectrogram(), ref=np.min)

    def mel_spectrogram(self):
        magnitude, phase = librosa.magphase(self.spectrogram())
        # TODO calculate n_fft
        return librosa.feature.melspectrogram(S=magnitude, sr=self.sample_rate)

    def db_mel_spectrogram(self):
        return librosa.amplitude_to_db(self.mel_spectrogram(), ref=np.min)

    def sound_wave_fig(self) -> Figure:
        fig = self.plot_prepare('Sound Wave')
        librosa.display.waveshow(self.samples, sr=self.sample_rate)
        return fig

    def spectrogram_fig(self) -> Figure:
        fig = self.plot_prepare('Spectrogram')
        librosa.display.specshow(self.db_spectrogram(), sr=self.sample_rate, x_axis='time', y_axis='hz')
        fig.colorbar(mappable=plt.gci(), format='%+2.0f dB')
        return fig

    def mel_spectrogram_fig(self) -> Figure:
        fig = self.plot_prepare('Mel Spectrogram')
        librosa.display.specshow(self.db_mel_spectrogram(), sr=self.sample_rate, x_axis='time', y_axis='mel')
        fig.colorbar(mappable=plt.gci(), format='%+2.0f dB')
        return fig

    def __enter__(self):
        self.load_sound()
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        print("Error thrown when dealing with SoundFile")
