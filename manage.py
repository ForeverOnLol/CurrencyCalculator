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
        print('Подгрузка данных из ЦБ. Пожалуйста, подождите.')
        date_list = RequiredDate.all()
        for date in date_list:
            valute_by_day_list = CbrScrapper(date=date).get()
            for valute in valute_by_day_list:
                valute.entity.create()
                valute.data.create()

    @classmethod
    def load_fresh(cls) -> None:
        '''
        Подгрузка новых данных из ЦБ в БД.
        :return:
        '''
        print('Подгрузка новых данных из ЦБ. Пожалуйста, подождите.')
        existing_dates = frozenset(ValutePrice.existing_dates())
        date_list = frozenset(RequiredDate.all())
        mismatched = date_list - existing_dates

        if mismatched:
            for date in mismatched:
                valute_by_day_list = CbrScrapper(date=date).get()
                for valute in valute_by_day_list:
                    valute.entity.create()
                    valute.data.create()

    @classmethod
    def today(cls) -> list[ValuteByDay]:
        date = RequiredDate.today()
        return ValuteByDay.all(date=date)
