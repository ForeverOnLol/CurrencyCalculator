import datetime
from datetime import datetime

from datequarter import DateQuarter
from dateutil.relativedelta import relativedelta


class RequiredDate:
    '''
    Создаём необходимые даты:
    1) Все дни последних четырёх недель,
    2) Все дни последних четырёх месяцев,
    4) 1 и 15 день каждого месяца последних четырёх лет.
    :return: None
    '''

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
        :return: список с датами
        '''
        dates_list_fixed = []
        for date in dates_list:
            if (date.day == 1) or (date.day == 15):
                dates_list_fixed.append(date)
        return dates_list_fixed

    @classmethod
    def last_weeks(cls) -> list[datetime.date]:
        '''
        Все дни последних четырёх недель.
        :return: Список с датами
        '''
        today = datetime.datetime.now().date()
        start_date = today - relativedelta(days=today.weekday(), weeks=3)
        return cls.__count(start_dt=start_date, end_dt=today)

    @classmethod
    def last_months(cls) -> list[datetime.date]:
        '''
        Все дни последних четырёх месяцев.
        :return: Список с датами
        '''
        today = datetime.datetime.now().date()
        start_date = today - relativedelta(days=today.day - 1, months=3)
        return cls.__count(start_dt=start_date, end_dt=today)

    @classmethod
    def last_quarts(cls) -> list[datetime.date]:
        '''
        1 и 15 день каждого месяца последних четырёх кварталов.
        :return: Список с датами
        '''
        today = datetime.datetime.now().date()
        start_quart = DateQuarter.from_date(today.replace(day=1)) - 3
        start_date = start_quart.start_date()

        dates_list = cls.__count(start_dt=start_date, end_dt=today)
        return cls.__start_mid_format(dates_list)

    @classmethod
    def last_years(cls) -> list[datetime.date]:
        '''
        1 и 15 день каждого месяца последних четырёх лет.
        :return: Список с датами
        '''
        today = datetime.datetime.now().date()
        start_date = today.replace(day=1, month=1) - relativedelta(years=3)

        dates_list = cls.__count(start_dt=start_date, end_dt=today)
        return cls.__start_mid_format(dates_list)

    @classmethod
    def all(cls) -> list[str]:
        '''
        Возвращает список строк в формате %Y/%m/%d с необходимыми датами.
        :return: список с датами
        '''
        result = []
        for date in cls.last_weeks() + cls.last_months() + cls.last_quarts() + cls.last_years():
            date = date.strftime('%d/%m/%Y')
            if date not in result:
                result.append(date)
        return result
