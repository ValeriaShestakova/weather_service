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
