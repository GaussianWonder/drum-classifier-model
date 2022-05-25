import torch
import torchaudio
import cli
from models import init_sqlite

import files as futils
from files import SoundFile

from dataset import AudioAssets

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

    audioDataset = AudioAssets()
    print(len(audioDataset))

    spectrogram, category = audioDataset[0]

