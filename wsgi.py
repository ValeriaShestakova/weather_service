import os

from flask_restful import Api
from WeatherService import app
from WeatherService.weather_api import WeatherAPI, HomePage, load_new_data
import threading

t = threading.Thread(target=load_new_data, daemon=True)
t.start()
t.join()

api = Api(app)
api.add_resource(WeatherAPI, '/weather_service/get_data')
api.add_resource(HomePage, '/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='127.0.0.1', port=port, debug=True)
