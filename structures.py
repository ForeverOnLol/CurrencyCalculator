import os
import sqlite3
import urllib.request
import xml.dom.minidom

from datequarter import DateQuarter
from dateutil.relativedelta import relativedelta
from datetime import datetime
import datetime


class Database():
    pass


class SQLiteDB(Database):
    file_name = None
    dir_path = None
    file_path = None
    connection = None

    def __init__(self, db_file_name: str = 'sqlite_database.db',
                 db_dir_path: str = os.getcwd() + '/sqlite'
                 ):
        SQLiteDB.file_name = db_file_name
        SQLiteDB.dir_path = db_dir_path
        SQLiteDB.file_path = self.dir_path + '/' + self.file_name

    def __is_exist(self):
        return os.path.isfile(self.file_path)

    def __create_dir(self):
        os.mkdir(self.dir_path)

    def __create_file(self):
        os.mknod(self.file_path)

    def __build_structure(self):
        with open('create_sqlite.sql', 'r') as sql_file:
            sql_script = sql_file.read()

        connection = sqlite3.connect(self.file_path)
        cursor = connection.cursor()
        cursor.executescript(sql_script)
        connection.commit()
        cursor.close()

    def run(self):
        if not self.__is_exist():
            self.__create_dir()
            self.__create_file()
            self.__build_structure()
        SQLiteDB.connection = sqlite3.connect(self.file_path)


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


class ValuteManager:
    @staticmethod
    def load_data_in_db():
        '''
        Подгрузка данных в БД при каждом запуске приложения.
        :return: None
        '''
        date_list = RequiredDate.all()
        valute_list = sorted(Valute.all())

        if not len(valute_list):
            for date in date_list:
                valute_by_day_list = CbrScrapper(date=date).get()

                for valute in valute_by_day_list:
                    valute.entity.create()
                    valute.data.create()
        else:
            pass


class Valute:
    def __init__(self, id, num_code, char_code, name, nominal):
        self.id = str(id)
        self.num_code = int(num_code)
        self.char_code = str(char_code)
        self.name = str(name)
        self.nominal = int(nominal)

    def __is_exist(self, valute_id):
        sql = ' SELECT valute.id FROM valute WHERE valute.id={} '.format(valute_id)

        db = SQLiteDB.connection
        cursor = db.cursor()

        cursor.execute(sql)
        db.commit()
        cursor.close()

    def create(self):
        sql = ''' INSERT INTO valute(id, num_code, char_code, nominal, name)
                  VALUES(?, ?,?,?,?) '''
        db = SQLiteDB.connection
        cursor = db.cursor()
        try:
            cursor.execute(sql, [self.id, self.num_code, self.char_code, self.nominal, self.name])
            db.commit()
        except sqlite3.IntegrityError:
            pass
        finally:
            cursor.close()

    @staticmethod
    def all():
        sql = ''' SELECT * FROM valute '''

        db = SQLiteDB.connection
        cursor = db.cursor()

        cursor.execute(sql)
        db.commit()
        data = cursor.fetchall()
        cursor.close()
        return data

    @staticmethod
    def is_exist_any():
        sql = ''' SELECT * FROM valute '''

        db = SQLiteDB.connection
        cursor = db.cursor()

        cursor.execute(sql)
        db.commit()
        data = cursor.fetchall()
        cursor.close()
        return data


class ValutePrice:
    def __init__(self, value, date, valute_id):
        self.value = float(value)
        self.date = str(date)
        self.valute_id = valute_id

    def __is_exist(self, valute_id: str):
        pass

    def create(self):
        sql = ''' INSERT INTO valute_price(value, date, valute_id)
                  VALUES(?, ?, ?) '''
        db = SQLiteDB.connection
        cursor = db.cursor()

        cursor.execute(sql, [self.value, self.date, self.valute_id])
        db.commit()
        cursor.close()

    @staticmethod
    def get(date, valute_id):
        sql = ''' SELECT * FROM valute_price WHERE date=? AND valute_id=? '''
        db = SQLiteDB.connection
        cursor = db.cursor()

        cursor.execute(sql, (date, valute_id))
        db.commit()
        data = cursor.fetchall()
        cursor.close()

        return data


class ValuteByDay:
    def __init__(self, valute: Valute, valute_data: ValutePrice):
        self.entity = valute
        self.data = valute_data


class Scrapper:
    @staticmethod
    def _get_xml(url: str):
        return urllib.request.urlopen(url)


class CbrScrapper(Scrapper):
    url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req={}'

    def __init__(self, date):
        self.date = date
        self.current_url = self.__format_url(date)

    @classmethod
    def __format_url(cls, date: str):
        return cls.url.format(date)

    def __parse_xml(self, cbr_xml):
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
