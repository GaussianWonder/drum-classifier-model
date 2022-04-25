import files as futils
from files import SoundFile
from models import init_sqlite

if __name__ == '__main__':
    init_sqlite()

    # for category, file in futils.get_files():
    #     with SoundFile.from_file(file, category) as sound:
    #         sound.sound_wave_fig().show()
    #         spectrogram = sound.spectrogram_fig().show()
    #         mel_spectrogram = sound.mel_spectrogram_fig().show()
