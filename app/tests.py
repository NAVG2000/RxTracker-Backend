import unittest
import drugClass
import graphClass
import importerClass
import modelClass
import seasonality as seasonality
import holidays
import datetime
import pandas as pd


class TestSuite(unittest.TestCase):
    def test_seasonality_holidays(self):
        seasonalityFridayHolidays = seasonality.generate_holidays(2017, 2022)

        fridayHolidayDates = [
            # 2017 Fridays closest to holiday
            datetime.datetime.strptime("2017-01-06", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2017-01-20", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2017-02-24", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2017-06-02", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2017-07-07", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2017-09-08", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2017-10-13", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2017-11-17", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2017-11-24", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2017-12-29", "%Y-%m-%d").date(),
            # 2018 Fridays closest to holiday
            datetime.datetime.strptime("2018-01-05", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2018-01-19", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2018-02-23", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2018-06-01", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2018-07-06", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2018-09-07", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2018-10-12", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2018-11-16", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2018-11-23", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2018-12-28", "%Y-%m-%d").date(),
            # 2019 Fridays closest to holiday
            datetime.datetime.strptime("2019-01-04", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2019-01-25", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2019-02-22", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2019-05-31", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2019-07-05", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2019-09-06", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2019-10-18", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2019-11-15", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2019-11-29", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2019-12-27", "%Y-%m-%d").date(),
            # 2020 Fridays closest to holiday
            datetime.datetime.strptime("2020-01-03", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2020-01-24", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2020-02-21", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2020-05-29", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2020-07-10", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2020-09-11", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2020-10-16", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2020-11-13", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2020-11-27", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2020-12-25", "%Y-%m-%d").date(),
            # 2021 Fridays closest to holiday
            datetime.datetime.strptime("2021-01-01", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2021-01-22", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2021-02-19", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2021-06-04", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2021-07-09", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2021-09-10", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2021-10-15", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2021-11-12", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2021-11-26", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2021-12-31", "%Y-%m-%d").date(),
            # 2022 Fridays closest to holiday
            datetime.datetime.strptime("2022-01-07", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2022-01-21", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2022-02-25", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2022-06-03", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2022-07-08", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2022-09-09", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2022-10-14", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2022-11-11", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2022-11-25", "%Y-%m-%d").date(),
            datetime.datetime.strptime("2022-12-30", "%Y-%m-%d").date(),
        ]
        fridayHolidays = pd.Series(fridayHolidayDates)
        self.assertTrue(fridayHolidays.equals(seasonalityFridayHolidays["ds"]))


if __name__ == "__main__":
    unittest.main()
