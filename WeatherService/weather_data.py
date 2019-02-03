import requests
import datetime


class WeatherData:

    def __init__(self, city):
        self._city = city
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
        data = []
        for date in date_list:
            response = requests.get(f'https://www.metaweather.com/api/'
                                    f'location/{self._city_id}/{date.strftime("%Y/%m/%d")}')
            day_data = response.json()
            data.extend(day_data)
        return data


if __name__ == '__main__':
    Weather = WeatherData('St Petersburg')

