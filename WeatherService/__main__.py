import logging.config
from WeatherService.weather_service import weather_service


logging.config.fileConfig('../config/logging.conf')
logger = logging.getLogger('WeatherService')


def main():
    logger.info("Program started")
    weather_service.get_days_data_from_db(30)


if __name__ == '__main__':
    main()
