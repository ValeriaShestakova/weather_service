"""
Module to load and save data to db
"""
from WeatherService.weather_dao import WeatherDAO


class DaemonService:

    def __init__(self, weather_service):
        self._weather_service = weather_service

    def proceed_weather(self, num_days=1):
        """
        Method for data record to DB
        :param num_days: number of days
        :return:
        """
        all_weather_data = self._weather_service.get_data_for_days(num_days)
        db = WeatherDAO()
        db.save_data(all_weather_data)


