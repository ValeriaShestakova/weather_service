import logging.config
from WeatherService.daemon_service import DaemonService
from WeatherService.weather_service import WeatherService


logging.config.fileConfig('../config/logging.conf')
logger = logging.getLogger('WeatherService')


def main():
    weather_service = WeatherService()
    logger.info("Program started")
    logger.info("Success!")
    weather_service.get_days_data_from_db(2)


if __name__ == '__main__':
    main()
