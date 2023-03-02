from gui.interface import DesktopUI
from structures import ValuteManager
from db import SQLiteDB


class App():
    def run(self) -> None:
        '''
        Запуск приложения
        :return:
        '''
        db = SQLiteDB()
        db.run()
        ValuteManager.load_data_in_db()
        DesktopUI()


if __name__ == '__main__':
    '''
    Точка входа в программу.
    '''
    app = App().run()
