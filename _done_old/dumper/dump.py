import csv
from abc import abstractmethod
from datetime import datetime
from uuid import uuid4

from database import PickedLastName, PickedFirstName, PickedMiddleName, PickedSNILS, PickedDocumentSerial, PickedDocumentNumber, PickedDocumentOrganization, PickedAddressIndex, PickedAddressRegion, \
    PickedAddressArea, PickedAddressLocality, PickedAddressStreet, PickedAddressHouse, PickedAddressBuilding, PickedAddressFlat, PickedPersonalNumber, PickedMilitaryRank, PickedMilitarySubject, \
    LinkedPerson, LinkedDocument, LinkedDocumentVBD, LinkedAddress, LinkedOrderFIO, LinkedOrderPerson, LinkedDefender, LinkedOrderPersonPeriod, KeepedOrder, KeepedOrderRecord, KeepedReport, \
    KeepedReportRecord
from tools import string_to_datetime


class Dumper:

    def __init__(self, session, class_name, filepath):
        self.session = session
        self.filepath = filepath
        self.class_name = class_name
        self.dump = None
        self.equals = {
            'military_rank_id': 'eskk_military_rank_id',
            'military_subject_id': 'eskk_military_subject_id',
            'type_id': 'eskk_document_type_id',

            'serial_id': 'picked_serial_id',
            'number_id': 'picked_number_id',
            'organization_id': 'picked_organization_id',

            'index_id': 'picked_index_id',
            'region_id': 'picked_region_id',
            'area_id': 'picked_area_id',
            'locality_id': 'picked_locality_id',
            'street_id': 'picked_street_id',
            'house_id': 'picked_house_id',
            'building_id': 'picked_building_id',
            'room_id': 'picked_flat_id',

            'last_name_id': 'picked_last_name_id',
            'first_name_id': 'picked_first_name_id',
            'middle_name_id': 'picked_middle_name_id',
            'snils_id': 'picked_snils_id',
            'gender_id': 'eskk_gender_id',

            'military_rank_tmp_id': 'picked_military_rank_id',
            'personal_number_id': 'picked_personal_number_id',
            'military_subject_tmp_id': 'picked_military_subject_id',

            'person_id': 'linked_person_id',
            'document_id': 'linked_document_id',
            'document_vbd_id': 'linked_document_vbd_id',
            'reg_address_id': 'linked_reg_address_id',
            'fact_address_id': 'linked_fact_address_id',

            'oshu_order_fio_id': 'linked_order_fio_id',
            'oshu_order_person_id': 'linked_order_person_id',

            'hash': 'hash_sum',
            'file_path': 'instance_filename',
            'contacts': 'contact_info',
            'is_truth': 'is_on_template'
        }
        self.exclude = ['days', 'comment', 'errors']

    def __repr__(self):
        return '<{}> count <{}>'.format(self.filepath, len(self.dump))

    def dump_dict(self):
        result = []
        with open(self.filepath, encoding='utf-8') as csv_file:
            data = csv.reader(csv_file)
            headers = []
            for row_ind, row_val in enumerate(data):
                if row_ind == 0:
                    headers = row_val
                else:
                    dict_row = {}
                    for col_ind, col_val in enumerate(row_val):

                        if headers[col_ind] == 'created_utc':
                            dict_row[headers[col_ind]] = string_to_datetime(col_val)
                        elif headers[col_ind] in self.equals:
                            dict_row[self.equals[headers[col_ind]]] = col_val
                        elif headers[col_ind] in self.exclude:
                            pass
                        else:
                            dict_row[headers[col_ind]] = col_val

                    if 'is_loaded' in dict_row:
                        if dict_row['is_loaded'] == '1':
                            dict_row['is_loaded'] = True
                        else:
                            dict_row['is_loaded'] = False

                    if 'is_on_template' in dict_row:
                        if dict_row['is_on_template'] == '1':
                            dict_row['is_on_template'] = True
                        else:
                            dict_row['is_on_template'] = False

                    result.append(dict_row)
        return result

    def migrate(self):
        self.dump = self.dump_dict()
        for row in self.dump:
            model = self.class_name(**row)
            self.session.add(model)
            self.session.flush()
            model.created_utc = row['created_utc']
            self.session.flush()
        self.session.commit()


class LastNameDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, PickedLastName, filename)
        self.migrate()


class FirstNameDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, PickedFirstName, filename)
        self.migrate()


class MiddleNameDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, PickedMiddleName, filename)
        self.migrate()


class SNILSDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, PickedSNILS, filename)
        self.migrate()


class DocumentSerialDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, PickedDocumentSerial, filename)
        self.migrate()


class DocumentNumberDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, PickedDocumentNumber, filename)
        self.migrate()


class DocumentOrganizationDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, PickedDocumentOrganization, filename)
        self.migrate()


class AddressIndexDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, PickedAddressIndex, filename)
        self.migrate()


class AddressRegionDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, PickedAddressRegion, filename)
        self.migrate()


class AddressAreaDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, PickedAddressArea, filename)
        self.migrate()


class AddressLocalityDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, PickedAddressLocality, filename)
        self.migrate()


class AddressStreetDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, PickedAddressStreet, filename)
        self.migrate()


class AddressHouseDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, PickedAddressHouse, filename)
        self.migrate()


class AddressBuildingDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, PickedAddressBuilding, filename)
        self.migrate()


class AddressFlatDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, PickedAddressFlat, filename)
        self.migrate()


class PersonalNumberDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, PickedPersonalNumber, filename)
        self.migrate()


class MilitaryRankDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, PickedMilitaryRank, filename)
        self.migrate()


class MilitarySubjectDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, PickedMilitarySubject, filename)
        self.migrate()


class PersonDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, LinkedPerson, filename)
        self.migrate()


class DocumentDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, LinkedDocument, filename)
        self.migrate()


class DocumentVBDDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, LinkedDocumentVBD, filename)
        self.migrate()


class AddressVBDDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, LinkedAddress, filename)
        self.migrate()


class OrderFIODumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, LinkedOrderFIO, filename)
        self.migrate()


class OrderPersonDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, LinkedOrderPerson, filename)
        self.migrate()


class OrderPersonPeriodDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, LinkedOrderPersonPeriod, filename)
        self.equals['days'] = 'days_count'
        self.exclude = ['errors', 'oshu_import_id']
        self.migrate()

    def migrate(self):
        self.dump = self.dump_dict()
        for row in self.dump:
            model = self.session.query(LinkedOrderPersonPeriod)
            model = model.filter(LinkedOrderPersonPeriod.linked_order_person_id == row['linked_order_person_id'])
            model = model.filter(LinkedOrderPersonPeriod.date_begin == row['date_begin'])
            model = model.filter(LinkedOrderPersonPeriod.date_end == row['date_end'])
            model = model.scalar()
            if not model:
                model = self.class_name(**row)
                self.session.add(model)
                self.session.flush()
                model.created_utc = row['created_utc']
                self.session.flush()
        self.session.commit()


class OrderDumper:

    def __init__(self, session):
        self.order = KeepedOrder()
        self.order.id = '20231121-104214'
        self.order.created_utc = string_to_datetime('2023-11-21 07:54:06')
        self.order.hash_sum = 'undefined'
        self.order.original_filename = 'Общий.ods'
        self.order.instance_filename = 'storage/orders/20231121-104214.ods'
        self.order.is_on_template = True
        self.order.is_loaded = True
        self.order.note = 'Перенесен при миграции'

        session.add(self.order)
        session.flush()
        self.order.created_utc = string_to_datetime('2023-11-21 07:54:06')
        session.flush()

        self.records = session.query(LinkedOrderPersonPeriod).order_by(LinkedOrderPersonPeriod.created_utc).all()
        for index, record in enumerate(self.records):
            model = KeepedOrderRecord()
            model.id = str(uuid4())
            model.keep_row_num = index + 1
            model.file_row_num = index + 1
            model.warning_messages = ''
            model.critical_messages = ''
            model.keeped_order_id = self.order.id
            model.linked_order_person_period_id = record.id
            session.add(model)

        session.commit()

    def __repr__(self):
        return '<{}> count <{}>'.format(self.order.id, len(self.records))


class ReportDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, KeepedReport, filename)
        self.equals['comment'] = 'note'
        self.exclude = ['is_on_export', 'is_send_sfr', 'is_load_answer', 'is_send_back']
        self.migrate()


class DefenderDumper(Dumper):

    def __init__(self, session, filename):
        super().__init__(session, LinkedDefender, filename)
        # self.exclude = ['defenders_import_id', 'import_row_num', 'document_row_num', 'is_success', 'is_order_identify', 'warning_errors', 'critical_errors', 'result']
        self.migrate()

    def migrate(self):
        self.dump = self.dump_dict()
        for row in self.dump:
            model = self.session.query(LinkedDefender)
            model = model.filter(LinkedDefender.linked_person_id == row['linked_person_id'])
            model = model.filter(LinkedDefender.linked_document_id == row['linked_document_id'])
            model = model.filter(LinkedDefender.linked_document_vbd_id == row['linked_document_vbd_id'])
            model = model.filter(LinkedDefender.linked_reg_address_id == row['linked_reg_address_id'])
            model = model.filter(LinkedDefender.linked_fact_address_id == row['linked_fact_address_id'])
            model = model.filter(LinkedDefender.picked_military_subject_id == row['picked_military_subject_id'])
            model = model.filter(LinkedDefender.picked_personal_number_id == row['picked_personal_number_id'])
            model = model.filter(LinkedDefender.birth_place == row['birth_place'])
            model = model.filter(LinkedDefender.exclude_date == row['exclude_date'])
            model = model.filter(LinkedDefender.exclude_order == row['exclude_order'])
            model = model.filter(LinkedDefender.id_ern == row['id_ern'])
            model = model.scalar()

            record = {
                'id': str(uuid4()),
                'linked_defender_id': model.id if model else row['id'],
                'keeped_report_id': row['defenders_import_id'],
                'keep_row_num': row['import_row_num'],
                'file_row_num': row['document_row_num'],
                'is_find_in_orders': True if row['is_order_identify'] == '1' else False,
                'warning_messages': row['warning_errors'],
                'critical_messages': row['critical_errors'],
                'created_utc': row['created_utc']
            }

            row.pop('defenders_import_id')
            row.pop('import_row_num')
            row.pop('document_row_num')
            row.pop('is_order_identify')
            row.pop('warning_errors')
            row.pop('critical_errors')
            row.pop('is_success')
            row.pop('result')

            if not model:
                model = self.class_name(**row)
                self.session.add(model)
                self.session.flush()
                model.created_utc = row['created_utc']
                self.session.flush()


            model = KeepedReportRecord(**record)
            self.session.add(model)
            self.session.flush()
            model.created_utc = row['created_utc']
            self.session.flush()

        self.session.commit()
