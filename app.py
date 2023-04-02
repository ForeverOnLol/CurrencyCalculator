from gui.ui import run_desktop
from manage import ValuteManager
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
        run_desktop()


if __name__ == '__main__':
    '''
    Точка входа в программу.
    '''
    app = App().run()
