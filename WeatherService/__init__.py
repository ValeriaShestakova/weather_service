from gevent import monkey
monkey.patch_all()

from flask import Flask
from WeatherService.daemon_service import DaemonService
import threading


def create_app():
    daemon_service = DaemonService()
    t = threading.Thread(target=daemon_service.load_new_data, daemon=True)
    t.start()
    t.join()
    return Flask(__name__)


app = create_app()


@app.errorhandler(404)
def page_not_found(e):
    message = '<h3>Page not found.</h3> <h3>Available requests: </h3>' \
              '/weather_service/get_data_for_day - to get data for day <br>' \
               '/weather_service/get_data_for_days/{num_days} - to get data for days <br>' \
              '/weather_service/get_city_id - to get location id'
    return message, 404


app.register_error_handler(404, page_not_found)

