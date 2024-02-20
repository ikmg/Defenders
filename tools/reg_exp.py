import re

from tools import DTConvert


def is_date_format(value):
    """"""
    tmp = DTConvert(value).dstring   # должна быть дата
    if tmp and len(tmp) == 10 and re.fullmatch('\d{2}[.]{1}\d{2}[.]{1}\d{4}', tmp):
        return True
    else:
        return False


def re_full_match(pattern, value):
    return True if re.fullmatch(pattern, value) else False
