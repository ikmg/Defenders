from datetime import datetime

from tools import get_new_path
from .dump import (OrderFIODumper, OrderPersonDumper, OrderPersonPeriodDumper, OrderDumper, LastNameDumper, FirstNameDumper, MiddleNameDumper,
                   SNILSDumper, DocumentSerialDumper, DocumentNumberDumper, DocumentOrganizationDumper, AddressIndexDumper, AddressRegionDumper,
                   AddressAreaDumper, AddressLocalityDumper, AddressStreetDumper, AddressHouseDumper, AddressBuildingDumper, AddressFlatDumper,
                   PersonalNumberDumper, MilitaryRankDumper, MilitarySubjectDumper, PersonDumper, DocumentDumper, DocumentVBDDumper, AddressVBDDumper,
                   ReportDumper, DefenderDumper)


def dump_orders(session, root):
    dump = get_new_path(root, 'dump')

    filepath = get_new_path(dump, 'oshu_order_fio.csv')
    print('[{}] <{}> обработка'.format(datetime.now(), filepath))
    print('[{}] {}'.format(datetime.now(), OrderFIODumper(session, filepath)))

    filepath = get_new_path(dump, 'oshu_order_persons.csv')
    print('[{}] <{}> обработка'.format(datetime.now(), filepath))
    print('[{}] {}'.format(datetime.now(), OrderPersonDumper(session, filepath)))

    filepath = get_new_path(dump, 'oshu_order_person_periods.csv')
    print('[{}] <{}> обработка'.format(datetime.now(), filepath))
    print('[{}] {}'.format(datetime.now(), OrderPersonPeriodDumper(session, filepath)))

    print('[{}] запись периодов в импорт приказа'.format(datetime.now(), filepath))
    print('[{}] {}'.format(datetime.now(), OrderDumper(session)))


def dump_defenders(session, root):
    dump = get_new_path(root, 'dump')

    print(LastNameDumper(session, get_new_path(dump, 'last_names.csv')))
    print(FirstNameDumper(session, get_new_path(dump, 'first_names.csv')))
    print(MiddleNameDumper(session, get_new_path(dump, 'middle_names.csv')))
    print(SNILSDumper(session, get_new_path(dump, 'snilses.csv')))

    print(DocumentSerialDumper(session, get_new_path(dump, 'document_serials.csv')))
    print(DocumentNumberDumper(session, get_new_path(dump, 'document_numbers.csv')))
    print(DocumentOrganizationDumper(session, get_new_path(dump, 'document_organizations.csv')))

    print(AddressIndexDumper(session, get_new_path(dump, 'address_indexes.csv')))
    print(AddressRegionDumper(session, get_new_path(dump, 'address_regions.csv')))
    print(AddressAreaDumper(session, get_new_path(dump, 'address_areas.csv')))
    print(AddressLocalityDumper(session, get_new_path(dump, 'address_localities.csv')))
    print(AddressStreetDumper(session, get_new_path(dump, 'address_streets.csv')))
    print(AddressHouseDumper(session, get_new_path(dump, 'address_houses.csv')))
    print(AddressBuildingDumper(session, get_new_path(dump, 'address_buildings.csv')))
    print(AddressFlatDumper(session, get_new_path(dump, 'address_rooms.csv')))

    print(PersonalNumberDumper(session, get_new_path(dump, 'personal_numbers.csv')))
    print(MilitaryRankDumper(session, get_new_path(dump, 'military_ranks_tmp.csv')))
    print(MilitarySubjectDumper(session, get_new_path(dump, 'military_subjects_tmp.csv')))

    print(PersonDumper(session, get_new_path(dump, 'persons.csv')))
    print(DocumentDumper(session, get_new_path(dump, 'documents.csv')))
    print(DocumentVBDDumper(session, get_new_path(dump, 'documents_vbd.csv')))
    print(AddressVBDDumper(session, get_new_path(dump, 'addresses.csv')))

    print(ReportDumper(session, get_new_path(dump, 'defenders_imports.csv')))
    print(DefenderDumper(session, get_new_path(dump, 'defenders.csv')))
