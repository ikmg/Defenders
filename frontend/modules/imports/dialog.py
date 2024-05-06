from PyQt5.QtWidgets import QDialog

from frontend import Ui_Dialog_import
from .tv_data import ImportData
from tools import DTConvert
from .tv_dialog import DialogTableModel


class DialogImport(QDialog, Ui_Dialog_import):

    def __init__(self, import_item: ImportData):
        self.import_item = import_item
        QDialog.__init__(self)
        self.setupUi(self)

        self.set_content()
        self.set_table_view()

        self.show()

    def set_content(self):
        self.lineEdit_created_utc.setText(DTConvert(self.import_item.model.created_utc).dtstring)
        self.lineEdit_reg_num.setText(self.import_item.model.id)
        self.lineEdit_subject.setText(self.import_item.model.eskk_military_subject.short_name)
        self.lineEdit_contacts.setText(self.import_item.model.contact_info)
        self.lineEdit_stat.setText(str(self.import_item))
        self.lineEdit_status.setText('')

    def set_table_view(self):
        rows = self.import_item.dialog_table_model_rows()
        table_model = DialogTableModel(rows)
        self.tableView_rows.setSortingEnabled(True)
        self.tableView_rows.setModel(table_model)
        self.tableView_rows.resizeColumnsToContents()
