"""
Module for description RestApi functions
"""

from flask_restful import Resource
from WeatherService import app
from WeatherService.weather_service import WeatherService
from WeatherService.metaweather_api import MetaWeatherAPI


from flask import jsonify


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


class DayWeather(Resource):
    def get(self):
        weather_service = WeatherService()
        data = weather_service.get_day_data_from_db()
        return data


class DaysWeather(Resource):
    def get(self, num_days):
        if type(num_days) is not int:
            raise InvalidUsage('Parameter num_days must be positive integer!', status_code=410)
        weather_service = WeatherService()
        data = weather_service.get_days_data_from_db(num_days)
        return data


class CityId(Resource):
    def get(self):
        meta_weather_api = MetaWeatherAPI()
        data = meta_weather_api.get_city_id()
        return data


class HomePage(Resource):
    def get(self):
        return 'Hi, you are on page weather service. If you want get info about ' \
               'weather in SPb for one day: /weather_service/get_data_for_day, for days: ' \
               '/weather_service/get_data_for_days/{num_days}. To get city id: /weather_service/get_city_id'


if __name__ == '__main__':
    app.run(debug=True)
