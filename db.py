import os
import sqlite3


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
