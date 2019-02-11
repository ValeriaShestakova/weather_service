"""
Module to load config parameters
"""
import yaml
import logging

LOGGER = logging.getLogger('WeatherService.load_config')


class Config:

    def __init__(self):
        self._path = 'config/config.yml'
        self._config = self._load_config()
        LOGGER.info('Init config')

    def _load_config(self):
        with open(self._path, 'r') as f:
            config = yaml.load(f)
        for key, value in config.items():
            setattr(self, key, value)
        LOGGER.info('Loaded config')

        return config


if __name__ == '__main__':
    config = Config()
    print(config.city)


config = Config()
