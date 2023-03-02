import urllib.request
import xml.dom.minidom

from common.models import ValuteByDay, ValutePrice, Valute


class Scrapper:
    @staticmethod
    def _get_xml(url: str):
        return urllib.request.urlopen(url)


class CbrScrapper(Scrapper):
    '''
    Парсер валют сайта ЦБ
    '''
    url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req={}'

    def __init__(self, date: str):
        '''
        :param date: Дата за которую нужны данные.
        '''
        self.date = date
        self.current_url = self.__format_url(date)

    @classmethod
    def __format_url(cls, date: str):
        return cls.url.format(date)

    def __parse_xml(self, cbr_xml):
        '''
        Преобразование XML в объекты, с которыми можно взаимодействовать.
        :param cbr_xml:
        :return:
        '''
        data = []
        dom = xml.dom.minidom.parse(cbr_xml)
        dom.normalize()

        node_array = dom.getElementsByTagName("Valute")
        for node in node_array:
            childList = node.childNodes
            valute = Valute(
                id=childList[3].childNodes[0].nodeValue,
                num_code=childList[0].childNodes[0].nodeValue,
                char_code=childList[1].childNodes[0].nodeValue,
                nominal=childList[2].childNodes[0].nodeValue,
                name=childList[3].childNodes[0].nodeValue
            )
            content = ValutePrice(
                date=self.date,
                value=str(childList[4].childNodes[0].nodeValue).replace(',', '.'),
                valute_id=childList[3].childNodes[0].nodeValue
            )
            data.append(ValuteByDay(valute, content))
        return data

    def get(self) -> list[ValuteByDay]:
        '''
        Получение данных о всех валютах на текущую дату.
        :param date: строка в формате '%d/%m/%y'
        :return: Возвращает словарь с ключами: date - дата полученных валют, content - список валют
        '''
        url = self.current_url
        xml = self._get_xml(url=url)
        data = self.__parse_xml(xml)

        return data
