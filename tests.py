import pytest
from freezegun import freeze_time

from db import SQLiteDB
from common.models import ValutePrice, Valute
from common.scrapper import CbrScrapper
from common.required_date import RequiredDate


@pytest.fixture
def run_db(tmpdir):
    db_file_name = 'test_db.sqlite'
    db_dir_path = tmpdir + '/sqlite'

    db = SQLiteDB(db_file_name=db_file_name, db_dir_path=str(db_dir_path))
    db.run()


class TestSQLiteDB:
    pass


class TestCbrScrapper:

    def test_get(self):
        scrapper = CbrScrapper(date='27/04/2022')
        res = scrapper.get()
        print(res)


class TestValute:
    def test_create(self, run_db):
        Valute(id='123sd', num_code=222, char_code='2323', name='Aidro', nominal=222).create()
        Valute(id='123zx', num_code=222, char_code='2323', name='Aidro', nominal=222).create()
        Valute(id='123zx', num_code=222, char_code='2323', name='Aidro', nominal=222).create()

    def test_all(self, run_db):
        assert Valute.all() == []
        Valute(id='123zx', num_code=222, char_code='2323', name='Aidro', nominal=222).create()
        assert Valute.all() == [('123zx', 222, '2323', 222, 'Aidro')]
        Valute(id='123z2', num_code=222, char_code='2323', name='Aidro', nominal=222).create()
        assert Valute.all() == [('123zx', 222, '2323', 222, 'Aidro'), ('123z2', 222, '2323', 222, 'Aidro')]


class TestValutePrice:
    def test_create(self, run_db):
        value_id = '123sd'
        valute = Valute(id=value_id, num_code=222, char_code='2323', name='Aidro', nominal=222).create()
        ValutePrice(value='27.2', date='27/04/2022', valute_id=value_id).create()

        value_id = '123sd'
        valute = Valute(id=value_id, num_code=222, char_code='2323', name='Aidro', nominal=222).create()
        ValutePrice(value='27.2', date='27/04/2022', valute_id=value_id).create()


    def test_get(self, run_db):
        date = '27/04/2022'
        valute_id = '123sd'

        Valute(id=valute_id, num_code=222, char_code='2323', name='Aidro', nominal=222).create()
        ValutePrice(value='27.2', date=date, valute_id=valute_id).create()

        ValutePrice.get(date=date, valute_id=valute_id)


class TestRequiredDate:
    @freeze_time('2023-02-17')
    def test_last_weeks(self):
        result = RequiredDate.last_weeks()
        assert result[-1] == '17/02/2023'
        assert result[0] == '23/01/2023'

    @freeze_time('2023-02-17')
    def test_last_months(self):
        result = RequiredDate.last_months()
        assert result[-1] == '17/02/2023'
        assert result[-11] == '07/02/2023'
        assert result[0] == '01/11/2022'

    @freeze_time('2023-02-17')
    def test_last_quarts(self):
        result = RequiredDate.last_quarts()
        assert result[0] == '01/04/2022'
        assert result[-1] == '15/02/2023'

    @freeze_time('2023-02-17')
    def test_last_years(self):
        result = RequiredDate.last_years()
        assert result[0] == '01/01/2020'
        assert result[-1] == '15/02/2023'

    @freeze_time('2023-02-17')
    def test_last_years(self):
        result = RequiredDate.all()