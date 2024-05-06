# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_importdVNHbd.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_Dialog_import(object):
    def setupUi(self, Dialog_import):
        if not Dialog_import.objectName():
            Dialog_import.setObjectName(u"Dialog_import")
        Dialog_import.resize(1087, 684)
        self.gridLayout = QGridLayout(Dialog_import)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_created_utc = QHBoxLayout()
        self.horizontalLayout_created_utc.setObjectName(u"horizontalLayout_created_utc")
        self.label_created_utc = QLabel(Dialog_import)
        self.label_created_utc.setObjectName(u"label_created_utc")

        self.horizontalLayout_created_utc.addWidget(self.label_created_utc)

        self.lineEdit_created_utc = QLineEdit(Dialog_import)
        self.lineEdit_created_utc.setObjectName(u"lineEdit_created_utc")
        self.lineEdit_created_utc.setEnabled(False)

        self.horizontalLayout_created_utc.addWidget(self.lineEdit_created_utc)

        self.horizontalLayout_created_utc.setStretch(0, 1)
        self.horizontalLayout_created_utc.setStretch(1, 6)

        self.verticalLayout.addLayout(self.horizontalLayout_created_utc)

        self.horizontalLayout_reg_num = QHBoxLayout()
        self.horizontalLayout_reg_num.setObjectName(u"horizontalLayout_reg_num")
        self.label_reg_num = QLabel(Dialog_import)
        self.label_reg_num.setObjectName(u"label_reg_num")

        self.horizontalLayout_reg_num.addWidget(self.label_reg_num)

        self.lineEdit_reg_num = QLineEdit(Dialog_import)
        self.lineEdit_reg_num.setObjectName(u"lineEdit_reg_num")
        self.lineEdit_reg_num.setEnabled(False)

        self.horizontalLayout_reg_num.addWidget(self.lineEdit_reg_num)

        self.horizontalLayout_reg_num.setStretch(0, 1)
        self.horizontalLayout_reg_num.setStretch(1, 6)

        self.verticalLayout.addLayout(self.horizontalLayout_reg_num)

        self.horizontalLayout_subject = QHBoxLayout()
        self.horizontalLayout_subject.setObjectName(u"horizontalLayout_subject")
        self.label_subject = QLabel(Dialog_import)
        self.label_subject.setObjectName(u"label_subject")

        self.horizontalLayout_subject.addWidget(self.label_subject)

        self.lineEdit_subject = QLineEdit(Dialog_import)
        self.lineEdit_subject.setObjectName(u"lineEdit_subject")
        self.lineEdit_subject.setEnabled(False)

        self.horizontalLayout_subject.addWidget(self.lineEdit_subject)

        self.horizontalLayout_subject.setStretch(0, 1)
        self.horizontalLayout_subject.setStretch(1, 6)

        self.verticalLayout.addLayout(self.horizontalLayout_subject)

        self.horizontalLayout_contacts = QHBoxLayout()
        self.horizontalLayout_contacts.setObjectName(u"horizontalLayout_contacts")
        self.label_contacts = QLabel(Dialog_import)
        self.label_contacts.setObjectName(u"label_contacts")

        self.horizontalLayout_contacts.addWidget(self.label_contacts)

        self.lineEdit_contacts = QLineEdit(Dialog_import)
        self.lineEdit_contacts.setObjectName(u"lineEdit_contacts")
        self.lineEdit_contacts.setEnabled(True)

        self.horizontalLayout_contacts.addWidget(self.lineEdit_contacts)

        self.horizontalLayout_contacts.setStretch(0, 1)
        self.horizontalLayout_contacts.setStretch(1, 6)

        self.verticalLayout.addLayout(self.horizontalLayout_contacts)

        self.horizontalLayout_files = QHBoxLayout()
        self.horizontalLayout_files.setObjectName(u"horizontalLayout_files")
        self.label_files = QLabel(Dialog_import)
        self.label_files.setObjectName(u"label_files")

        self.horizontalLayout_files.addWidget(self.label_files)

        self.pushButton_received_file = QPushButton(Dialog_import)
        self.pushButton_received_file.setObjectName(u"pushButton_received_file")

        self.horizontalLayout_files.addWidget(self.pushButton_received_file)

        self.pushButton_protocol_import = QPushButton(Dialog_import)
        self.pushButton_protocol_import.setObjectName(u"pushButton_protocol_import")

        self.horizontalLayout_files.addWidget(self.pushButton_protocol_import)

        self.pushButton_protocol_identify = QPushButton(Dialog_import)
        self.pushButton_protocol_identify.setObjectName(u"pushButton_protocol_identify")

        self.horizontalLayout_files.addWidget(self.pushButton_protocol_identify)

        self.horizontalLayout_files.setStretch(0, 1)
        self.horizontalLayout_files.setStretch(1, 2)
        self.horizontalLayout_files.setStretch(2, 2)
        self.horizontalLayout_files.setStretch(3, 2)

        self.verticalLayout.addLayout(self.horizontalLayout_files)

        self.horizontalLayout_stat = QHBoxLayout()
        self.horizontalLayout_stat.setObjectName(u"horizontalLayout_stat")
        self.label_stat = QLabel(Dialog_import)
        self.label_stat.setObjectName(u"label_stat")

        self.horizontalLayout_stat.addWidget(self.label_stat)

        self.lineEdit_stat = QLineEdit(Dialog_import)
        self.lineEdit_stat.setObjectName(u"lineEdit_stat")
        self.lineEdit_stat.setEnabled(False)

        self.horizontalLayout_stat.addWidget(self.lineEdit_stat)

        self.horizontalLayout_stat.setStretch(0, 1)
        self.horizontalLayout_stat.setStretch(1, 6)

        self.verticalLayout.addLayout(self.horizontalLayout_stat)

        self.horizontalLayout_status = QHBoxLayout()
        self.horizontalLayout_status.setObjectName(u"horizontalLayout_status")
        self.label_status = QLabel(Dialog_import)
        self.label_status.setObjectName(u"label_status")

        self.horizontalLayout_status.addWidget(self.label_status)

        self.lineEdit_status = QLineEdit(Dialog_import)
        self.lineEdit_status.setObjectName(u"lineEdit_status")
        self.lineEdit_status.setEnabled(False)

        self.horizontalLayout_status.addWidget(self.lineEdit_status)

        self.horizontalLayout_status.setStretch(0, 1)
        self.horizontalLayout_status.setStretch(1, 6)

        self.verticalLayout.addLayout(self.horizontalLayout_status)

        self.horizontalLayout_rows = QHBoxLayout()
        self.horizontalLayout_rows.setObjectName(u"horizontalLayout_rows")
        self.tableView_rows = QTableView(Dialog_import)
        self.tableView_rows.setObjectName(u"tableView_rows")

        self.horizontalLayout_rows.addWidget(self.tableView_rows)


        self.verticalLayout.addLayout(self.horizontalLayout_rows)

        self.horizontalLayout_operations = QHBoxLayout()
        self.horizontalLayout_operations.setObjectName(u"horizontalLayout_operations")
        self.label_operations = QLabel(Dialog_import)
        self.label_operations.setObjectName(u"label_operations")

        self.horizontalLayout_operations.addWidget(self.label_operations)

        self.pushButton_import_delete = QPushButton(Dialog_import)
        self.pushButton_import_delete.setObjectName(u"pushButton_import_delete")

        self.horizontalLayout_operations.addWidget(self.pushButton_import_delete)

        self.pushButton_result_file = QPushButton(Dialog_import)
        self.pushButton_result_file.setObjectName(u"pushButton_result_file")

        self.horizontalLayout_operations.addWidget(self.pushButton_result_file)

        self.pushButton_import_finish = QPushButton(Dialog_import)
        self.pushButton_import_finish.setObjectName(u"pushButton_import_finish")

        self.horizontalLayout_operations.addWidget(self.pushButton_import_finish)

        self.horizontalLayout_operations.setStretch(0, 1)
        self.horizontalLayout_operations.setStretch(1, 2)
        self.horizontalLayout_operations.setStretch(2, 2)
        self.horizontalLayout_operations.setStretch(3, 2)

        self.verticalLayout.addLayout(self.horizontalLayout_operations)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(Dialog_import)

        QMetaObject.connectSlotsByName(Dialog_import)
    # setupUi

    def retranslateUi(self, Dialog_import):
        Dialog_import.setWindowTitle(QCoreApplication.translate("Dialog_import", u"\u0417\u0430\u0433\u0440\u0443\u0436\u0435\u043d\u043d\u044b\u0439 \u0444\u0430\u0439\u043b", None))
        self.label_created_utc.setText(QCoreApplication.translate("Dialog_import", u"\u0414\u0430\u0442\u0430/\u0432\u0440\u0435\u043c\u044f \u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0438", None))
        self.label_reg_num.setText(QCoreApplication.translate("Dialog_import", u"\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u043d\u043e\u043c\u0435\u0440", None))
        self.label_subject.setText(QCoreApplication.translate("Dialog_import", u"\u0421\u0443\u0431\u044a\u0435\u043a\u0442 \u0432\u043e\u0439\u0441\u043a", None))
        self.label_contacts.setText(QCoreApplication.translate("Dialog_import", u"\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u044b \u043e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u0435\u043b\u044f", None))
        self.label_files.setText(QCoreApplication.translate("Dialog_import", u"\u0424\u0430\u0439\u043b\u044b", None))
        self.pushButton_received_file.setText(QCoreApplication.translate("Dialog_import", u"\u041f\u043e\u0441\u0442\u0443\u043f\u0438\u0432\u0448\u0438\u0439 \u0444\u0430\u0439\u043b", None))
        self.pushButton_protocol_import.setText(QCoreApplication.translate("Dialog_import", u"\u041f\u0440\u043e\u0442\u043e\u043a\u043e\u043b \u0438\u043c\u043f\u043e\u0440\u0442\u0430", None))
        self.pushButton_protocol_identify.setText(QCoreApplication.translate("Dialog_import", u"\u041f\u0440\u043e\u0442\u043e\u043a\u043e\u043b \u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u0438", None))
        self.label_stat.setText(QCoreApplication.translate("Dialog_import", u"\u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430", None))
        self.label_status.setText(QCoreApplication.translate("Dialog_import", u"\u0421\u0442\u0430\u0442\u0443\u0441 \u0440\u0430\u0431\u043e\u0442\u044b \u0441 \u0444\u0430\u0439\u043b\u043e\u043c", None))
        self.label_operations.setText(QCoreApplication.translate("Dialog_import", u"\u041e\u043f\u0435\u0440\u0430\u0446\u0438\u0438", None))
        self.pushButton_import_delete.setText(QCoreApplication.translate("Dialog_import", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0443", None))
        self.pushButton_result_file.setText(QCoreApplication.translate("Dialog_import", u"\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0438\u0440\u0443\u044e\u0449\u0438\u0439 \u0444\u0430\u0439\u043b", None))
        self.pushButton_import_finish.setText(QCoreApplication.translate("Dialog_import", u"\u0417\u0430\u0432\u0435\u0440\u0448\u0438\u0442\u044c \u0440\u0430\u0431\u043e\u0442\u0443", None))
    # retranslateUi

