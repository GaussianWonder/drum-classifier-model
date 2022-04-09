import numpy as np
from numpy import number
import librosa
import librosa.display
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from utils.files.file import File


class SoundFile(File):
    samples: np.ndarray = []
    sample_rate: number = 22050

    def __init__(self, path: str, throw: bool = True):
        super().__init__(path, throw)
        samples, sample_rate = librosa.load(self.path, sr=None)
        self.samples = samples
        self.sample_rate = sample_rate

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
