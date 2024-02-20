from backend import csv_from_list, export_data
from database import ProvidedReport
from tools import DTConvert


class ExportData:

    def __init__(self, app):
        self.app = app
        self.model = None

    @property
    def session(self):
        return self.app.database.session

    def data(self):
        return export_data(self.session, self.model.id)

    def get_export(self, export_id):
        self.model = self.session.query(ProvidedReport)
        self.model = self.model.filter(ProvidedReport.id == export_id)
        self.model = self.model.scalar()

    def create_export_file(self):
        destination = self.app.storage.exports.add_file('{}.csv'.format(self.model.id))
        csv_from_list(destination.path, self.data())
        destination.start()

    def table_model_row(self):
        return [
            self.model.id,
            DTConvert(self.model.created_utc).dtstring,  # должно быть дата/время
            len(self.model.provided_report_records),
            self.model.answer_import.reg_number if self.model.answer_import else 'Протокол не поступал',
            self.model.answer_import.result if self.model.answer_import else '---'
        ]


class ExportsListData:
    
    def __init__(self, app):
        self.app = app
        self.rows = []
        self.total_answered = 0

    @property
    def session(self):
        return self.app.database.session
    
    def get_data(self):
        models = self.session.query(ProvidedReport)
        models = models.order_by(ProvidedReport.created_utc.desc())
        models = models.all()
        zero_count = len(str(len(models)))
        for index, model in enumerate(models):
            exported = ExportData(self.app)
            exported.model = model
            self.rows.append([str(index + 1).zfill(zero_count)] + exported.table_model_row())
        return self.rows
