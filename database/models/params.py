from sqlalchemy import Column, String
from ._base_ import Base


class DefenderParameter(Base):
    """Параметры приложения"""
    __tablename__ = 'def_params'

    param = Column(String, primary_key=True, nullable=False, doc='Наименование параметра')
    value = Column(String, nullable=True, doc='Значение параметра')
