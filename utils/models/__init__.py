from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

engine = create_engine("sqlite:///assets/cache.db", echo=True, future=True)


def init_sqlite():
    Base.metadata.create_all(engine)


def select_all(statement):
    with Session(engine) as session:
        return session.scalars(statement)


def persist_all(objects):
    with Session(engine) as session:
        session.add_all(objects)
        session.commit()
