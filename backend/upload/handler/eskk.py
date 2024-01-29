from database import EskkGender, EskkDocumentType, EskkMilitaryRank, EskkMilitarySubject
from .base import BaseHandler


class EskkHandler(BaseHandler):

    def __init__(self, session, class_model, **keywords):
        super().__init__(session, class_model)
        # данные для модели
        self.id = keywords['id']
        self.name = keywords['name']
        self.sort = keywords['sort']

    def _find_(self):
        # ищем модель по id
        model = self._session_.query(self._class_name_).filter(
            self._class_name_.id == self.id
        ).scalar()
        # если модель найдена
        if model:
            # отмечаем признак существования данных
            self.is_already_exists = True
            # забираем из модели created_utc
            self.created_utc = model.created_utc
            # пытаемся обновить значения модели name и sort в случае расхождений
            model.name = self.name
            model.sort = self.sort
            # синхронизируем состояние данных
            self._session_.flush()

    def get_model(self):
        """
        Создает модель данных в случае если она еще не присутствует в базе, добавляет ее и синхронизирует состояние
        """
        self._find_()
        if not self.is_already_exists:
            self.model = self._class_name_()
            self.model.id = self.id
            self.model.created_utc = self.created_utc
            self.model.name = self.name
            self.model.sort = self.sort
            self._session_.add(self.model)
            self._session_.flush()

    def check(self):
        """Не используется"""
        pass


class EskkGenderHandler(EskkHandler):

    def __init__(self, session, **keywords):
        super().__init__(session, EskkGender, **keywords)
        self.check()
        self.get_model()


class EskkDocumentTypeHandler(EskkHandler):

    def __init__(self, session, **keywords):
        super().__init__(session, EskkDocumentType, **keywords)
        self.check()
        self.get_model()


class EskkMilitaryRankHandler(EskkHandler):

    def __init__(self, session, **keywords):
        super().__init__(session, EskkMilitaryRank, **keywords)
        self.check()
        self.get_model()


class EskkMilitarySubjectHandler(EskkHandler):

    def __init__(self, session, **keywords):
        super().__init__(session, EskkMilitarySubject, **keywords)
        # данные для модели
        self.parent_id = keywords['parent_id']
        self.path = keywords['path']
        self.short_name = keywords['short_name']
        self.conditional_name = keywords['conditional_name']
        self.conditional_short_name = keywords['conditional_short_name']
        self.get_model()
        self.check()

    def check(self):
        if self.id == '1':
            model = self._session_.query(EskkMilitarySubject).filter(
                EskkMilitarySubject.id == '1'
            ).scalar()
            if model and model.parent_id != '0':
                model.parent_id = '0'
                self._session_.flush()

    def _find_(self):
        # ищем модель по id
        model = self._session_.query(self._class_name_).filter(
            self._class_name_.id == self.id
        ).scalar()
        # если модель найдена
        if model:
            # отмечаем признак существования данных
            self.is_already_exists = True
            # забираем из модели created_utc
            self.created_utc = model.created_utc
            # пытаемся обновить значения модели в случае расхождений
            model.parent_id = self.parent_id
            model.path = self.path
            model.sort = self.sort
            model.name = self.name
            model.short_name = self.short_name
            model.conditional_name = self.conditional_name
            model.conditional_short_name = self.conditional_short_name
            # синхронизируем состояние данных
            self._session_.flush()

    def get_model(self):
        """
        Создает модель данных в случае если она еще не присутствует в базе, добавляет ее и синхронизирует состояние
        """
        self._find_()
        if not self.is_already_exists:
            model = self._class_name_()
            # model = EskkMilitarySubject()
            model.id = self.id
            model.created_utc = self.created_utc
            model.parent_id = self.parent_id
            model.path = self.path
            model.sort = self.sort
            model.name = self.name
            model.short_name = self.short_name
            model.conditional_name = self.conditional_name
            model.conditional_short_name = self.conditional_short_name
            self._session_.add(model)
            self._session_.flush()
