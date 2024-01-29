from .data import dict_from_csv
from .handler import EskkGenderHandler, EskkDocumentTypeHandler, EskkMilitaryRankHandler, EskkMilitarySubjectHandler


def base_upload(session, class_name, file_path):
    data = dict_from_csv(file_path)
    for row in data:
        class_name(session, **row)
    session.commit()


def eskk_genders_upload(session, file_path):
    base_upload(session, EskkGenderHandler, file_path)


def eskk_document_types_upload(session, file_path):
    base_upload(session, EskkDocumentTypeHandler, file_path)


def eskk_military_ranks_upload(session, file_path):
    base_upload(session, EskkMilitaryRankHandler, file_path)


def eskk_military_subjects_upload(session, file_path):
    base_upload(session, EskkMilitarySubjectHandler, file_path)
