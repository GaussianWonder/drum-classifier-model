from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session

engine = create_engine("sqlite:///assets/cache.db", echo=True, future=True)

Base = declarative_base()

# Models (so that init_sqlite works)
from models.sound_file import SoundFileModel
from models.label import LabelModel


def init_sqlite():
    Base.metadata.create_all(engine)


def select_all(statement):
    with Session(engine) as session:
        return session.scalars(statement)


def persist_all(objects):
    with Session(engine) as session:
        session.add_all(objects)
        session.commit()
