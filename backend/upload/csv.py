from .data import dict_from_csv
from .handler import EskkGenderHandler, EskkDocumentTypeHandler, EskkMilitaryRankHandler, EskkMilitarySubjectHandler


def base_upload(session, class_name, file):
    if file.is_exists:
        data = dict_from_csv(file.path)
        for row in data:
            class_name(session, **row)
        session.commit()
    else:
        raise FileNotFoundError('Файл не найден {}'.format(file.rel_path))


def eskk_genders_upload(session, file):
    base_upload(session, EskkGenderHandler, file)


def eskk_document_types_upload(session, file):
    base_upload(session, EskkDocumentTypeHandler, file)


def eskk_military_ranks_upload(session, file):
    base_upload(session, EskkMilitaryRankHandler, file)


def eskk_military_subjects_upload(session, file):
    base_upload(session, EskkMilitarySubjectHandler, file)
