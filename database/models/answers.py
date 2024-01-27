from sqlalchemy import Column, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship

from . import BaseModel


class ImportAnswer(BaseModel):
    __tablename__ = 'answer_imports'

    provided_report_id = Column(String, ForeignKey('provided_reports.id', ondelete='CASCADE'), primary_key=True, nullable=False, doc='')
    import_date = Column(Date, nullable=False)
    reg_number = Column(String, nullable=False)
    user = Column(String, nullable=False)
    result = Column(String, nullable=False)

    provided_report = relationship('ProvidedReport', uselist=False, lazy=True)


class InitAnswer(BaseModel):
    __tablename__ = 'answer_init'

    provided_report_record_id = Column(String, ForeignKey('provided_report_records.id', ondelete='CASCADE'), primary_key=True, nullable=False, doc='')
    init_date = Column(DateTime(timezone=True), nullable=False)
    number = Column(String, nullable=False)
    status = Column(String, nullable=False)
    comment = Column(String, nullable=False)

    provided_report_record = relationship('ProvidedReportRecord', uselist=False, lazy=True)
