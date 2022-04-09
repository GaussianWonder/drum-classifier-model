import utils.files as futils


if __name__ == '__main__':
    for sound in futils.SOUNDS.get('all'):
        sound.plot_sound_wave()
