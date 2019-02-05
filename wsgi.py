import os

from gevent import monkey
monkey.patch_all()

from flask_restful import Api
from WeatherService import app
from WeatherService.daemon_service import DaemonService
from WeatherService.weather_api import DayWeather, DaysWeather, HomePage, CityId
import threading

daemon_service = DaemonService()
t = threading.Thread(target=daemon_service.load_new_data, daemon=True)
t.start()
t.join()


api = Api(app)
api.add_resource(DayWeather, '/weather_service/get_data_for_day')
api.add_resource(DaysWeather, '/weather_service/get_data_for_days/<int:num_days>')
api.add_resource(CityId, '/weather_service/get_city_id')
api.add_resource(HomePage, '/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='127.0.0.1', port=port, debug=True)
