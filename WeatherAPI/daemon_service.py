import requests

from WeatherAPI.config_loader import Config


class DaemonService:

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

    def get_data_for_date(self, date):
        """
        Method for get weather data from api for special date
        :param date: Date in the format yyyy/mm/dd
        :return: data for one day
        """
        response = requests.get(f'https://www.metaweather.com/api/location/{self._city_id}/{date}')
        data = response.json()
        return data


if __name__ == '__main__':
    DaemonService = DaemonService()
    # print(DaemonService.get_data_for_date('2017/04/02'))
