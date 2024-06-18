from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import BaseModel


class EskkModel(BaseModel):
    """
    Единая система классификации и кодирования. Абстрактная модель классификатора.
    Первичным ключом классификатора является идентификатор (id),
    также содержит поле со значением (name) и порядок сортировки (sort).
    """
    __abstract__ = True

    id = Column(String, primary_key=True, nullable=False, index=True, doc='Идентификатор значения классификатора')
    name = Column(String, nullable=False, doc='Основное значение классификатора')
    sort = Column(Integer, nullable=True, doc='Порядок сортировки значений')

    def __repr__(self):
        return 'value <{}>, id <{}>'.format(
            self.name,
            self.id
        )


class EskkGender(EskkModel):
    """Классификатор гендеров"""
    __tablename__ = 'eskk_genders'


class EskkDocumentType(EskkModel):
    """Классификатор типов документов"""
    __tablename__ = 'eskk_document_types'


class EskkMilitaryRank(EskkModel):
    """Классификатор воинских (специальных) званий"""
    __tablename__ = 'eskk_military_ranks'


class EskkMilitarySubject(EskkModel):
    """Классификатор субъектов войск"""
    __tablename__ = 'eskk_military_subjects'

    id = Column(String, primary_key=True, nullable=False, index=True)
    parent_id = Column(String, ForeignKey('eskk_military_subjects.id'), nullable=True)

    path = Column(String, nullable=False)
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    conditional_name = Column(String, nullable=True)
    conditional_short_name = Column(String, nullable=True)

    parent = relationship('EskkMilitarySubject', remote_side=id, single_parent=True, lazy=True)
