from datetime import datetime


class H:
    def __init__(self, num, val=datetime.now()):
        self.value = val
        self.num = num
        print('num: {}, class id: {}, value id: {}, value: {}'.format(
            self.num, id(self), id(self.value), self.value
        ))


for i in range(10):
    print('try #', i)
    H(i)












# if val == None:
#     self.value = datetime.now()

from tools import DateTimeConvert


def test(val_type, object):
    print(val_type)
    print('value', object.value, type(object.value))
    tmp = object.date
    print('date', tmp, type(tmp))
    tmp = object.datetime
    print('datetime', tmp, type(tmp))
    tmp = object.string
    print('string', tmp, type(tmp))
    print()


# datetime
# test('дата/время', DateTimeConvert())
# # date
# dt = DateTimeConvert().value.date()
# test('дата', DateTimeConvert(dt))
# # string
# test('строка', DateTimeConvert('16.04.1986'))
# test('строка', DateTimeConvert('1986-04-16'))
#
# test('строка', DateTimeConvert('1986-04-16 01:01:01.567'))  # '%Y-%m-%d %H:%M:%S.%f'
# test('строка', DateTimeConvert('1986-04-16 01:01:01'))  # '%Y-%m-%d %H:%M:%S'
# test('строка', DateTimeConvert('16-04-1986 01:01:01'))  # '%d-%m-%Y %H:%M:%S'
# test('строка', DateTimeConvert('хуй'))
# test('строка', DateTimeConvert(''))
# test('строка', DateTimeConvert(True))
# test('строка', DateTimeConvert(None))
