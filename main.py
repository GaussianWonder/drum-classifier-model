import torch
import torchaudio
import cli
from models import init_sqlite

import files as futils
from files import SoundFile

opts = cli.get_args()

print('using torch: ' + torch.__version__)
print('using torchaudio: ' + torchaudio.__version__)

if __name__ == '__main__':
    init_sqlite()

    if cli.should_reset(opts):
        # Delete everything and Rescan
        pass

    if cli.should_rescan(opts):
        # Rescan
        pass

    # for category, file in futils.get_files():
    #     with SoundFile.from_file(file, category) as sound:
    #         print(sound.get_path_labels())
    #         sound.sound_wave_fig().show()
    #         spectrogram = sound.spectrogram_fig().show()
    #         mel_spectrogram = sound.mel_spectrogram_fig().show()
