import datetime
from typing import Union

from datequarter import DateQuarter
from dateutil.relativedelta import relativedelta


def num_month_to_name(num: int, short: bool = False) -> str:
    '''
    Преобразование номера месяца в название на русском
    :param num: номер месяца
    :param short: флаг, если надо короткое название месяца, например, январь - янв
    :return:
    '''
    if short:
        d = {
            1: 'Янв',
            2: 'Фев',
            3: 'Мар',
            4: 'Апр',
            5: 'Май',
            6: 'Июнь',
            7: 'Июль',
            8: 'Авг',
            9: 'Сен',
            10: 'Окт',
            11: 'Нояб',
            12: 'Дек'
        }
    else:
        d = {
            1: 'Январь',
            2: 'Февраль',
            3: 'Март',
            4: 'Апрель',
            5: 'Май',
            6: 'Июнь',
            7: 'Июль',
            8: 'Август',
            9: 'Сентябрь',
            10: 'Октябрь',
            11: 'Ноябрь',
            12: 'Декабрь'
        }
    return d[num]


class RequiredDate:
    '''
    Создаём необходимые даты:
    1) Все дни последних четырёх недель,
    2) Все дни последних четырёх месяцев,
    4) 1 и 15 день каждого месяца последних четырёх лет.
    :return: None
    '''

    @staticmethod
    def __date_to_str(date: datetime.date):
        return date.strftime('%d/%m/%Y')

    @staticmethod
    def __count(start_dt: datetime.date, end_dt: datetime.date) -> list[datetime.date]:
        '''
        Создание списка с датами от start_dt до end_dt
        :param start_dt: стартовая дата
        :param end_dt: конечная дата
        :return: список с датами
        '''
        result = []
        while (start_dt <= end_dt):
            result.append(start_dt)
            start_dt += datetime.timedelta(days=1)
        return result

    @staticmethod
    def __start_mid_format(dates_list: list[datetime.date]) -> list[datetime.date]:
        '''
        Форматирование списка, исключающее все даты, кроме 01 и 15 дня месяца.
        :param dates_list: Список с датами
        :return: список с датами в формате %Y/%m/%d.
        '''
        dates_list_fixed = []
        for date in dates_list:
            if (date.day == 1) or (date.day == 15):
                dates_list_fixed.append(date)
        return dates_list_fixed

    @staticmethod
    def __conv_to_str(date_list: list[datetime.date]) -> list[str]:
        '''
        Преобразование списка дат формата datetime.date в список со строками-датами в формате %Y/%m/%d.
        :param date_list:
        :return:
        '''
        f = lambda x: RequiredDate.__date_to_str(x)
        return list(map(f, date_list))

    @classmethod
    def last_weeks(cls, original=False) -> list[Union[str, datetime.date]]:
        '''
        Все дни последних четырёх недель.
        :param original: Возврат данных в формате datetime.date если True, или в формате строк если False
        :return: Список с датами в формате %Y/%m/%d
        '''
        today = datetime.datetime.now().date()
        start_date = today - relativedelta(days=today.weekday(), weeks=3)
        date_list = cls.__count(start_dt=start_date, end_dt=today)
        if original:
            return date_list
        return cls.__conv_to_str(date_list=date_list)

    @classmethod
    def last_weeks_detail(cls) -> dict:
        '''
        Получение полной информации о днях последних 4 недель в расширенном формате.
        :return: Словарь -> ключ - интервал недели прим. '13/02/2023 - 19/02/2023', значение - кортеж с датами данного
         интервала
        '''
        dates = RequiredDate.last_weeks()
        return {
            f'{dates[0]} - {dates[6]}': [dates[i] for i in range(7)],
            f'{dates[7]} - {dates[13]}': [dates[i] for i in range(7, 13)],
            f'{dates[14]} - {dates[20]}': [dates[i] for i in range(13, 20)],
            f'{dates[21]} - {dates[-1]}': [dates[i] for i in range(20, len(dates))]
        }

    @classmethod
    def last_months(cls, original=False) -> list[Union[str, datetime.date]]:
        '''
        Все дни последних четырёх месяцев.
        :param original: Возврат данных в формате datetime.date если True, или в формате строк если False.
        :return: Список с датами в формате %Y/%m/%d.
        '''
        today = datetime.datetime.now().date()
        start_date = today - relativedelta(days=today.day - 1, months=3)
        date_list = cls.__count(start_dt=start_date, end_dt=today)
        if original:
            return date_list
        return cls.__conv_to_str(date_list=date_list)

    @classmethod
    def last_months_detail(cls) -> dict:
        '''
        Получение полной информации о днях последних 4 месяцах в расширенном формате.
        :return: Словарь -> ключ - названия месяца и год прим. 'Январь 2023', значение - кортеж с датами данного меесяца.
        '''
        dates = RequiredDate.last_months(original=True)

        res_d = {}

        for d in dates:
            month_year = f'{num_month_to_name(d.month)} {d.year}'
            if month_year not in res_d:
                res_d[month_year] = []
            res_d[month_year].append(RequiredDate.__date_to_str(d))

        return res_d

    @classmethod
    def last_quarts(cls, original=False) -> list[Union[str, datetime.date]]:
        '''
        1 и 15 день каждого месяца последних четырёх кварталов.
        :param original: Возврат данных в формате datetime.date если True, или в формате строк если False.
        :return: Список с датами в формате %Y/%m/%d.
        '''
        today = datetime.datetime.now().date()
        start_quart = DateQuarter.from_date(today.replace(day=1)) - 3
        start_date = start_quart.start_date()

        date_list = cls.__count(start_dt=start_date, end_dt=today)
        date_list = cls.__start_mid_format(date_list)
        if original:
            return date_list
        return cls.__conv_to_str(date_list=date_list)

    @classmethod
    def last_quarts_detail(cls) -> dict:
        '''
        Получение полной информации о днях последних 4 кварталах в расширенном формате.
        :return: Словарь -> ключ - названия квартала и год прим. '1 квартал 2021', значение - кортеж с датами данного квартала
        '''
        dates = RequiredDate.last_quarts(original=True)
        num_quart_to_name = {
            1: '1 квартал',
            2: '2 квартал',
            3: '3 квартал',
            4: '4 квартал'
        }

        res_d = {}

        for d in dates:
            quart = f'{num_quart_to_name[DateQuarter.from_date(d).quarter()]} {d.year}'
            if quart not in res_d:
                res_d[quart] = []
            res_d[quart].append(RequiredDate.__date_to_str(d))

        return res_d

    @classmethod
    def last_years(cls, original=True) -> list[Union[str, datetime.date]]:
        '''
        1 и 15 день каждого месяца последних четырёх лет.
        :param original: Возврат данных в формате datetime.date если True, или в формате строк если False
        :return: Список с датами в формате %Y/%m/%d.
        '''
        today = datetime.datetime.now().date()
        start_date = today.replace(day=1, month=1) - relativedelta(years=3)

        dates_list = cls.__count(start_dt=start_date, end_dt=today)
        date_list = cls.__start_mid_format(dates_list)
        if original:
            return date_list
        return cls.__conv_to_str(date_list=date_list)

    @classmethod
    def last_year_detail(cls) -> dict:
        '''
        Получение полной информации о днях последних 4 годах в расширенном формате.
        :return: Словарь -> ключ - год прим. '2021', значение - кортеж с датами данного года.
        '''
        dates = RequiredDate.last_years(original=True)

        res_d = {}

        for d in dates:
            year = f'{d.year}'
            if year not in res_d:
                res_d[year] = []
            res_d[year].append(RequiredDate.__date_to_str(d))

        return res_d

    @classmethod
    def all(cls) -> list[str]:
        '''
        Возвращает все необходимые даты.
        :return: Список с датами в формате %Y/%m/%d.
        '''
        result = []
        for date in cls.last_weeks(original=False) + cls.last_months(original=False) + cls.last_quarts(
                original=False) + cls.last_years(original=False):
            if date not in result:
                result.append(date)
        return result

    @classmethod
    def today(cls) -> str:
        '''
        Возвращает текущую дату.
        :return: дата в формате %Y/%m/%d.
        '''
        today = [datetime.datetime.now().date()]
        return cls.__conv_to_str(today)[0]
