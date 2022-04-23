import utils.files as futils
from utils.files import SoundFile
from utils.models import init_sqlite

if __name__ == '__main__':
    init_sqlite()

    for file in futils.FILES.get('all'):
        with SoundFile.from_file(file) as sound:
            sound.sound_wave_fig().show()
            spectrogram = sound.spectrogram_fig().show()
            mel_spectrogram = sound.mel_spectrogram_fig().show()
