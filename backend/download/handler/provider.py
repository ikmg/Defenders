from uuid import uuid4

from database import KeepedReportRecord, ProvidedReportRecord, ProvidedReport
from tools.date_time import DateTimeConvert


class ProvidedReportHandler:

    def __init__(self, session):
        self.session = session
        self.rows = None
        self.get_data()

    @property
    def count(self):
        return len(self.rows)

    def get_data(self):
        self.rows = self.session.query(KeepedReportRecord)
        self.rows = self.rows.filter(KeepedReportRecord.critical_messages == '')
        self.rows = self.rows.filter(KeepedReportRecord.provided_report_record == None)
        self.rows = self.rows.filter(KeepedReportRecord.is_find_in_orders == True)
        self.rows = self.rows.order_by(KeepedReportRecord.keeped_report_id)
        self.rows = self.rows.order_by(KeepedReportRecord.keep_row_num)
        self.rows = self.rows.all()

    def make_export(self):
        model_export = ProvidedReport()
        model_export.created_utc = DateTimeConvert().value
        model_export.id = model_export.created_utc.strftime('%Y%m%d-%H%M%S')
        self.session.add(model_export)
        self.session.flush()

        for index, record in enumerate(self.rows):
            model_row = ProvidedReportRecord()
            model_row.id = str(uuid4())
            model_row.created_utc = DateTimeConvert().value
            model_row.provided_report_id = model_export.id
            model_row.row_number = index + 1
            model_row.keeped_report_record_id = record.id
            self.session.add(model_row)
            self.session.flush()
        self.session.commit()
