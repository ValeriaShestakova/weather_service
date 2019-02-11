"""
This is a module to get and check data from db
"""

import datetime
import logging

from WeatherService.weather_dao import weather_dao
from WeatherService.daemon_service import daemon_service

logger = logging.getLogger('WeatherService.weather_service')


class WeatherService:

    def __init__(self):
        self._weather_db = weather_dao

    @staticmethod
    def _create_date_range(num_days: int) -> tuple:
        """
        Method for creating date range on number of days
        :param num_days: number of days
        :return: begin date, end date
        """
        end_date = datetime.datetime.today()
        begin_date = end_date - datetime.timedelta(days=num_days - 1)
        return begin_date.date(), end_date

    def _check_data(self, data: list, num_days: int) -> bool:
        """
        Method for check data. Return true if data is full.
        :param data: lists of data
        :param num_days: number of days
        :return: True or False
        """
        logger.info('Check data')
        begin_date, end_date = self._create_date_range(num_days)
        try:
            if data[len(data)-1]['applicable_date'] != \
                    begin_date.strftime("%Y-%m-%d"):
                daemon_service.proceed_weather(num_days)
                return False
            else:
                return True
        except IndexError:
            daemon_service.proceed_weather(num_days)
            return False

    def get_day_data_from_db(self) -> list:
        """
        Method to get data from local database for one day
        :return: list of weather data dicts
        """
        logger.info('Get data from db')
        begin_date, end_date = self._create_date_range(1)
        data = self._weather_db.get_data(begin_date, end_date)
        if self._check_data(data, 1) is False:
            data = self._weather_db.get_data(begin_date, end_date)
        return data

    def get_days_data_from_db(self, num_days: int) -> list:
        """
        Method to get data from local database for some days
        :return: list of weather data dicts
        """
        logger.info('Get data from db')
        begin_date, end_date = self._create_date_range(num_days)
        data = self._weather_db.get_data(begin_date, end_date)
        if self._check_data(data, num_days) is False:
            data = self._weather_db.get_data(begin_date, end_date)
        return data


weather_service = WeatherService()


if __name__ == '__main__':
    Weather = WeatherService()

