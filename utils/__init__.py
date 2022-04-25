from utils.files import SoundFile
from utils.models.sound_file import SoundFileModel


def model_to_sound_file(model: SoundFileModel):
    return SoundFile(model.path)


def sound_file_to_model(sound_file: SoundFile):
    return SoundFileModel(sound_file)
