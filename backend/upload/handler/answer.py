from uuid import uuid4

from database import ProvidedReport, ImportAnswer, InitAnswer
from tools import DTConvert


# from tools.dt import string_to_date, string_to_datetime, date_to_string, datetime_timezone


class AnswerHandler:

    def __init__(self, session, export_id, import_data, init_data):
        self.session = session
        self.export = session.query(ProvidedReport).filter(ProvidedReport.id == export_id).scalar()
        self.import_data = import_data
        self.init_data = init_data

    def check(self):
        print('Проверка протокола идентификации...')
        if self.export and self.import_data and self.init_data:
            for row in self.init_data:
                if row['init_date'].date() < self.import_data['date']:
                    raise ValueError('дата идентификации {} младше даты загрузки {}'.format(
                        row['init_date'].date(), self.import_data['date']
                    ))

            del_list = []
            print('Поиск записей из протокола идентификации в выгруженных записях...')
            for row in self.init_data:
                # print('строка #{}: <{} ({})>...'.format(row['number'], row['fio'], DTConvert(row['birthday']).dstring))
                for record in self.export.provided_report_records:
                    tmp = record.keeped_report_record.linked_defender.linked_person
                    if row['fio'] == tmp.person_appeal and DTConvert(row['birthday']).dstring == DTConvert(tmp.birthday).dstring:  # должна быть дата
                        if record.id not in del_list:
                            row['provided_report_record_id'] = record.id
                            del_list.append(record.id)
                            print('\tid <{}>: <{} ({})>'.format(record.id, tmp.person_appeal, DTConvert(tmp.birthday).dstring))
                            break
                print('\033[{}mстрока #{}: <{} ({})> - {}\033[0m'.format(
                    32 if row['provided_report_record_id'] else 31,
                    row['number'],
                    row['fio'],
                    DTConvert(row['birthday']).dstring,
                    'успешно' if row['provided_report_record_id'] else 'ошибка'
                ))

            export_errors_list = []
            for row in self.init_data:
                if not row['provided_report_record_id']:
                    export_errors_list.append('{} ({} г.р.)'.format(row['fio'], DTConvert(row['birthday']).dstring))
                    # raise ValueError('персона {} ({} г.р.) не выгружалась'.format(row['fio'], DTConvert(row['birthday']).dstring))

            init_errors_list = []
            for record in self.export.provided_report_records:
                is_found = False
                for row in self.init_data:
                    if record.id == row['provided_report_record_id']:
                        is_found = True
                if not is_found:
                    init_errors_list.append('{} ({} г.р.)'.format(
                        record.keeped_report_record.linked_defender.linked_person.person_appeal,
                        record.keeped_report_record.linked_defender.linked_person.birthday
                    ))
                    # raise ValueError('персона {} ({} г.р.) отсутствует в протоколе идентификации'.format(
                    #     record.keeped_report_record.linked_defender.linked_person.person_appeal,
                    #     record.keeped_report_record.linked_defender.linked_person.birthday
                    # ))

            if export_errors_list or init_errors_list:
                error_message = ''
                if export_errors_list:
                    export_message = 'Не выгружались (присутствуют в протоколе):\n{}'.format('\n'.join(export_errors_list))
                    error_message = '{}\n\n{}'.format(error_message, export_message)
                if init_errors_list:
                    init_message = 'Выгружались (отсутствуют в протоколе):\n{}'.format('\n'.join(init_errors_list))
                    error_message = '{}\n\n{}'.format(error_message, init_message)
                raise ValueError(error_message)

        else:
            raise ValueError('произошло что-то непонятное')

    def save(self):
        answer_import = ImportAnswer()
        answer_import.id = str(uuid4())
        answer_import.created_utc = DTConvert().datetime  # должно быть дата/время с часовым поясом
        answer_import.provided_report_id = self.export.id
        answer_import.import_date = self.import_data['date']
        answer_import.reg_number = self.import_data['reg_num']
        answer_import.user = self.import_data['user']
        answer_import.result = self.import_data['result']
        self.session.add(answer_import)
        self.session.flush()

        for row in self.init_data:
            answer_init = self.session.query(InitAnswer).filter(InitAnswer.provided_report_record_id == row['provided_report_record_id']).scalar()
            if answer_init:
                raise ValueError('протокол идентификации на {} уже загружен'.format(row['provided_report_record_id']))
            else:
                answer_init = InitAnswer()
                answer_init.id = str(uuid4())
                answer_init.created_utc = DTConvert().datetime  # должно быть дата/время с часовым поясом
                answer_init.provided_report_record_id = row['provided_report_record_id']
                answer_init.init_date = row['init_date']
                answer_init.number = row['number']
                answer_init.status = row['status']
                answer_init.comment = row['comment']
                self.session.add(answer_init)
                self.session.flush()

    def update(self):
        answer_import = self.session.query(ImportAnswer).filter(ImportAnswer.provided_report_id == self.export.id).scalar()
        answer_import.created_utc = DTConvert().datetime  # должно быть дата/время с часовым поясом
        answer_import.import_date = self.import_data['date']
        answer_import.reg_number = self.import_data['reg_num']
        answer_import.user = self.import_data['user']
        answer_import.result = self.import_data['result']
        self.session.flush()

        for row in self.init_data:
            answer_init = self.session.query(InitAnswer).filter(InitAnswer.provided_report_record_id == row['provided_report_record_id']).scalar()
            answer_init.created_utc = DTConvert().datetime  # должно быть дата/время с часовым поясом
            # answer_init.provided_report_record_id = row['provided_report_record_id']
            answer_init.init_date = row['init_date']
            answer_init.number = row['number']
            answer_init.status = row['status']
            answer_init.comment = row['comment']
            self.session.flush()
