"""
Module for description RestApi functions
"""

from flask_restful import Resource
from WeatherService import app
from WeatherService.weather_service import WeatherService
from WeatherService.daemon_service import DaemonService

import threading

weather_service = WeatherService()


def load_new_data():
    threading.Timer(5, load_new_data).start()
    daemon_service = DaemonService(weather_service)
    daemon_service.proceed_weather()
    print('Proceed weather')


class WeatherAPI(Resource):
    def get(self):
        data = weather_service.get_data_from_db()
        return data


class HomePage(Resource):
    def get(self):
        return 'Hi, you are on page weather service. If you want get info about ' \
               'weather in SPb for month: /weather_service/get_data'


if __name__ == '__main__':
    app.run(debug=True)
