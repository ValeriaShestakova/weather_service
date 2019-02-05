"""
This is a module to get data from external application
"""
import grequests
import requests
import datetime
import logging

from WeatherService.weather_dao import WeatherDAO
from WeatherService.config_loader import Config
from WeatherService.daemon_service import DaemonService

logger = logging.getLogger('WeatherService.weather_service')


class WeatherService:

    def __init__(self):
        self._config = Config()
        self._city = self._config.city
        self._city_id = self._get_city_id()

    def _get_city_id(self):
        """
        Method for get location id
        :return: location id
        """
        response = requests.get(f'https://www.metaweather.com/api/location/search/?query={self._city}')
        data = response.json()
        return data[0]['woeid']

    def get_data_for_days(self, num_days):
        """
        Method for get weather data from api for a certain number of days
        :param num_days: days number
        :return: list data for some days, each element in json format
        """
        end_date = datetime.datetime.today()
        date_list = [end_date - datetime.timedelta(days=x) for x in range(0, num_days)]
        address = f'https://www.metaweather.com/api/location/{self._city_id}/'
        base = address+'{}'
        rs = (grequests.get(u) for u in [base.format(t.strftime("%Y/%m/%d")) for t in date_list])
        data = []
        for r in grequests.map(rs):
            data.extend(r.json())
        return data

    def _check_data(self, data, num_days=30):
        """
        Method for check data. Return true if data is full.
        :param data: lists of data
        :param num_days: number of days
        :return: True or False
        """
        logger.info('Check data')
        end_date = datetime.datetime.today()
        last_date = end_date - datetime.timedelta(days=num_days-1)
        if data[len(data)-1]['applicable_date'] != last_date.date().strftime("%Y-%m-%d"):
            daemon_service = DaemonService(self)
            daemon_service.proceed_weather(num_days)
            return False
        else:
            return True

    def get_data_from_db(self):
        """
        Method to get data from local database
        :return: list of weather data dicts
        """
        logger.info('Get data from db')
        weather_db = WeatherDAO()
        data = weather_db.get_data()
        checked_flag = self._check_data(data)
        if checked_flag is False:
            data = weather_db.get_data()
        return data


if __name__ == '__main__':
    Weather = WeatherService()

