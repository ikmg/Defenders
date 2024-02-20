from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from . import BaseModel


# ------------------------------------------------------------------
#                 КОМПОНОВЩИКИ ПЕРВОГО УРОВНЯ
# ------------------------------------------------------------------
# Композиция из классификаторов и пикеров в осмысленный набор данных
# ------------------------------------------------------------------


class LinkedPerson(BaseModel):
    """Компоновщик сведений о гражданине Российской Федерации по набору данных СФР (как в СМЭВ)."""
    __tablename__ = 'linked_persons'

    eskk_gender_id = Column(String, ForeignKey('eskk_genders.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    picked_snils_id = Column(String, ForeignKey('picked_snilses.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    picked_last_name_id = Column(String, ForeignKey('picked_last_names.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    picked_first_name_id = Column(String, ForeignKey('picked_first_names.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    picked_middle_name_id = Column(String, ForeignKey('picked_middle_names.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    birthday = Column(String, primary_key=True, nullable=False)

    eskk_gender = relationship('EskkGender', uselist=False, lazy=True)
    picked_snils = relationship('PickedSNILS', uselist=False, lazy=True)
    picked_last_name = relationship('PickedLastName', uselist=False, lazy=True)
    picked_first_name = relationship('PickedFirstName', uselist=False, lazy=True)
    picked_middle_name = relationship('PickedMiddleName', uselist=False, lazy=True)

    @hybrid_property
    def person_appeal(self):
        return '{} {} {}'.format(
            self.picked_last_name.value,
            self.picked_first_name.value,
            self.picked_middle_name.value
        )


class LinkedDocument(BaseModel):
    """Компоновщик сведений о документах, удостоверяющих личность на территории Российской Федерации."""
    __tablename__ = 'linked_documents'

    eskk_document_type_id = Column(String, ForeignKey('eskk_document_types.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    picked_serial_id = Column(String, ForeignKey('picked_document_serials.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    picked_number_id = Column(String, ForeignKey('picked_document_numbers.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    picked_organization_id = Column(String, ForeignKey('picked_document_organizations.id', ondelete='CASCADE'), nullable=False)
    date = Column(String, nullable=False)

    eskk_document_type = relationship('EskkDocumentType', uselist=False, lazy=True)
    picked_serial = relationship('PickedDocumentSerial', uselist=False, lazy=True)
    picked_number = relationship('PickedDocumentNumber', uselist=False, lazy=True)
    picked_organization = relationship('PickedDocumentOrganization', uselist=False, lazy=True)


class LinkedDocumentVBD(BaseModel):
    """Компоновщик сведений об удостоверениях ветерана боевых действий."""
    __tablename__ = 'linked_documents_vbd'

    picked_serial_id = Column(String, ForeignKey('picked_document_serials.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    picked_number_id = Column(String, ForeignKey('picked_document_numbers.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    picked_organization_id = Column(String, ForeignKey('picked_document_organizations.id', ondelete='CASCADE'), nullable=False)
    date = Column(String, nullable=False)

    picked_serial = relationship('PickedDocumentSerial', uselist=False, lazy=True)
    picked_number = relationship('PickedDocumentNumber', uselist=False, lazy=True)
    picked_organization = relationship('PickedDocumentOrganization', uselist=False, lazy=True)


class LinkedAddress(BaseModel):
    """Компоновщик сведений об адресах."""
    __tablename__ = 'linked_addresses'

    picked_index_id = Column(String, ForeignKey('picked_address_indexes.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    picked_region_id = Column(String, ForeignKey('picked_address_regions.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    picked_area_id = Column(String, ForeignKey('picked_address_areas.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    picked_locality_id = Column(String, ForeignKey('picked_address_localities.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    picked_street_id = Column(String, ForeignKey('picked_address_streets.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    picked_house_id = Column(String, ForeignKey('picked_address_houses.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    picked_building_id = Column(String, ForeignKey('picked_address_buildings.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    picked_flat_id = Column(String, ForeignKey('picked_address_flats.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    picked_index = relationship('PickedAddressIndex', uselist=False, lazy=True)
    picked_region = relationship('PickedAddressRegion', uselist=False, lazy=True)
    picked_area = relationship('PickedAddressArea', uselist=False, lazy=True)
    picked_locality = relationship('PickedAddressLocality', uselist=False, lazy=True)
    picked_street = relationship('PickedAddressStreet', uselist=False, lazy=True)
    picked_house = relationship('PickedAddressHouse', uselist=False, lazy=True)
    picked_building = relationship('PickedAddressBuilding', uselist=False, lazy=True)
    picked_flat = relationship('PickedAddressFlat', uselist=False, lazy=True)


class LinkedOrderFIO(BaseModel):
    """Компоновщик сведений о ФИО в приказах ОШУ Росгвардии."""
    __tablename__ = 'linked_order_fio'

    picked_last_name_id = Column(String, ForeignKey('picked_last_names.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    picked_first_name_id = Column(String, ForeignKey('picked_first_names.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    picked_middle_name_id = Column(String, ForeignKey('picked_middle_names.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    picked_last_name = relationship('PickedLastName', uselist=False, lazy=True)
    picked_first_name = relationship('PickedFirstName', uselist=False, lazy=True)
    picked_middle_name = relationship('PickedMiddleName', uselist=False, lazy=True)

    @hybrid_property
    def person_appeal(self):
        return '{} {} {}'.format(
                self.picked_last_name.value,
                self.picked_first_name.value,
                self.picked_middle_name.value
            )


# ---------------------------------------------------------------------
#                    КОМПОНОВЩИКИ ВТОРОГО УРОВНЯ
# ---------------------------------------------------------------------
# Композиция из классификаторов, пикеров и компоновщиков первого уровня
# ---------------------------------------------------------------------


class LinkedOrderPerson(BaseModel):
    """Компоновщик сведений о военнослужащих (сотрудниках) в приказах ОШУ Росгвардии."""
    __tablename__ = 'linked_order_persons'

    picked_military_rank_id = Column(String, ForeignKey('picked_military_ranks.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    picked_personal_number_id = Column(String, ForeignKey('picked_personal_numbers.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    picked_military_subject_id = Column(String, ForeignKey('picked_military_subjects.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    linked_order_fio_id = Column(String, ForeignKey('linked_order_fio.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    # days = Column(String, nullable=False) не нужно т.к. данные пересекаются
    # note = Column(String, nullable=False) не нужно т.к. данные пересекаются

    picked_military_rank = relationship('PickedMilitaryRank', uselist=False, lazy=True)
    picked_personal_number = relationship('PickedPersonalNumber', uselist=False, lazy=True)
    picked_military_subject = relationship('PickedMilitarySubject', uselist=False, lazy=True)
    linked_order_fio = relationship('LinkedOrderFIO', uselist=False, lazy=True)

    linked_order_person_periods = relationship('LinkedOrderPersonPeriod', back_populates='linked_order_person', uselist=True, lazy=True)


class LinkedDefender(BaseModel):
    __tablename__ = 'linked_defenders'

    linked_person_id = Column(String, ForeignKey('linked_persons.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    linked_document_id = Column(String, ForeignKey('linked_documents.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    linked_document_vbd_id = Column(String, ForeignKey('linked_documents_vbd.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    linked_reg_address_id = Column(String, ForeignKey('linked_addresses.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    linked_fact_address_id = Column(String, ForeignKey('linked_addresses.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    picked_military_subject_id = Column(String, ForeignKey('picked_military_subjects.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    picked_personal_number_id = Column(String, ForeignKey('picked_personal_numbers.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    birth_place = Column(String, primary_key=True, nullable=False)
    exclude_date = Column(String, primary_key=True, nullable=False)
    exclude_order = Column(String, primary_key=True, nullable=False)
    id_ern = Column(String, primary_key=True, nullable=False)

    linked_person = relationship('LinkedPerson', uselist=False, lazy=True)
    linked_document = relationship('LinkedDocument', uselist=False, lazy=True)
    linked_document_vbd = relationship('LinkedDocumentVBD', uselist=False, lazy=True)
    linked_reg_address = relationship('LinkedAddress', foreign_keys=[linked_reg_address_id], uselist=False, lazy=True)
    linked_fact_address = relationship('LinkedAddress', foreign_keys=[linked_fact_address_id], uselist=False, lazy=True)
    picked_military_subject = relationship('PickedMilitarySubject', uselist=False, lazy=True)
    picked_personal_number = relationship('PickedPersonalNumber', uselist=False, lazy=True)

    keeped_report_records = relationship('KeepedReportRecord', uselist=True, lazy=True, back_populates='linked_defender')


# --------------------------------------------------------------------------------
#                         КОМПОНОВЩИКИ ТРЕТЬЕГО УРОВНЯ
# --------------------------------------------------------------------------------
# Композиция из классификаторов, пикеров и компоновщиков первого и второго уровней
# --------------------------------------------------------------------------------


class LinkedOrderPersonPeriod(BaseModel):
    """Компоновщик сведений о периодах участия в СВО военнослужащих (сотрудников) в приказах ОШУ Росгвардии."""
    __tablename__ = 'linked_order_person_periods'

    linked_order_person_id = Column(String, ForeignKey('linked_order_persons.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    date_begin = Column(String, primary_key=True, nullable=False)
    date_end = Column(String, primary_key=True, nullable=False)
    days_count = Column(Integer, nullable=False)

    linked_order_person = relationship('LinkedOrderPerson', back_populates='linked_order_person_periods', uselist=False, lazy=True)
    # keeped_order_record = relationship('KeepedOrderRecord', back_populates='linked_order_person_periods', uselist=False, lazy=True)
