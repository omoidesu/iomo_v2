import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from src.config import redis_db, redis_host, redis_pass, redis_port, redis_subscribe


class SqlSession:
    _conn_url: str
    _session: Session

    def __init__(self, conn_url: str):
        self._conn_url = conn_url

        engine = create_engine(self._conn_url, echo=True, pool_size=20, max_overflow=0, pool_recycle=3600)

        _sessionmaker = sessionmaker(bind=engine)
        self._session = _sessionmaker()

    def session(self) -> Session:
        return self._session


class Redis:
    _instance = None
    _conn = None
    _pubsub = None

    def __init__(self):
        pool = redis.ConnectionPool(host=redis_host, port=redis_port, password=redis_pass, db=redis_db)
        self._conn = redis.Redis(connection_pool=pool)
        self._pubsub = self._conn.pubsub()
        self._pubsub.psubscribe(redis_subscribe)

    def get_connection(self):
        return self._conn

    @property
    def pubsub(self):
        return self._pubsub

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
