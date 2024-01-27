from database import EskkMilitarySubject
from modules.receiver import EskkGenderHandler, EskkDocumentTypeHandler, EskkMilitaryRankHandler, EskkMilitarySubjectHandler


class EskkLoader:
    """Обновление справочников базы данных"""

    def __init__(self, session):
        self.session = session

    def update_genders(self, data_list):
        """Обновление справочника гендеров"""
        for row in data_list:
            EskkGenderHandler(self.session, **row)
        # фиксируем состояние базы данных
        self.session.commit()

    def update_document_types(self, data_list):
        """Обновление справочника типов документов"""
        for row in data_list:
            EskkDocumentTypeHandler(self.session, **row)
        # фиксируем состояние базы данных
        self.session.commit()

    def update_military_ranks(self, data_list):
        """Обновление справочника званий"""
        for row in data_list:
            EskkMilitaryRankHandler(self.session, **row)
        # фиксируем состояние базы данных
        self.session.commit()

    def update_military_subjects(self, data_list):
        """Обновление справочника субъектов"""
        for row in data_list:
            EskkMilitarySubjectHandler(self.session, **row)
        # обновляем запись для корневого элемента
        model = self.session.query(EskkMilitarySubject).filter(
            EskkMilitarySubject.id == '1'
        ).scalar()
        if model and model.parent_id != '0':
            model.parent_id = '0'
            self.session.flush()
        # фиксируем состояние базы данных
        self.session.commit()
