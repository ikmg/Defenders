from .base import BaseWorkbook


class OrderWorkbook(BaseWorkbook):
    """
    Класс получения данных из приказов
    """

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.required_worksheets = ['СПИСОК', 'Моб', 'Территориальные органы']

    def load(self):
        super().load()
        for sheet_name in self.required_worksheets:
            self.select_worksheet(sheet_name)
            self.check_active_worksheet()

    def check_active_worksheet(self):
        """
        Проверка соответствия шаблону
        """
        min_row_count = 4
        min_col_count = 8
        if self.max_row_num < min_row_count:  # минимально допустимое количество строк
            raise ValueError('количество строк меньше {}'.format(min_row_count))
        if len(self.get_row_num_data(1)) < min_col_count:  # минимально допустимое количество столбцов
            raise ValueError('количество столбцов меньше {}'.format(min_col_count))
        for ws_name in self.required_worksheets:
            if ws_name not in self.worksheets_list:
                raise KeyError('отсутствует лист {}'.format(ws_name))

    def worksheet_data(self):
        """
        Установка активного листа по имени и получение его данных
        """
        return self._data_[self.active]
