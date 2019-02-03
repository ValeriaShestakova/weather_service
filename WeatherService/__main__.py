# -*- coding: utf-8 -*-
"""
Weather service
Entry point to module

"""
import logging.config
from WeatherService.daemon_service import DaemonService

logging.config.fileConfig('../config/logging.conf')
logger = logging.getLogger('WeatherService')


def main():
    logger.info("Program started")
    daemon_service = DaemonService()
    logger.info("Proceed main daemon service")
    daemon_service.proceed_weather()
    logger.info("Success!")


if __name__ == '__main__':
    main()
