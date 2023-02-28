import os
import sqlite3
import urllib.request
import xml.dom.minidom

from common.required_date import RequiredDate


class Database:
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

    def __create_dir(self) -> None:
        os.mkdir(self.dir_path)

    def __create_file(self) -> None:
        os.mknod(self.file_path)

    def __build_structure(self) -> None:
        with open('create_sqlite.sql', 'r') as sql_file:
            sql_script = sql_file.read()

        connection = sqlite3.connect(self.file_path)
        cursor = connection.cursor()
        cursor.executescript(sql_script)
        connection.commit()
        cursor.close()

    def run(self) -> None:
        if not self.__is_exist():
            self.__create_dir()
            self.__create_file()
            self.__build_structure()
        SQLiteDB.connection = sqlite3.connect(self.file_path)


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

        valute_list = sorted(Valute.all())

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
    def get_by_period(cls, period):
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
    '''
    Стоимость валюты за определённую дату
    '''

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
        try:
            cursor.execute(sql, [self.value, self.date, self.valute_id])
            db.commit()
        except sqlite3.IntegrityError:
            pass
        finally:
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

    @staticmethod
    def existing_dates():
        sql = ''' SELECT DISTINCT date FROM valute_price '''
        db = SQLiteDB.connection
        cursor = db.cursor()

        cursor.execute(sql)
        db.commit()
        data = cursor.fetchall()
        cursor.close()

        return data


class ValuteByDay:
    '''
    Информация о валюте и её данные за день.
    '''

    def __init__(self, valute: Valute, valute_data: ValutePrice):
        self.entity = valute
        self.data = valute_data


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
