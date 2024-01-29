from database import ProvidedReport, ProvidedReportRecord


def sfr_export_data(session, sfr_export_id):
    """Формирует данные для CSV файла по id экспорта в СФР"""
    # запрос и сортировка сведений по номерам строк
    provided_report = session.query(ProvidedReport)
    provided_report = provided_report.filter(ProvidedReport.id == sfr_export_id)
    provided_report = provided_report.join(ProvidedReportRecord)
    provided_report = provided_report.order_by(ProvidedReportRecord.row_number)
    provided_report = provided_report.scalar()
    # обработка результатов запроса
    export_csv = []
    if provided_report:
        for record in provided_report.provided_report_records:
            defender = record.keeped_report_record.linked_defender
            row = [
                defender.linked_person.picked_last_name.value,
                defender.linked_person.picked_first_name.value,
                defender.linked_person.picked_middle_name.value,
                defender.linked_person.eskk_gender.id,
                defender.linked_person.birthday,
                defender.birth_place,
                defender.linked_person.picked_snils.value,
                defender.linked_document.eskk_document_type.id,
                defender.linked_document.picked_serial.value,
                defender.linked_document.picked_number.value,
                defender.linked_document.date,
                defender.linked_document.picked_organization.value,
                defender.linked_document_vbd.picked_serial.value,
                defender.linked_document_vbd.picked_number.value,
                defender.linked_document_vbd.date,
                defender.linked_document_vbd.picked_organization.value,
                defender.linked_reg_address.picked_index.value,
                defender.linked_reg_address.picked_region.value,
                defender.linked_reg_address.picked_area.value,
                defender.linked_reg_address.picked_locality.value,
                defender.linked_reg_address.picked_street.value,
                defender.linked_reg_address.picked_house.value,
                defender.linked_reg_address.picked_building.value,
                defender.linked_reg_address.picked_flat.value,
                defender.linked_fact_address.picked_index.value,
                defender.linked_fact_address.picked_region.value,
                defender.linked_fact_address.picked_area.value,
                defender.linked_fact_address.picked_locality.value,
                defender.linked_fact_address.picked_street.value,
                defender.linked_fact_address.picked_house.value,
                defender.linked_fact_address.picked_building.value,
                defender.linked_fact_address.picked_flat.value,
                defender.id_ern
            ]
            export_csv.append(row)
    return export_csv
