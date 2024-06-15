# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windowpjpHQo.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1024, 768)
        MainWindow.setMinimumSize(QSize(1024, 768))
        MainWindow.setMaximumSize(QSize(3840, 2160))
        MainWindow.setToolButtonStyle(Qt.ToolButtonIconOnly)
        MainWindow.setTabShape(QTabWidget.Rounded)
        MainWindow.setDockOptions(QMainWindow.AllowTabbedDocks|QMainWindow.AnimatedDocks)
        self.action_load_orders = QAction(MainWindow)
        self.action_load_orders.setObjectName(u"action_load_orders")
        self.action_information = QAction(MainWindow)
        self.action_information.setObjectName(u"action_information")
        self.action_storage_imports = QAction(MainWindow)
        self.action_storage_imports.setObjectName(u"action_storage_imports")
        self.action_storage_exports = QAction(MainWindow)
        self.action_storage_exports.setObjectName(u"action_storage_exports")
        self.action_storage_answers = QAction(MainWindow)
        self.action_storage_answers.setObjectName(u"action_storage_answers")
        self.action_storage_orders = QAction(MainWindow)
        self.action_storage_orders.setObjectName(u"action_storage_orders")
        self.action_clear_storage = QAction(MainWindow)
        self.action_clear_storage.setObjectName(u"action_clear_storage")
        self.action_exit = QAction(MainWindow)
        self.action_exit.setObjectName(u"action_exit")
        self.action_eskk_genders = QAction(MainWindow)
        self.action_eskk_genders.setObjectName(u"action_eskk_genders")
        self.action_eskk_doc_types = QAction(MainWindow)
        self.action_eskk_doc_types.setObjectName(u"action_eskk_doc_types")
        self.action_eskk_ranks = QAction(MainWindow)
        self.action_eskk_ranks.setObjectName(u"action_eskk_ranks")
        self.action_eskk_subjects = QAction(MainWindow)
        self.action_eskk_subjects.setObjectName(u"action_eskk_subjects")
        self.action_eskk_all = QAction(MainWindow)
        self.action_eskk_all.setObjectName(u"action_eskk_all")
        self.action_vacuum_db = QAction(MainWindow)
        self.action_vacuum_db.setObjectName(u"action_vacuum_db")
        self.action_storage_stat = QAction(MainWindow)
        self.action_storage_stat.setObjectName(u"action_storage_stat")
        self.action_storage = QAction(MainWindow)
        self.action_storage.setObjectName(u"action_storage")
        self.action_sfr_control = QAction(MainWindow)
        self.action_sfr_control.setObjectName(u"action_sfr_control")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tab_statistic = QWidget()
        self.tab_statistic.setObjectName(u"tab_statistic")
        self.gridLayout_7 = QGridLayout(self.tab_statistic)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.comboBox_select_statistic = QComboBox(self.tab_statistic)
        self.comboBox_select_statistic.setObjectName(u"comboBox_select_statistic")

        self.horizontalLayout_2.addWidget(self.comboBox_select_statistic)

        self.pushButton_refresh_statistic = QPushButton(self.tab_statistic)
        self.pushButton_refresh_statistic.setObjectName(u"pushButton_refresh_statistic")

        self.horizontalLayout_2.addWidget(self.pushButton_refresh_statistic)

        self.horizontalLayout_2.setStretch(0, 5)
        self.horizontalLayout_2.setStretch(1, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.tableView_statistic_data = QTableView(self.tab_statistic)
        self.tableView_statistic_data.setObjectName(u"tableView_statistic_data")
        self.tableView_statistic_data.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView_statistic_data.setSortingEnabled(True)
        self.tableView_statistic_data.horizontalHeader().setProperty("showSortIndicator", True)
        self.tableView_statistic_data.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_4.addWidget(self.tableView_statistic_data)

        self.pushButton_save_statistic = QPushButton(self.tab_statistic)
        self.pushButton_save_statistic.setObjectName(u"pushButton_save_statistic")

        self.verticalLayout_4.addWidget(self.pushButton_save_statistic)


        self.gridLayout_7.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_statistic, "")
        self.tab_imports = QWidget()
        self.tab_imports.setObjectName(u"tab_imports")
        self.gridLayout_2 = QGridLayout(self.tab_imports)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_import_workbook = QLabel(self.tab_imports)
        self.label_import_workbook.setObjectName(u"label_import_workbook")

        self.horizontalLayout_8.addWidget(self.label_import_workbook)

        self.lineEdit_import_filename = QLineEdit(self.tab_imports)
        self.lineEdit_import_filename.setObjectName(u"lineEdit_import_filename")
        self.lineEdit_import_filename.setEnabled(False)

        self.horizontalLayout_8.addWidget(self.lineEdit_import_filename)

        self.pushButton_select_import_file = QPushButton(self.tab_imports)
        self.pushButton_select_import_file.setObjectName(u"pushButton_select_import_file")

        self.horizontalLayout_8.addWidget(self.pushButton_select_import_file)

        self.horizontalLayout_8.setStretch(0, 1)
        self.horizontalLayout_8.setStretch(1, 8)
        self.horizontalLayout_8.setStretch(2, 1)

        self.gridLayout_2.addLayout(self.horizontalLayout_8, 1, 0, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_import_subject = QLabel(self.tab_imports)
        self.label_import_subject.setObjectName(u"label_import_subject")

        self.horizontalLayout_7.addWidget(self.label_import_subject)

        self.comboBox_select_import_subject = QComboBox(self.tab_imports)
        self.comboBox_select_import_subject.setObjectName(u"comboBox_select_import_subject")
        self.comboBox_select_import_subject.setMaxVisibleItems(30)
        self.comboBox_select_import_subject.setInsertPolicy(QComboBox.NoInsert)

        self.horizontalLayout_7.addWidget(self.comboBox_select_import_subject)

        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 9)

        self.gridLayout_2.addLayout(self.horizontalLayout_7, 0, 0, 1, 1)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_import_worksheet = QLabel(self.tab_imports)
        self.label_import_worksheet.setObjectName(u"label_import_worksheet")

        self.horizontalLayout_9.addWidget(self.label_import_worksheet)

        self.comboBox_import_worksheet = QComboBox(self.tab_imports)
        self.comboBox_import_worksheet.setObjectName(u"comboBox_import_worksheet")

        self.horizontalLayout_9.addWidget(self.comboBox_import_worksheet)

        self.horizontalLayout_9.setStretch(0, 1)
        self.horizontalLayout_9.setStretch(1, 9)

        self.gridLayout_2.addLayout(self.horizontalLayout_9, 2, 0, 1, 1)

        self.verticalLayout_imports = QVBoxLayout()
        self.verticalLayout_imports.setObjectName(u"verticalLayout_imports")
        self.tableView_imports = QTableView(self.tab_imports)
        self.tableView_imports.setObjectName(u"tableView_imports")
        self.tableView_imports.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView_imports.setSortingEnabled(True)
        self.tableView_imports.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_imports.addWidget(self.tableView_imports)


        self.gridLayout_2.addLayout(self.verticalLayout_imports, 5, 0, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_contacts = QLabel(self.tab_imports)
        self.label_contacts.setObjectName(u"label_contacts")

        self.horizontalLayout_11.addWidget(self.label_contacts)

        self.lineEdit_contacts = QLineEdit(self.tab_imports)
        self.lineEdit_contacts.setObjectName(u"lineEdit_contacts")

        self.horizontalLayout_11.addWidget(self.lineEdit_contacts)

        self.horizontalLayout_11.setStretch(0, 1)
        self.horizontalLayout_11.setStretch(1, 9)

        self.gridLayout_2.addLayout(self.horizontalLayout_11, 3, 0, 1, 1)

        self.pushButton_load_import = QPushButton(self.tab_imports)
        self.pushButton_load_import.setObjectName(u"pushButton_load_import")

        self.gridLayout_2.addWidget(self.pushButton_load_import, 4, 0, 1, 1)

        self.tabWidget.addTab(self.tab_imports, "")
        self.tab_exports = QWidget()
        self.tab_exports.setObjectName(u"tab_exports")
        self.gridLayout_8 = QGridLayout(self.tab_exports)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.pushButton_export_data = QPushButton(self.tab_exports)
        self.pushButton_export_data.setObjectName(u"pushButton_export_data")

        self.verticalLayout_6.addWidget(self.pushButton_export_data)

        self.tableView_exports = QTableView(self.tab_exports)
        self.tableView_exports.setObjectName(u"tableView_exports")
        self.tableView_exports.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView_exports.setSortingEnabled(True)
        self.tableView_exports.horizontalHeader().setProperty("showSortIndicator", True)
        self.tableView_exports.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_6.addWidget(self.tableView_exports)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_export_id = QLabel(self.tab_exports)
        self.label_export_id.setObjectName(u"label_export_id")

        self.horizontalLayout.addWidget(self.label_export_id)

        self.lineEdit_export_id = QLineEdit(self.tab_exports)
        self.lineEdit_export_id.setObjectName(u"lineEdit_export_id")
        self.lineEdit_export_id.setEnabled(False)

        self.horizontalLayout.addWidget(self.lineEdit_export_id)

        self.pushButton_answer_cancel = QPushButton(self.tab_exports)
        self.pushButton_answer_cancel.setObjectName(u"pushButton_answer_cancel")

        self.horizontalLayout.addWidget(self.pushButton_answer_cancel)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 8)
        self.horizontalLayout.setStretch(2, 1)

        self.verticalLayout_6.addLayout(self.horizontalLayout)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setSpacing(6)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_answer_import = QLabel(self.tab_exports)
        self.label_answer_import.setObjectName(u"label_answer_import")

        self.horizontalLayout_14.addWidget(self.label_answer_import)

        self.lineEdit_answer_import_filename = QLineEdit(self.tab_exports)
        self.lineEdit_answer_import_filename.setObjectName(u"lineEdit_answer_import_filename")
        self.lineEdit_answer_import_filename.setEnabled(False)

        self.horizontalLayout_14.addWidget(self.lineEdit_answer_import_filename)

        self.pushButton_select_answer_import = QPushButton(self.tab_exports)
        self.pushButton_select_answer_import.setObjectName(u"pushButton_select_answer_import")

        self.horizontalLayout_14.addWidget(self.pushButton_select_answer_import)

        self.horizontalLayout_14.setStretch(0, 2)
        self.horizontalLayout_14.setStretch(1, 8)
        self.horizontalLayout_14.setStretch(2, 1)

        self.verticalLayout_6.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setSpacing(6)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_answer_init = QLabel(self.tab_exports)
        self.label_answer_init.setObjectName(u"label_answer_init")

        self.horizontalLayout_12.addWidget(self.label_answer_init)

        self.lineEdit_answer_init_filename = QLineEdit(self.tab_exports)
        self.lineEdit_answer_init_filename.setObjectName(u"lineEdit_answer_init_filename")
        self.lineEdit_answer_init_filename.setEnabled(False)

        self.horizontalLayout_12.addWidget(self.lineEdit_answer_init_filename)

        self.pushButton_select_answer_init = QPushButton(self.tab_exports)
        self.pushButton_select_answer_init.setObjectName(u"pushButton_select_answer_init")

        self.horizontalLayout_12.addWidget(self.pushButton_select_answer_init)

        self.horizontalLayout_12.setStretch(0, 2)
        self.horizontalLayout_12.setStretch(1, 8)
        self.horizontalLayout_12.setStretch(2, 1)

        self.verticalLayout_6.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.pushButton_load_answers = QPushButton(self.tab_exports)
        self.pushButton_load_answers.setObjectName(u"pushButton_load_answers")

        self.horizontalLayout_18.addWidget(self.pushButton_load_answers)


        self.verticalLayout_6.addLayout(self.horizontalLayout_18)


        self.gridLayout_8.addLayout(self.verticalLayout_6, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_exports, "")
        self.tab_defenders = QWidget()
        self.tab_defenders.setObjectName(u"tab_defenders")
        self.gridLayout_4 = QGridLayout(self.tab_defenders)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_find_defender = QLabel(self.tab_defenders)
        self.label_find_defender.setObjectName(u"label_find_defender")

        self.horizontalLayout_3.addWidget(self.label_find_defender)

        self.lineEdit_find_defender = QLineEdit(self.tab_defenders)
        self.lineEdit_find_defender.setObjectName(u"lineEdit_find_defender")

        self.horizontalLayout_3.addWidget(self.lineEdit_find_defender)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.tableView_defenders = QTableView(self.tab_defenders)
        self.tableView_defenders.setObjectName(u"tableView_defenders")
        self.tableView_defenders.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView_defenders.setSortingEnabled(True)
        self.tableView_defenders.horizontalHeader().setProperty("showSortIndicator", True)
        self.tableView_defenders.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_2.addWidget(self.tableView_defenders)


        self.gridLayout_4.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_defenders, "")
        self.tab_svo = QWidget()
        self.tab_svo.setObjectName(u"tab_svo")
        self.gridLayout_5 = QGridLayout(self.tab_svo)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_find_participant = QLabel(self.tab_svo)
        self.label_find_participant.setObjectName(u"label_find_participant")

        self.horizontalLayout_4.addWidget(self.label_find_participant)

        self.lineEdit_find_order_person = QLineEdit(self.tab_svo)
        self.lineEdit_find_order_person.setObjectName(u"lineEdit_find_order_person")

        self.horizontalLayout_4.addWidget(self.lineEdit_find_order_person)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.tableView_order_persons = QTableView(self.tab_svo)
        self.tableView_order_persons.setObjectName(u"tableView_order_persons")
        self.tableView_order_persons.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView_order_persons.setSortingEnabled(True)
        self.tableView_order_persons.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout_3.addWidget(self.tableView_order_persons)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_order = QLabel(self.tab_svo)
        self.label_order.setObjectName(u"label_order")

        self.horizontalLayout_10.addWidget(self.label_order)

        self.lineEdit_order_filename = QLineEdit(self.tab_svo)
        self.lineEdit_order_filename.setObjectName(u"lineEdit_order_filename")
        self.lineEdit_order_filename.setEnabled(False)

        self.horizontalLayout_10.addWidget(self.lineEdit_order_filename)

        self.pushButton_select_order_file = QPushButton(self.tab_svo)
        self.pushButton_select_order_file.setObjectName(u"pushButton_select_order_file")

        self.horizontalLayout_10.addWidget(self.pushButton_select_order_file)

        self.horizontalLayout_10.setStretch(0, 1)
        self.horizontalLayout_10.setStretch(1, 8)
        self.horizontalLayout_10.setStretch(2, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_10)

        self.pushButton_load_orders = QPushButton(self.tab_svo)
        self.pushButton_load_orders.setObjectName(u"pushButton_load_orders")

        self.verticalLayout_3.addWidget(self.pushButton_load_orders)


        self.gridLayout_5.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_svo, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1024, 22))
        self.menu_main = QMenu(self.menubar)
        self.menu_main.setObjectName(u"menu_main")
        self.menu_storage = QMenu(self.menubar)
        self.menu_storage.setObjectName(u"menu_storage")
        self.menu_catalogs = QMenu(self.menu_storage)
        self.menu_catalogs.setObjectName(u"menu_catalogs")
        self.menu_eskk = QMenu(self.menu_storage)
        self.menu_eskk.setObjectName(u"menu_eskk")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menu_main.menuAction())
        self.menubar.addAction(self.menu_storage.menuAction())
        self.menu_main.addAction(self.action_sfr_control)
        self.menu_main.addAction(self.action_exit)
        self.menu_storage.addAction(self.menu_catalogs.menuAction())
        self.menu_storage.addAction(self.menu_eskk.menuAction())
        self.menu_storage.addAction(self.action_clear_storage)
        self.menu_storage.addAction(self.action_vacuum_db)
        self.menu_catalogs.addAction(self.action_storage_imports)
        self.menu_catalogs.addAction(self.action_storage_exports)
        self.menu_catalogs.addAction(self.action_storage_answers)
        self.menu_catalogs.addAction(self.action_storage_orders)
        self.menu_catalogs.addAction(self.action_storage_stat)
        self.menu_catalogs.addSeparator()
        self.menu_catalogs.addAction(self.action_storage)
        self.menu_eskk.addAction(self.action_eskk_genders)
        self.menu_eskk.addAction(self.action_eskk_doc_types)
        self.menu_eskk.addAction(self.action_eskk_ranks)
        self.menu_eskk.addAction(self.action_eskk_subjects)
        self.menu_eskk.addSeparator()
        self.menu_eskk.addAction(self.action_eskk_all)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0449\u0438\u0442\u043d\u0438\u043a\u0438 \u041e\u0442\u0435\u0447\u0435\u0441\u0442\u0432\u0430", None))
        self.action_load_orders.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0434\u0430\u043d\u043d\u044b\u0435 \u0438\u0437 \u041e\u0428\u0423 \u0420\u043e\u0441\u0433\u0432\u0430\u0440\u0434\u0438\u0438", None))
        self.action_information.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f", None))
        self.action_storage_imports.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u043a\u0438", None))
        self.action_storage_exports.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0433\u0440\u0443\u0437\u043a\u0438", None))
        self.action_storage_answers.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0432\u0435\u0442\u044b", None))
        self.action_storage_orders.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0438\u043a\u0430\u0437\u044b", None))
        self.action_clear_storage.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0447\u0438\u0441\u0442\u0438\u0442\u044c \u0445\u0440\u0430\u043d\u0438\u043b\u0438\u0449\u0435", None))
        self.action_exit.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0445\u043e\u0434", None))
        self.action_eskk_genders.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043b", None))
        self.action_eskk_doc_types.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0438\u043f\u044b \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u043e\u0432", None))
        self.action_eskk_ranks.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0432\u0430\u043d\u0438\u044f", None))
        self.action_eskk_subjects.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0443\u0431\u044a\u0435\u043a\u0442\u044b", None))
        self.action_eskk_all.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0441\u0435", None))
        self.action_vacuum_db.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0436\u0430\u0442\u044c \u0431\u0430\u0437\u0443 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.action_storage_stat.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430", None))
        self.action_storage.setText(QCoreApplication.translate("MainWindow", u"\u0425\u0440\u0430\u043d\u0438\u043b\u0438\u0449\u0435", None))
        self.action_sfr_control.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0432\u0435\u0440\u043a\u0430 \u0441 \u0421\u0424\u0420", None))
        self.pushButton_refresh_statistic.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c", None))
        self.pushButton_save_statistic.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_statistic), QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430", None))
        self.label_import_workbook.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043d\u0438\u0433\u0430", None))
        self.pushButton_select_import_file.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c", None))
        self.label_import_subject.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0443\u0431\u044a\u0435\u043a\u0442", None))
        self.label_import_worksheet.setText(QCoreApplication.translate("MainWindow", u"\u041b\u0438\u0441\u0442", None))
        self.label_contacts.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u044b", None))
        self.pushButton_load_import.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0444\u0430\u0439\u043b", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_imports), QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u043a\u0438", None))
        self.pushButton_export_data.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0441\u0432\u0435\u0434\u0435\u043d\u0438\u044f \u0432 \u0421\u043e\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u0439 \u0424\u043e\u043d\u0434 \u0420\u043e\u0441\u0441\u0438\u0438", None))
        self.label_export_id.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0432\u0435\u0442 \u0434\u043b\u044f \u0432\u044b\u0433\u0440\u0443\u0437\u043a\u0438", None))
        self.pushButton_answer_cancel.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.label_answer_import.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0442\u043e\u043a\u043e\u043b \u0437\u0430\u0433\u0440\u0443\u0437\u043a\u0438", None))
        self.pushButton_select_answer_import.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c", None))
        self.label_answer_init.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0442\u043e\u043a\u043e\u043b \u0438\u0434\u0435\u043d\u0442\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u0438", None))
        self.pushButton_select_answer_init.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c", None))
        self.pushButton_load_answers.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u043f\u0440\u043e\u0442\u043e\u043a\u043e\u043b\u044b", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_exports), QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0433\u0440\u0443\u0437\u043a\u0438", None))
        self.label_find_defender.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0438\u0441\u043a:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_defenders), QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0449\u0438\u0442\u043d\u0438\u043a\u0438", None))
        self.label_find_participant.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0438\u0441\u043a:", None))
        self.label_order.setText(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b", None))
        self.pushButton_select_order_file.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c", None))
        self.pushButton_load_orders.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0434\u0430\u043d\u043d\u044b\u0435 \u043e\u0431 \u0443\u0447\u0430\u0441\u0442\u043d\u0438\u043a\u0430\u0445", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_svo), QCoreApplication.translate("MainWindow", u"\u0423\u0447\u0430\u0441\u0442\u043d\u0438\u043a\u0438", None))
        self.menu_main.setTitle(QCoreApplication.translate("MainWindow", u"\u041c\u0435\u043d\u044e", None))
        self.menu_storage.setTitle(QCoreApplication.translate("MainWindow", u"\u0425\u0440\u0430\u043d\u0438\u043b\u0438\u0449\u0435", None))
        self.menu_catalogs.setTitle(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u043a\u0430\u0442\u0430\u043b\u043e\u0433...", None))
        self.menu_eskk.setTitle(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c \u0441\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0438...", None))
    # retranslateUi

