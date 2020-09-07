import datetime
import holidays
import pandas as pd


def holiday_to_friday(holiday):
    while holiday.weekday() != 4:
        holiday += datetime.timedelta(1)
    return holiday


def holidays_dict_to_df(holidays_list):
    holidays_df = pd.DataFrame(list(holidays_list.items()), columns=["ds", "holiday"])
    for i in range(len(holidays_df)):
        holidays_df["ds"][i] = holiday_to_friday(holidays_df["ds"][i])
    holidays_df["upper_window"] = 7
    holidays_df["lower_window"] = 0
    return holidays_df


def generate_holidays(start_year, end_year):
    year_range = range(start_year, end_year + 1)
    us_holidays = holidays.UnitedStates(years=year_range, observed=False)
    holidays_df = holidays_dict_to_df(us_holidays)
    return holidays_df


def is_holiday(day):
    day = datetime.datetime.strptime(day, "%Y-%m-%d").date()
    us_holidays = holidays.UnitedStates(years=[day.year])
    us_holidays_friday = list(map(holiday_to_friday, us_holidays))
    return day in us_holidays_friday
