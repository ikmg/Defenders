from sqlalchemy import Column, Boolean, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import BaseModel


# -------------
# Киперы файлов
# -------------


class KeeperFileModel(BaseModel):
    """Абстрактная модель хранителя данных о загруженном файле."""
    __abstract__ = True

    hash_sum = Column(String, primary_key=True, nullable=True, doc='Хэш-сумма эталонного экземпляра файла')
    original_filename = Column(String, nullable=False, doc='Имя оригинального файла (без пути к нему)')
    instance_filename = Column(String, nullable=False, doc='Путь к эталонному экземпляру скопированного файла')
    is_on_template = Column(Boolean, nullable=False, default=False, doc='Файл соответствует шаблону')
    is_loaded = Column(Boolean, nullable=False, default=False, doc='Запись всех строк из файла завершена')
    note = Column(String, nullable=True, doc='Примечания программы к загруженному файлу')


class KeepedOrder(KeeperFileModel):
    """Хранитель файлов с приказами ОШУ Росгвардии об участниках СВО"""
    __tablename__ = 'keeped_orders'

    keeped_order_records = relationship('KeepedOrderRecord', uselist=True, lazy=True, back_populates='keeped_order')


class KeepedReport(KeeperFileModel):
    """Хранитель файлов отчетов войск с уволенными участниками СВО"""
    __tablename__ = 'keeped_reports'

    eskk_military_subject_id = Column(String, ForeignKey('eskk_military_subjects.id', ondelete='CASCADE'), nullable=False, doc='Принадлежность отчета к субъекту войск')
    contact_info = Column(String, nullable=True, doc='Контактные данные отправителя отчета')
    is_finished = Column(Boolean, default=False, nullable=False)

    eskk_military_subject = relationship('EskkMilitarySubject', uselist=False, lazy=True)
    keeped_report_records = relationship('KeepedReportRecord', lazy=True, back_populates='keeped_report')


# class KeepedAnswer(KeeperFileModel):
#     """Хранитель информации о протоколах загрузки СФР России"""
#     __tablename__ = 'keeped_answers'


# -------------------
# Киперы строк файлов
# -------------------


class KeeperRecordModel(BaseModel):
    """Абстрактная модель хранителя информации, содержащейся в загруженном файле."""
    __abstract__ = True

    id = Column(String, primary_key=True, nullable=False, index=True, doc='Идентификатор записи')
    keep_row_num = Column(Integer, nullable=False, doc='Хранимый номер строки загрузки')
    file_row_num = Column(Integer, nullable=False, doc='Действительный номер строки в файле')
    warning_messages = Column(String, nullable=False, doc='Ошибки с предупреждением')
    critical_messages = Column(String, nullable=False, doc='Критические ошибки')


class KeepedOrderRecord(KeeperRecordModel):
    """Хранитель загруженной строки приказа ОШУ Росгвардии"""
    __tablename__ = 'keeped_order_records'

    keeped_order_id = Column(String, ForeignKey('keeped_orders.id', ondelete='CASCADE'), nullable=False, doc='Идентификатор приказа')
    linked_order_person_period_id = Column(String, ForeignKey('linked_order_person_periods.id', ondelete='CASCADE'), nullable=False, doc='Строка приказа с периодом участия в СВО')

    keeped_order = relationship('KeepedOrder', uselist=False, lazy=True)
    linked_order_person_period = relationship('LinkedOrderPersonPeriod', uselist=False, lazy=True)


class KeepedReportRecord(KeeperRecordModel):
    """Хранитель загруженной строки отчета войск"""
    __tablename__ = 'keeped_report_records'

    keeped_report_id = Column(String, ForeignKey('keeped_reports.id', ondelete='CASCADE'), nullable=False, doc='Идентификатор отчета')
    linked_defender_id = Column(String, ForeignKey('linked_defenders.id', ondelete='CASCADE'), nullable=False, doc='Строка отчета с защитником Отечества')
    is_find_in_orders = Column(Boolean, nullable=False, default=False, doc='Защитник Отечества найден (идентифицирован) в приказах ОШУ Росгвардии')

    keeped_report = relationship('KeepedReport', uselist=False, lazy=True, back_populates='keeped_report_records')
    linked_defender = relationship('LinkedDefender', uselist=False, lazy=True)
    provided_report_record = relationship('ProvidedReportRecord', uselist=False, lazy=True, back_populates='keeped_report_record')


# class KeepedAnswerRecords(KeeperRecordModel):
#     """Хранитель информации о протоколах идентификации СФР России"""
#     __tablename__ = 'keeped_answer_records'
