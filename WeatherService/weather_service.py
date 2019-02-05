"""
This is a module to get data from db
"""

import datetime
import logging

from WeatherService.weather_dao import WeatherDAO
from WeatherService.daemon_service import DaemonService

logger = logging.getLogger('WeatherService.weather_service')


class WeatherService:

    def __init__(self):
        self._weather_db = WeatherDAO()

    def _check_data(self, data, num_days):
        """
        Method for check data. Return true if data is full.
        :param data: lists of data
        :param num_days: number of days
        :return: True or False
        """
        logger.info('Check data')
        end_date = datetime.datetime.today()
        last_date = end_date - datetime.timedelta(days=num_days-1)
        daemon_service = DaemonService()
        try:
            if data[len(data)-1]['applicable_date'] != last_date.date().strftime("%Y-%m-%d"):
                daemon_service.proceed_weather(num_days)
                return False
            else:
                return True
        except IndexError:
            daemon_service.proceed_weather(num_days)
            return False

    def get_day_data_from_db(self):
        """
        Method to get data from local database for one day
        :return: list of weather data dicts
        """
        logger.info('Get data from db')
        data = self._weather_db.get_data(num_days=1)
        if self._check_data(data, 1) is False:
            data = self._weather_db.get_data(num_days=1)
        return data

    def get_days_data_from_db(self, num_days):
        """
        Method to get data from local database for some days
        :return: list of weather data dicts
        """
        logger.info('Get data from db')
        data = self._weather_db.get_data(num_days)
        if self._check_data(data, num_days) is False:
            data = self._weather_db.get_data(num_days)
        return data


if __name__ == '__main__':
    Weather = WeatherService()

