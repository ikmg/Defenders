from abc import abstractmethod, ABC

from tools import DTConvert


def get_key(pn: str):
    cases = {
        'А': 'A',
        'A': 'A',
        'ПР': 'PR',
        'ПP': 'PR',
        'РС': 'RS',
        'РC': 'RS',
        'PС': 'RS',
        'PC': 'RS'
    }
    for case in cases:
        if case in pn:
            return cases[case]
    return 'other'


class Base(ABC):

    def __init__(self):
        self.count = 0
        self._dict_ = {}

    def __repr__(self):
        return str(self.count)

    @abstractmethod
    def add(self, *args):
        pass

    @abstractmethod
    def kit(self):
        pass


class Keys(Base):

    def add(self, key: str):
        self.count += 1
        if key not in self._dict_:
            self._dict_[key] = 0
        self._dict_[key] += 1

    def percent(self, key):
        if key in self._dict_:
            if self.count:
                return round(self._dict_[key] / self.count * 100, 2)
        else:
            self._dict_[key] = 0
            return 0

    def kit(self):
        self._dict_['count'] = self.count
        self._dict_['A_percent'] = self.percent('A')
        self._dict_['PR_percent'] = self.percent('PR')
        self._dict_['RS_percent'] = self.percent('RS')
        self._dict_['other_percent'] = round(100 - (
                self._dict_['A_percent'] - self._dict_['PR_percent'] - self._dict_['RS_percent']
        ), 2)
        return {'Сводные сведения': self._dict_}


class Years(Base):

    def add(self, year: str, key: str):
        if year not in self._dict_:
            self.count += 1
            self._dict_[year] = Keys()
        self._dict_[year].add(key)

    def kit(self):
        result = {}
        self._dict_ = dict(sorted(self._dict_.items()))
        for year in self._dict_:
            key = 'в {} г.'.format(year) if year else 'Год не определен'
            result[key] = self._dict_[year].kit()['Сводные сведения']
        return result


class Collection(ABC):

    def __init__(self):
        self.total = Keys()
        self.years = Years()

    @abstractmethod
    def add(self, *args):
        pass

    def kit(self):
        return {**self.total.kit(), **self.years.kit()}


class Persons(Collection):

    def add(self, key: str, years: iter):
        self.total.add(key)
        for year in years:
            self.years.add(year, key)


class Periods(Collection):

    def add(self, key: str, years: iter):
        for year in years:
            self.total.add(key)
            self.years.add(year, key)


def inspect_participants(orders_id: str, models: iter):
    persons = Persons()
    periods = Periods()

    print(DTConvert().dtstring, '{} участников'.format(len(models)))

    for index, model in enumerate(models):
        if (index + 1) % 10000 == 0:
            print(DTConvert().dtstring, 'обработано {}'.format(index + 1))

        person_years = set()
        person_periods = []

        for period in model.linked_order_person_periods:
            date = DTConvert(period.date_begin).date
            year = date.year if date else 0
            person_years.add(year)
            person_periods.append(year)

        key = get_key(model.picked_personal_number.value)
        persons.add(key, person_years)
        periods.add(key, person_periods)

    print(DTConvert().dtstring, 'обработка завершена')

    result = []
    temp = {
        'Участники': persons.kit(),
        'Периоды участия': periods.kit()
    }
    sorter = 0
    for data_type in temp:
        for name in temp[data_type]:
            sorter += 1
            primary_key = {
                'keeped_order_id': orders_id,
                'data_type': data_type,
                'name': name,
                'sort': sorter,
            }
            result.append({**primary_key, **temp[data_type][name]})
    return result
