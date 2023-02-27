from structures import SQLiteDB, ValuteManager


class App():
    def run(self) -> None:
        '''
        Запуск приложения
        :return:
        '''
        db = SQLiteDB()
        db.run()
        ValuteManager.load_data_in_db()


if __name__ == '__main__':
    '''
    Точка входа в программу.
    '''
    app = App().run()
