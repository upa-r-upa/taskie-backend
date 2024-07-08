from contextlib import contextmanager
from fastapi import Depends
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from app.core.config import DATABASE_URI

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def initialize_database():
    inspector = inspect(engine)
    table_names = inspector.get_table_names()

    if len(table_names) <= 1:
        Base.metadata.create_all(engine)
        print("Database is initialized.")
    else:
        print("Database is already initialized.")


def get_db() -> Session:
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


@contextmanager
def tx_manager(session: Session = Depends(get_db)) -> None:
    try:
        if not session.in_transaction():
            session.begin()
        yield
    finally:
        session.commit()
