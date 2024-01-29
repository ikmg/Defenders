# пакет handler укладывает полученные данные в БД по правилам, получает сессию от upload,
# работает с моделями данных

from .eskk import EskkGenderHandler, EskkDocumentTypeHandler, EskkMilitaryRankHandler, EskkMilitarySubjectHandler
from .keeper import KeepedReportHandler, KeepedOrderHandler
