from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel(Base):
    """
    Абстрактная базовая модель построения таблиц.
    Первичный ключ отсутствует.
    Содержит идентификатор записи и временную метку создания.
    """
    __abstract__ = True

    id = Column(String, unique=True, nullable=False, index=True, doc='Идентификатор записи')
    created_utc = Column(DateTime(timezone=True), default=func.now(), doc='Временная метка создания записи')
