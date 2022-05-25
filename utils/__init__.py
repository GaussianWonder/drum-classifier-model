from files import SoundFile
from models import SoundFileModel, engine, Session
from sqlalchemy import select, func


def model_to_sound_file(model: SoundFileModel):
    return SoundFile(model.path)


# def sound_file_to_model(sound_file: SoundFile):
#     return SoundFileModel(sound_file)


def number_of_sound_files() -> int:
    with engine.connect() as con:
        return con.execute(select([func.count()]).select_from(SoundFileModel)).scalar()


def find_sound_file_by_index(index: int) -> SoundFileModel:
    with Session(engine) as session:
        return session.query(SoundFileModel).get(index)
