from tools.date_and_time import datetime_timezone
from ._workbook_ import WorkBook


class DefendersWorkbook(WorkBook):
    """
    Класс загрузки файлов из субъектов войск об уволенных участниках СВО
    """

    def __init__(self, **keywords):
        super().__init__(**keywords)
        self.subject_id = str(keywords['subject_id'])
        self.import_id = '{}-{}'.format(
            self.subject_id.zfill(4),
            datetime_timezone().strftime('%Y%m%d-%H%M%S')
        )

    def check(self):
        """
        Реализация абстрактного метода проверки структуры книги
        :return: bool
        """
        self._add_to_log_('Проверка: <{}>'.format(self.filename))
        required = 'Лист1'  # наименование листа с данными
        # if required not in self.worksheets_list:
        #     self._add_to_log_(
        #         'Ошибка проверки: структура книги не соответствует заданному шаблону ({} not present in {})'.format(
        #             required,
        #             self.worksheets_list
        #         )
        #     )
        #     return False
        # else:

        # Для проверки берется вторая строка с данными
        second_row = self.get_worksheet_data(required)[1]
        # должно быть не менее 37 столбцов
        columns_count = len(second_row)
        if columns_count < 37:
            self._add_to_log_(
                'Ошибка проверки: количество столбцов должно быть не меньше 37, сейчас <{}>'.format(
                    columns_count
                )
            )
            return False
        # Значение в ячейках с 1 по 37 должно быть равно индексу столбца + 1
        for column_index, column_value in enumerate(second_row[:37]):
            if column_index + 1 != column_value:
                self._add_to_log_(
                    'Ошибка проверки: индекс столбца {} не соответствует значению <{}>'.format(
                        column_index + 1,
                        column_value
                    )
                )
                return False
        # успешная проверка
        return True

    def get_defenders_worksheet_data(self):
        """
        Запрос данных о Защитниках Отечества
        :return: [[], [], ...]
        """
        return self.get_worksheet_data('Лист1')
