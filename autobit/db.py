from __future__ import unicode_literals, absolute_import
from contextlib import contextmanager
from datetime import datetime
import logging
from os import getenv
import guessit
from sqlalchemy import create_engine, Column, Integer, Unicode, DateTime, Binary
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


logger = logging.getLogger(__name__)

Base = declarative_base()
Base.__repr__ = lambda self: "<{}({})>".format(
    self.__class__.__name__,
    ', '.join(["{}={}".format(k, repr(self.__dict__[k])) for k in self.__dict__ if k[0] != '_'])
)

Session = sessionmaker()


class AutoBitException(Exception):
    pass


class InternalError(AutoBitException):
    pass


class DuplicateError(AutoBitException):
    pass


def make_engine(url: str="", echo=True, init=True) -> Engine:
    if not url:
        url = getenv("SQLALCHEMY_URI")
        if not url:
            url = "sqlite://"
            logger.warning("Using in-memory database")
    engine = create_engine(url, echo=echo)
    if init:
        init_db(engine)
    Session.configure(bind=engine)
    return engine


def init_db(engine: Engine):
    Base.metadata.create_all(engine)


@contextmanager
def ctx(ses):
    """Provide a transactional scope around a series of operations."""
    try:
        yield ses
        ses.commit()
    except IntegrityError as e:
        ses.rollback()
        logger.exception("Tried to create duplicate record")
        raise DuplicateError(e)
    except DBAPIError as e:
        ses.rollback()
        logger.exception("Error committing transaction.")
        raise InternalError(e)


class Release(Base):
    __tablename__ = "release"
    release_id = Column(Integer, primary_key=True)
    name = Column(Unicode(length=128), nullable=False)
    media_type = Column(Integer, nullable=False)
    torrent_file = Column(Binary, nullable=False)
    torrent_id = Column(Integer, nullable=False)
    added_on = Column(DateTime, default=datetime.now())

    def __init__(self, name, torrent_id, media_type, media_class, source, torrent_file=None):
        self.name = self.normalize(name)
        self.torrent_id = int(torrent_id)
        self.media_type = media_type
        self.media_class = media_class
        self.source = source
        self.torrent_file = torrent_file

    @staticmethod
    def normalize(release_name: str) -> str:
        return ".".join(release_name.lower().split(" "))


def add_release(session: Session, release: Release) -> bool:
    try:
        with ctx(session):
            session.add(release)
    except DuplicateError:
        pass
    except InternalError:
        pass
    else:
        return True
    return False
