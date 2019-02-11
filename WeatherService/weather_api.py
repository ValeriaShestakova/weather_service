"""
Module for description RestApi functions
"""

from flask_restful import Resource
from WeatherService import app
from WeatherService.weather_service import weather_service
from WeatherService.metaweather_api import meta_weather_api


class DayWeather(Resource):
    def get(self):
        data = weather_service.get_day_data_from_db()
        return data


class DaysWeather(Resource):
    def get(self, num_days):
        data = weather_service.get_days_data_from_db(num_days)
        return data


class CityId(Resource):
    def get(self):
        data = meta_weather_api.get_city_id()
        return data


class HomePage(Resource):
    def get(self):
        return 'Hi, you are on page weather service. ' \
               'If you want get info about ' \
               'weather in SPb for one day: ' \
               '/weather_service/get_data_for_day, for days: ' \
               '/weather_service/get_data_for_days/{num_days}. ' \
               'To get city id: /weather_service/get_city_id'


if __name__ == '__main__':
    app.run(debug=True)
