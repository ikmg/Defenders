from datetime import datetime, date, timedelta, timezone


# FROM STRING


def string_to_date(value):
    try:
        return datetime.strptime(str(value), '%d.%m.%Y').date()
    except:
        try:
            return datetime.strptime(str(value), '%Y-%m-%d').date()
        except:
            return None


def string_to_datetime(value):
    try:
        return datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S.%f')
    except:
        try:
            return datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S')
        except:
            try:
                return datetime.strptime(str(value), '%d-%m-%Y %H:%M:%S')
            except:
                return None


# FROM DATETIME

def date_to_string(value):
    if isinstance(value, date):
        return value.strftime('%d.%m.%Y')
    else:
        return value


def datetime_to_string(value):
    if isinstance(value, datetime):
        return value.strftime('%d.%m.%Y %H:%M:%S')
    else:
        return value


# TIMEZONE


def datetime_timezone():
    delta = timedelta(hours=3, minutes=0)
    return datetime.now(timezone.utc) + delta


def date_timezone():
    return datetime_timezone().date()
