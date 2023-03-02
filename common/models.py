import sqlite3
from db import SQLiteDB


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
            print(f'Попытка добавить валюту, которая уже существует', (self.name,))
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

        return data


class ValuteByDay:
    '''
    Информация о валюте и её данные за день.
    '''

    def __init__(self, valute: Valute, valute_data: ValutePrice):
        self.entity = valute
        self.data = valute_data
