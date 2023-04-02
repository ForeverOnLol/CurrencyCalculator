import sqlite3
from itertools import chain

from db import SQLiteDB


class Valute:
    def __init__(self, id, num_code, char_code, name, nominal):
        self.id = str(id)
        self.num_code = int(num_code)
        self.char_code = str(char_code)
        self.name = str(name)
        self.nominal = int(nominal)

    def __eq__(self, other):
        if self.id == other.id and self.num_code == other.num_code and self.char_code == other.char_code and self.name == other.name and self.nominal == other.nominal:
            return True
        else:
            return False

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
            print(f'Попытка добавить валюту, которая уже существует', (self.name,))
        finally:
            cursor.close()

    @classmethod
    def all(cls):
        sql = ''' SELECT * FROM valute '''

        db = SQLiteDB.connection
        cursor = db.cursor()

        cursor.execute(sql)
        db.commit()
        data = cursor.fetchall()
        cursor.close()
        return Valute.__format(fetch_result=data)

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

    @staticmethod
    def __format(fetch_result: list[tuple]) -> list:
        '''
        Форматирует результат fetchall в список объектов Valute.
        :return: list[Valute]
        '''
        result = []
        for valute in fetch_result:
            result.append(Valute(
                id=valute[0],
                num_code=valute[1],
                char_code=valute[2],
                nominal=valute[3],
                name=valute[4]
            )
            )
        return result


class ValutePrice:
    '''
    Стоимость валюты за определённую дату
    '''

    def __init__(self, value, date, valute_id):
        self.value = float(value)
        self.date = str(date)
        self.valute_id = valute_id

    def __eq__(self, other):
        if self.value == other.value and self.date == other.date and self.valute_id == other.valute_id:
            return True
        else:
            return False

    def create(self):
        sql = ''' INSERT INTO valute_price(value, date, valute_id)
              VALUES(?, ?, ?) '''
        db = SQLiteDB.connection
        cursor = db.cursor()
        try:
            cursor.execute(sql, [self.value, self.date, self.valute_id])
            db.commit()
        except sqlite3.IntegrityError:
            print(f'Попытка добавить данные по валюте, которые уже существуют: ',
                  (self.value, self.date, self.valute_id))
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

        return list(chain.from_iterable(data))


class ValuteByDay:
    '''
    Информация о валюте и её данные за день.
    '''

    def __init__(self, valute: Valute, valute_data: ValutePrice):
        self.entity = valute
        self.data = valute_data

    def __eq__(self, other):
        if self.entity == other.entity and self.data == other.data:
            return True
        else:
            return False

    @staticmethod
    def get(date: str, valute_id: None | str = None, name: None | str = None):
        '''
        Получает полную информацию о валюте по дате.
        :param valute_id:
        :param date:
        :return: ValuteByDay
        '''
        db = SQLiteDB.connection
        cursor = db.cursor()
        if valute_id:
            sql = ''' SELECT v.id, num_code, char_code, nominal, name, value, date
            FROM valute_price as vp INNER JOIN valute as v on vp.valute_id = v.id WHERE vp.date=? AND v.id=? '''
            cursor.execute(sql, (date, valute_id))
        elif name:
            sql = ''' SELECT v.id, num_code, char_code, nominal, name, value, date
                       FROM valute_price as vp INNER JOIN valute as v on vp.valute_id = v.id WHERE vp.date=? AND v.name=? '''
            cursor.execute(sql, (date, name))
        else:
            raise ValueError

        db.commit()
        data = cursor.fetchall()
        cursor.close()
        return ValuteByDay.__format(fetch_result=data)[0]

    @staticmethod
    def all(date: str) -> list:
        '''
        Получает полную информацию о всех валютах по дате.
        :param valute_id:
        :param date:
        :return: ValuteByDay
        '''
        sql = ''' SELECT v.id, num_code, char_code, nominal, name, value, date
                FROM valute_price as vp INNER JOIN valute as v on vp.valute_id=v.id WHERE vp.date=? '''
        db = SQLiteDB.connection
        cursor = db.cursor()

        cursor.execute(sql, (date,))
        db.commit()
        data = cursor.fetchall()
        cursor.close()

        return ValuteByDay.__format(fetch_result=data)

    @staticmethod
    def __format(fetch_result: list[tuple]) -> list:
        '''
        Форматирует результат fetchall в список объектов ValuteDate.
        :return: list[ValuteDate]
        '''
        result = []

        for entity in fetch_result:
            valute = Valute(
                id=entity[0],
                num_code=entity[1],
                char_code=entity[2],
                nominal=entity[3],
                name=entity[4]
            )
            valute_price = ValutePrice(
                valute_id=entity[0],
                value=entity[5],
                date=entity[6]
            )
            result.append(ValuteByDay(valute, valute_price))

        return result
