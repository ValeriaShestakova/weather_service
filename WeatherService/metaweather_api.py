"""
This is a module to get data from external application
"""
import grequests
import requests
import datetime
import logging

from WeatherService.config import config

logger = logging.getLogger('WeatherService.metaweather_api')


class MetaWeatherAPI:

    def __init__(self):
        self._config = config
        self._address = self._config.api_address
        self._city = self._config.city
        self._city_id = self.get_city_id()
        self._date_format = "%Y/%m/%d"

    def get_city_id(self) -> int:
        """
        Method to get location id
        :return: location id
        """
        response = requests.get(self._address+f'search/?query={self._city}')
        data = response.json()
        try:
            woeid = data[0]['woeid']
        except IndexError as ex:
            print('Location name is not valid')
            raise ex
        return woeid

    def get_data_for_days(self, num_days: int) -> list:
        """
        Method for get weather data from api for a certain number of days
        :param num_days: days number
        :return: list data for some days, each element in json format
        """
        end_date = datetime.datetime.today()
        date_list = \
            [end_date - datetime.timedelta(days=x) for x in range(0, num_days)]
        base = self._address+str(self._city_id)+'/{}'
        rs = (grequests.get(u) for u in
              [base.format(t.strftime(self._date_format)) for t in date_list])
        data = []
        for r in grequests.map(rs):
            data.extend(r.json())
        return data

    def get_data_for_day(self) -> list:
        """
        Method for get weather data from api for one day
        :return: list data for day, each element in json format
        """
        date = datetime.datetime.today().strftime(self._date_format)
        response = requests.get(self._address+str(self._city_id)+'/'+date)
        data = response.json()
        return data


meta_weather_api = MetaWeatherAPI()


if __name__ == '__main__':
    Weather = MetaWeatherAPI()
