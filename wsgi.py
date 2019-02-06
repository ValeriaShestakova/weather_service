import os

from flask_restful import Api
from WeatherService import app
from WeatherService.weather_api import DayWeather, DaysWeather, HomePage, CityId


api = Api(app)
api.add_resource(DayWeather, '/weather_service/get_data_for_day')
api.add_resource(DaysWeather, '/weather_service/get_data_for_days/<num_days>')
api.add_resource(CityId, '/weather_service/get_city_id')
api.add_resource(HomePage, '/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='127.0.0.1', port=port, debug=True)
