from .app import DefendersApp
from .fs import Directory, File


from .ini_files import ini_to_dict
from .csv_files import csv_to_dict, write_csv_dict, write_csv_list
from .xls_file import write_xls_list

from .config import Config

from .date_and_time import string_to_date, date_to_string, datetime_to_string, date_timezone, datetime_timezone, string_to_datetime

from .strings import clear_string, clear_personal_number, change_e_symbol, is_snils_valid, get_fio_list
from .reg_exp import re_full_match, is_date_format


def debug_print(text):
    print('[{}] {}'.format(date_to_string(datetime_timezone()), text))
