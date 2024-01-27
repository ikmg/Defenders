from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from . import BaseModel


class PickerModel(BaseModel):
    """
    Жадные сборщики данных...
    Абстрактная модель сборщика поставляемых значений. Пикеры собирают любые значения и хранят их в текстовом формате.
    Первичным ключом пикера является значение (value). Основной задачей пикеров является хранение уникальных значений
    для использования в других таблицах базы данных. Пикеры являются своего рода справочниками человеческой глупости.
    С помощью пикера по реляционным связям можно быстро анализировать повторное использование важных значений.
    """
    __abstract__ = True

    value = Column(String, primary_key=True, nullable=False, index=True, doc='Значение, первичный ключ')

    def __repr__(self):
        return 'value <{}>, id <{}>'.format(
            self.value,
            self.id
        )


# Пикеры персональных данных


class PickedSNILS(PickerModel):
    """Пикер СИНЛСов"""
    __tablename__ = 'picked_snilses'


class PickedLastName(PickerModel):
    """Пикер фамилий"""
    __tablename__ = 'picked_last_names'


class PickedFirstName(PickerModel):
    """Пикер имен"""
    __tablename__ = 'picked_first_names'


class PickedMiddleName(PickerModel):
    """Пикер отчеств"""
    __tablename__ = 'picked_middle_names'


# Пикеры реквизитов документов


class PickedDocumentSerial(PickerModel):
    """Пикер серий документов"""
    __tablename__ = 'picked_document_serials'


class PickedDocumentNumber(PickerModel):
    """Пикер номеров документов"""
    __tablename__ = 'picked_document_numbers'


class PickedDocumentOrganization(PickerModel):
    """Пикер организаций, выдавших документы"""
    __tablename__ = 'picked_document_organizations'


# Пикеры составных частей адреса


class PickedAddressIndex(PickerModel):
    """Пикер адресных индексов"""
    __tablename__ = 'picked_address_indexes'


class PickedAddressRegion(PickerModel):
    """Пикер наименований регионов"""
    __tablename__ = 'picked_address_regions'


class PickedAddressArea(PickerModel):
    """Пикер наименований районов"""
    __tablename__ = 'picked_address_areas'


class PickedAddressLocality(PickerModel):
    """Пикер наименований населенных пунктов"""
    __tablename__ = 'picked_address_localities'


class PickedAddressStreet(PickerModel):
    """Пикер наименований улиц"""
    __tablename__ = 'picked_address_streets'


class PickedAddressHouse(PickerModel):
    """Пикер домов"""
    __tablename__ = 'picked_address_houses'


class PickedAddressBuilding(PickerModel):
    """Пикер строений и корпусов"""
    __tablename__ = 'picked_address_buildings'


class PickedAddressFlat(PickerModel):
    """Пикер квартир"""
    __tablename__ = 'picked_address_flats'


# Пикеры военной составляющей информации


class PickedPersonalNumber(PickerModel):
    """Пикер личных номеров"""
    __tablename__ = 'picked_personal_numbers'


class PickedMilitaryRank(PickerModel):
    """
    Пикер наименований воинских (специальных) званий.
    Обладает реляционной связью с классификатором званий для установки соответствия.
    """
    __tablename__ = 'picked_military_ranks'
    eskk_military_rank_id = Column(String, ForeignKey('eskk_military_ranks.id', ondelete='CASCADE'), nullable=True)
    eskk_military_rank = relationship('EskkMilitaryRank', uselist=False, lazy=True)


class PickedMilitarySubject(PickerModel):
    """
    Пикер наименований субъектов войск.
    Обладает реляционной связью с классификатором субъектов для установки соответствия.
    """
    __tablename__ = 'picked_military_subjects'
    eskk_military_subject_id = Column(String, ForeignKey('eskk_military_subjects.id', ondelete='CASCADE'), nullable=True)
    eskk_military_subject = relationship('EskkMilitarySubject', uselist=False, lazy=True)
