from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import BaseModel


class ProvidedReport(BaseModel):
    """Поставщик файлов для СФР России"""
    __tablename__ = 'provided_reports'

    id = Column(String, primary_key=True, nullable=False, index=True, doc='Идентификатор поставляемого файла (его имя)')

    provided_report_records = relationship('ProvidedReportRecord', uselist=True, lazy=True, back_populates='provided_report')
    answer_import = relationship('ImportAnswer', uselist=False, lazy=True, back_populates='provided_report')


class ProvidedReportRecord(BaseModel):
    """Поставщик записей в файлах для СФР России"""
    __tablename__ = 'provided_report_records'

    provided_report_id = Column(String, ForeignKey('provided_reports.id', ondelete='CASCADE'), primary_key=True, nullable=False, doc='Идентификатор файла')
    row_number = Column(Integer, primary_key=True, nullable=False, doc='Номер строки в файле')
    keeped_report_record_id = Column(String, ForeignKey('keeped_report_records.id', ondelete='CASCADE'), unique=True, nullable=False, doc='Идентификатор хранимой строки отчета войск')

    provided_report = relationship('ProvidedReport', uselist=False, lazy=True, back_populates='provided_report_records')
    keeped_report_record = relationship('KeepedReportRecord', uselist=False, lazy=True, back_populates='provided_report_record')
    answer_init = relationship('InitAnswer', uselist=False, lazy=True, back_populates='provided_report_record')
