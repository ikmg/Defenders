def clear_string(value):
    if value:
        result = str(value)
        result = result.replace('\r', ' ')
        result = result.replace('\n', ' ')
        result = result.strip()
        while '  ' in result:
            result = result.replace('  ', ' ')
        result = (result.replace('‐', '-')
                  .replace('–', '-')
                  .replace('—', '-')
                  .replace('−', '-'))
        result = change_e_symbol(result)
        return result
    else:
        return ''


def change_e_symbol(value):
    return value.replace('Ё', 'Е').replace('ё', 'е')


def is_snils_valid(value):
    number = value[:9]
    for item in ['000', '111', '222', '333', '444', '555', '666', '777', '888', '999']:
        if item in number:
            return False
    if number > '001001998' and len(number) == 9:
        check_sum = int(value[9:])
        summ = 0
        for i in range(9):
            summ += int(number[i]) * (9 - i)
        summ = str(summ % 101)
        summ = int(summ[len(summ) - 2:])
        if summ == check_sum:
            return True
        else:
            return False
    else:
        return True


def get_fio_list(value):
    temp = clear_string(value)
    temp = temp.split(' ', 2)
    if len(temp) == 3:
        return temp
    elif len(temp) == 2:
        return temp + ['']
    else:
        return temp + ['', '']
