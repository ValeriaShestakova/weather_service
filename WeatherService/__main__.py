import logging.config
from WeatherService.daemon_service import DaemonService
from WeatherService.weather_service import WeatherService


logging.config.fileConfig('config/logging.conf')
logger = logging.getLogger('WeatherService')


def main():
    weather_service = WeatherService()
    logger.info("Program started")
    daemon_service = DaemonService(weather_service)
    logger.info("Proceed main daemon service")
    daemon_service.proceed_weather()
    logger.info("Success!")
    print(weather_service.get_data_from_db())


if __name__ == '__main__':
    main()
