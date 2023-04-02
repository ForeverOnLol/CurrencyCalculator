import pytest
from freezegun import freeze_time

from common.models import ValuteConv, ValuteAnalize
from db import SQLiteDB
from common.orm import ValutePrice, Valute, ValuteByDay
from common.scrapper import CbrScrapper
from common.required_date import RequiredDate
from gui.ui import GUI
from manage import ValuteManager


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

        valute1 = Valute(id='123zx', name='Aidro', num_code=222, char_code='2323', nominal=222)
        valute1.create()
        assert Valute.all() == [valute1]

        valute2 = Valute(id='123z2', name='Aidro', num_code=222, char_code='2323', nominal=222)
        valute2.create()
        assert Valute.all() == [valute1]

        valute3 = Valute(id='123z2', num_code=222, char_code='2323', name='Aidro2', nominal=222)
        valute3.create()
        assert Valute.all() == [valute1, valute3]


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


class TestValuteByDay:
    def test_get(self, run_db):
        value_id = '123sd'
        date1 = '27/04/2022'
        date2 = '26/04/2022'

        valute = Valute(id=value_id, num_code=222, char_code='2323', name='Aidro', nominal=222)
        valute.create()

        valute_price1 = ValutePrice(value=27.2, date=date1, valute_id=value_id)
        valute_price1.create()
        valute_price2 = ValutePrice(value=100.0, date=date2, valute_id=value_id)
        valute_price2.create()

        result = ValuteByDay.get(valute_id=value_id, date=date1)
        assert result == ValuteByDay(valute=valute, valute_data=valute_price1)
        result = ValuteByDay.get(valute_id=value_id, date=date2)
        assert result == ValuteByDay(valute=valute, valute_data=valute_price2)

    def test_all(self, run_db):
        date = '27/04/2022'
        valute_name1 = 'Terrix'
        valute_name2 = 'Aidro'
        valute_id1 = '22'
        valute_id2 = '22R'

        valute1 = Valute(id=valute_id1, num_code=222, char_code='2323', name=valute_name1, nominal=222)
        valute1.create()

        valute2 = Valute(id=valute_id2, num_code=222, char_code='2323', name=valute_name2, nominal=222)
        valute2.create()

        valute_price1 = ValutePrice(value=27.2, date=date, valute_id=valute_id1)
        valute_price1.create()
        valute_price2 = ValutePrice(value=100.0, date=date, valute_id=valute_id2)
        valute_price2.create()

        result = ValuteByDay.all(date=date)
        assert result == [ValuteByDay(valute=valute1, valute_data=valute_price1),
                          ValuteByDay(valute=valute2, valute_data=valute_price2)]


class TestRequiredDate:
    @freeze_time('2023-02-17')
    def test_last_weeks(self):
        result = RequiredDate.last_weeks()
        assert result[-1] == '17/02/2023'
        assert result[0] == '23/01/2023'

    @freeze_time('2023-02-17')
    def test_last_weeks_det(self):
        result = RequiredDate.last_weeks_detail()
        assert result['23/01/2023 - 29/01/2023'] == ['23/01/2023', '24/01/2023', '25/01/2023', '26/01/2023',
                                                     '27/01/2023', '28/01/2023', '29/01/2023']

    @freeze_time('2023-02-17')
    def test_last_months(self):
        result = RequiredDate.last_months()
        assert result[-1] == '17/02/2023'
        assert result[-11] == '07/02/2023'
        assert result[0] == '01/11/2022'

    @freeze_time('2023-02-17')
    def test_last_months_det(self):
        result = RequiredDate.last_months_detail()
        print(result)

    @freeze_time('2023-02-17')
    def test_last_quarts(self):
        result = RequiredDate.last_quarts()
        assert result[0] == '01/04/2022'
        assert result[-1] == '15/02/2023'

    @freeze_time('2023-02-17')
    def test_last_quarts_det(self):
        result = RequiredDate.last_quarts_detail()
        print(result)

    @freeze_time('2023-02-17')
    def test_last_years(self):
        result = RequiredDate.last_years()
        assert result[0] == '01/01/2020'
        assert result[-1] == '15/02/2023'

    @freeze_time('2023-02-17')
    def test_last_years(self):
        result = RequiredDate.all()

    @freeze_time('2023-02-17')
    def test_last_years_det(self):
        result = RequiredDate.last_quarts_detail()
        print(result)

    @freeze_time('2023-02-17')
    def test_today(self):
        result = RequiredDate.today()
        assert result == '17/02/2023'


class TestValuteConv:
    @freeze_time('2023-03-16')
    def test_today(self, run_db):
        valute1 = Valute(id='R1', num_code=222, char_code='2323', name='Евро', nominal=1)
        valute1.create()
        valute_price1 = ValutePrice(value=80.8763, date='16/03/2023', valute_id='R1')
        valute_price1.create()

        valute2 = Valute(id='R2', num_code=224, char_code='23232', name='Доллар США', nominal=1)
        valute2.create()
        valute_price2 = ValutePrice(value=75.7457, date='16/03/2023', valute_id='R2')
        valute_price2.create()

        assert 64.06407228397124 == ValuteConv.today('Евро', 'Доллар США', '60')

    @freeze_time('2023-03-16')
    def test_names(self, run_db):
        assert ['Российский рубль'] == ValuteConv.names()
        valute1 = Valute(id='R1', num_code=222, char_code='2323', name='Евро', nominal=1)
        valute1.create()
        valute_price1 = ValutePrice(value=80.8763, date='16/03/2023', valute_id='R1')
        valute_price1.create()

        valute2 = Valute(id='R2', num_code=224, char_code='23232', name='Доллар США', nominal=1)
        valute2.create()
        valute_price2 = ValutePrice(value=75.7457, date='16/03/2023', valute_id='R2')
        valute_price2.create()

        assert ['Российский рубль', 'Евро', 'Доллар США'] == ValuteConv.names()


class TestValuteAnalize:
    @freeze_time('2023-03-16')
    def test_periods(self, run_db):
        ValuteAnalize.period('Неделя')
        ValuteAnalize.period('Месяц')
        ValuteAnalize.period('Квартал')
        ValuteAnalize.period('Год')
