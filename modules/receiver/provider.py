from datetime import datetime
from uuid import uuid4

from sqlalchemy import or_

from database import KeepedReportRecord, ProvidedReportRecord, ProvidedReport, KeepedReport
from tools.date_and_time import datetime_timezone


class ProvidedReportHandler:

    def __init__(self, session, keeped_report_id=None):
        self.report_id = keeped_report_id
        self.report_records = None
        self.message = ''
        self.count = 0

        self.session = session
        # self.id = datetime_timezone().strftime('%Y%m%d-%H%M%S')

        self.report = ProvidedReport()
        self.report.id = self.report_id if self.report_id else datetime_timezone().strftime('%Y%m%d-%H%M%S')
        self.report.created_utc = datetime.now()

        self.get_records()

    def get_records(self):
        self.report_records = self.session.query(KeepedReportRecord)
        self.report_records = self.report_records.join(KeepedReport)
        if self.report_id:
            self.report_records = self.report_records.filter(KeepedReportRecord.keeped_report_id == self.report_id)
        self.report_records = self.report_records.filter(KeepedReport.is_loaded == True)
        self.report_records = self.report_records.filter(KeepedReportRecord.critical_messages == '')
        self.report_records = self.report_records.filter(KeepedReportRecord.provided_report_record == None)
        self.report_records = self.report_records.filter(KeepedReportRecord.is_find_in_orders == True)
        self.report_records = self.report_records.order_by(KeepedReportRecord.keeped_report_id)
        self.report_records = self.report_records.order_by(KeepedReportRecord.keep_row_num)
        self.report_records = self.report_records.all()

        if self.report_records:
            self.count = len(self.report_records)
        else:
            self.message = 'Отсутствуют записи для экспорта'

    def get_records_migrate(self):
        self.report_records = self.session.query(KeepedReportRecord)
        if self.report_id:
            self.report_records = self.report_records.filter(KeepedReportRecord.keeped_report_id == self.report_id)
        self.report_records = self.report_records.filter(or_(KeepedReportRecord.critical_messages == '', KeepedReportRecord.critical_messages == 'персона отсутствует в приказах ОШУ'))
        self.report_records = self.report_records.filter(KeepedReportRecord.provided_report_record == None)
        self.report_records = self.report_records.order_by(KeepedReportRecord.keeped_report_id)
        self.report_records = self.report_records.order_by(KeepedReportRecord.keep_row_num)
        self.report_records = self.report_records.all()

        if self.report_records:
            self.count = len(self.report_records)
        else:
            self.message = 'Отсутствуют записи для экспорта'

    def get_records_migrate_compound_one(self):
        self.report_records = self.session.query(KeepedReportRecord)
        self.report_records = self.report_records.filter(
            or_(
                KeepedReportRecord.keeped_report_id == '0327-20231128-105016',
                KeepedReportRecord.keeped_report_id == '0918-20231130-092658',
                KeepedReportRecord.keeped_report_id == '4803-20231129-093039',
                KeepedReportRecord.keeped_report_id == '6713-20231129-092840'
            )
        )
        self.report_records = self.report_records.filter(or_(KeepedReportRecord.critical_messages == '', KeepedReportRecord.critical_messages == 'персона отсутствует в приказах ОШУ'))
        self.report_records = self.report_records.filter(KeepedReportRecord.provided_report_record == None)
        self.report_records = self.report_records.order_by(KeepedReportRecord.keeped_report_id)
        self.report_records = self.report_records.order_by(KeepedReportRecord.keep_row_num)
        self.report_records = self.report_records.all()

        self.report.id = '20231130-100000'

        if self.report_records:
            self.count = len(self.report_records)
        else:
            self.message = 'Отсутствуют записи для экспорта'

    def get_records_migrate_compound_two(self):
        self.report_records = self.session.query(KeepedReportRecord)
        self.report_records = self.report_records.filter(
            or_(
                KeepedReportRecord.keeped_report_id == '0001-20231130-123409',
                KeepedReportRecord.keeped_report_id == '0001-20231205-093957',
                KeepedReportRecord.keeped_report_id == '0115-20231205-094102',
                KeepedReportRecord.keeped_report_id == '0327-20231205-092409',
                KeepedReportRecord.keeped_report_id == '0441-20231130-161130',
                KeepedReportRecord.keeped_report_id == '3219-20231205-093922',
                KeepedReportRecord.keeped_report_id == '3481-20231201-145913',
                KeepedReportRecord.keeped_report_id == '5721-20231201-152140',
                KeepedReportRecord.keeped_report_id == '5765-20231205-093811',
                KeepedReportRecord.keeped_report_id == '5850-20231201-145105',
                KeepedReportRecord.keeped_report_id == '6948-20231205-093715'
            )
        )
        self.report_records = self.report_records.filter(or_(KeepedReportRecord.critical_messages == '', KeepedReportRecord.critical_messages == 'персона отсутствует в приказах ОШУ'))
        self.report_records = self.report_records.filter(KeepedReportRecord.provided_report_record == None)
        self.report_records = self.report_records.order_by(KeepedReportRecord.keeped_report_id)
        self.report_records = self.report_records.order_by(KeepedReportRecord.keep_row_num)
        self.report_records = self.report_records.all()

        self.report.id = '20231205-100000'

        if self.report_records:
            self.count = len(self.report_records)
        else:
            self.message = 'Отсутствуют записи для экспорта'

    def export(self):
        print(self.report.id)
        self.session.add(self.report)
        self.session.flush()

        for index, record in enumerate(self.report_records):
            model = ProvidedReportRecord()
            model.id = str(uuid4())
            model.created_utc = datetime.now()
            model.provided_report_id = self.report.id
            model.row_number = index + 1
            model.keeped_report_record_id = record.id

            self.session.add(model)
            self.session.flush()

        self.session.commit()
        self.message = 'Экспортировано {} записей'.format(self.count)
