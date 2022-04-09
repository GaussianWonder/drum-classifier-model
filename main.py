import utils.files as futils


if __name__ == '__main__':
    for sound in futils.SOUNDS.get('all'):
        sound.sound_wave_fig().show()
        spectrogram = sound.spectrogram_fig().show()
        mel_spectrogram = sound.mel_spectrogram_fig().show()
