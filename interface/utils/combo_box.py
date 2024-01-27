from database import EskkMilitarySubject


def subjects_combo_box_items(session):
    result = []
    models = session.query(EskkMilitarySubject).order_by(EskkMilitarySubject.short_name).all()
    for model in models:
        if model.conditional_short_name:
            result.append([model.id, '{} ({})'.format(model.short_name, model.conditional_short_name)])
        else:
            result.append([model.id, '{}'.format(model.short_name)])
    return result
