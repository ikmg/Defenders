import pyexcel
import openpyxl

# from tools.filesystem import base_filename, filename_extension, delete_file


def convert_to_xlsx(filepath):
    base = base_filename(filepath)
    path = filepath.replace(base, '')
    ext = filename_extension(base)
    base = base.replace(ext, '')
    filename_xls = '{}{}.xls'.format(path, base)
    pyexcel.save_book_as(
        file_name=filepath,
        dest_file_name=filename_xls
    )
    delete_file(filepath)
    filename_xlsx = '{}{}.xlsx'.format(path, base)
    pyexcel.save_book_as(file_name=filename_xls,
                         dest_file_name=filename_xlsx)
    delete_file(filepath)

    return filename_xls


def write_xls_list(filename, data_list):
    pyexcel.save_as(array=data_list, dest_file_name=filename)


def report_result(filename, column_data):
    workbook = pyexcel.get_book(file_name=filename)
    worksheet = workbook.sheet_by_name('Лист1')
    result_column = ['РЕЗУЛЬТАТ', 38]
    result_column += column_data
    worksheet.column += result_column
    for row_ind, row_val in enumerate(worksheet.array):
        for col_ind, col_val in enumerate(row_val):
            # worksheet.array[row_ind][col_ind] = str(col_val)
            worksheet[row_ind, col_ind] = str(col_val)
    workbook.save_as(filename)
