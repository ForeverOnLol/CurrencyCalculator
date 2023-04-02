import sys

from common.orm import ValutePrice, Valute, ValuteByDay
from common.required_date import RequiredDate
from common.scrapper import CbrScrapper


class ValuteManager:
    '''
    Управляет валютами и данными о них.
    '''

    @classmethod
    def load_data_in_db(cls) -> None:
        '''
        Подгрузка данных в БД при каждом запуске приложения.
        :return: None
        '''

        valute_list = Valute.all()

        if not len(valute_list):
            cls.load_all()
        else:
            cls.load_fresh()

    @classmethod
    def load_all(cls) -> None:
        '''
        Подгрузить все данные из ЦБ в БД.
        :return:
        '''

        date_list = RequiredDate.all()
        ValuteManager.load_valutes_by_dates(date_list)

    @classmethod
    def load_fresh(cls) -> None:
        '''
        Подгрузка новых данных из ЦБ в БД.
        :return:
        '''
        existing_dates = frozenset(ValutePrice.existing_dates())
        date_list = frozenset(RequiredDate.all())
        mismatched = date_list - existing_dates

        ValuteManager.load_valutes_by_dates(dates=list(mismatched))

    @classmethod
    def today(cls) -> list[ValuteByDay]:
        date = RequiredDate.today()
        return ValuteByDay.all(date=date)

    @classmethod
    def load_valutes_by_dates(cls, dates: list[str]):
        print(
            'Подгрузка всех необходимых данных из ЦБ. Пожалуйста, подождите. Если вы прервёте загрузку, то '
            'приложение может работать некорректно.')
        for date in dates:
            valute_by_day_list = CbrScrapper(date=date).get()
            for valute in valute_by_day_list:
                sys.stdout.write('\033[2K\033[1G')
                print(f'\rПодгрузка валюты {valute.entity.name} за {date}', end='')
                valute.entity.create()
                valute.data.create()
        sys.stdout.write('\033[2K\033[1G')
        print('Все данные подгружены', end='\n')
