"""
Module to load new data and save data to db
"""
import threading
import logging

from WeatherService.weather_dao import WeatherDAO
from WeatherService.metaweather_api import MetaWeatherAPI

logger = logging.getLogger('WeatherService.daemon_service')


class DaemonService:

    def __init__(self):
        self._api_meta_weather = MetaWeatherAPI()
        self._db = WeatherDAO()
        logger.info('Init daemon')

    def proceed_weather(self, num_days=1):
        """
        Method for data record to DB
        :param num_days: number of days
        :return:
        """
        if num_days == 1:
            all_weather_data = self._api_meta_weather.get_data_for_day()
        else:
            all_weather_data = self._api_meta_weather.get_data_for_days(num_days)
        self._db.save_data(all_weather_data)

    def load_new_data(self):
        threading.Timer(43200, self.load_new_data).start()
        self.proceed_weather()


daemon_service = DaemonService()

