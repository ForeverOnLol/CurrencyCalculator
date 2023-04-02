import datetime

from common.required_date import num_month_to_name


def ticks_format(dates: list, period_name: str):
    period_name = period_name.lower()
    match period_name:
        case 'неделя':
            return dates
        case 'месяц':
            res = [dates[i] if i % 5 == 0 else '' for i in range(len(dates))]
            return res
        case 'квартал':
            return dates
        case 'год':
            res = []
            for i, date in enumerate(dates):
                year = date[5:]
                day = date[0:2]
                if (day == '01' or day == '15'):
                    if (day == '01'):
                        month = num_month_to_name(int(date[3:5]), short=True)
                        res.append(f'{month} {year}')
                    else:
                        res.append("")
            return res
