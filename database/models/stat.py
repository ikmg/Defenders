from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from ._base_ import Base


class OrdersStat(Base):
    """Параметры приложения"""
    __tablename__ = 'stat_orders'

    keeped_order_id = Column(String, ForeignKey('keeped_orders.id', ondelete='CASCADE'), primary_key=True, nullable=False, doc='Идентификатор приказа')
    data_type = Column(String, primary_key=True, nullable=False, doc='Тип данных статистики')
    name = Column(String, primary_key=True, nullable=False, doc='Наименование данных статистики')
    sort = Column(Integer, nullable=False, doc='Порядок вывода в отчет')
    count = Column(Integer, nullable=False, doc='Общее количество')
    A = Column(Integer, nullable=False, doc='Офицеров (жетоны серии А)')
    A_percent = Column(Float, nullable=False, doc='Процент офицеров от общего количества')
    PR = Column(Integer, nullable=False, doc='Прапорщики (жетоны серии ПР)')
    PR_percent = Column(Float, nullable=False, doc='Процент прапорщиков от общего количества')
    RS = Column(Integer, nullable=False, doc='Солдаты/сержанты (жетоны серии РС)')
    RS_percent = Column(Float, nullable=False, doc='Процент солдат/сержантов от общего количества')
    other = Column(Integer, nullable=False, doc='Другие (жетоны неизвестных серий)')
    other_percent = Column(Float, nullable=False, doc='Процент других от общего количества')
    note = Column(String, nullable=True, doc='Примечание к статистическим данным')

    keeped_order = relationship('KeepedOrder', uselist=False, lazy=True)
