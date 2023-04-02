from enum import Enum
from typing import Optional

from common.orm import Valute, ValuteByDay
from common.required_date import RequiredDate


class ValuteConv():
    @staticmethod
    def __conv_to_rub(valute_name, count) -> float:
        '''
        Конвертация в российский рубль
        :param valute_name:
        :return:
        '''
        if valute_name == 'Российский рубль':
            return count
        today = RequiredDate.today()
        valute = ValuteByDay.get(name=valute_name, date=today)
        price = valute.data.value
        nominal = valute.entity.nominal
        return float(count) * float(price) * float(1) / (
                float(1) * float(nominal))

    @staticmethod
    def __conv_from_rub(valute_name, count) -> float:
        '''
        Конвертация из российского рубля
        :param valute_name:
        :return:
        '''
        if valute_name == 'Российский рубль':
            return count
        today = RequiredDate.today()
        valute = ValuteByDay.get(name=valute_name, date=today)
        price = valute.data.value
        nominal = valute.entity.nominal
        return float(count) * float(1) * float(nominal) / (
                float(price) * float(1))

    @staticmethod
    def today(valute_first: str, valute_second: str, count) -> float:
        '''
        Конвертация одной валюты в другую по курсу текущего дня
        :param valute_first: название первой валюты на русском.
        :param valute_second: название второй валюты на русском.
        :param count: число, которое необходимо конвертировать
        :return:
        '''
        if valute_first == 'Российский рубль':
            return ValuteConv.__conv_from_rub(valute_name=valute_second, count=count)
        if valute_second == 'Российский рубль':
            return ValuteConv.__conv_to_rub(valute_name=valute_first, count=count)

        today = RequiredDate.today()
        first_v = ValuteByDay.get(name=valute_first, date=today)
        second_v = ValuteByDay.get(name=valute_second, date=today)
        first_v_price = first_v.data.value
        second_v_price = second_v.data.value
        first_v_nominal = first_v.entity.nominal
        second_v_nominal = second_v.entity.nominal

        result = float(count) * float(first_v_price) * float(second_v_nominal) / (
                float(second_v_price) * float(first_v_nominal))
        return result

    @staticmethod
    def names(with_rub=True) -> list:
        '''
        Выводит список названий валют текущего дня.
        :return:
        '''
        today = RequiredDate.today()
        valute_by_day_list = ValuteByDay.all(today)
        res = []
        if with_rub:
            res.append('Российский рубль')

        for i in valute_by_day_list:
            res.append(i.entity.name)
        return res


class ValuteAnalize():
    @staticmethod
    def period(period_name: str) -> dict:
        period_name = period_name.lower()
        match period_name:
            case 'неделя':
                return RequiredDate.last_weeks_detail()
            case 'месяц':
                return RequiredDate.last_months_detail()
            case 'квартал':
                return RequiredDate.last_quarts_detail()
            case 'год':
                return RequiredDate.last_year_detail()

    @staticmethod
    def valute_prices(date_list: list, valute_name) -> list:
        values = []

        for date in date_list:
            valute_price = ValuteByDay.get(name=valute_name, date=date).data.value
            values.append(valute_price)
        return values
