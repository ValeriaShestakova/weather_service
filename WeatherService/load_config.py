"""
Module to load config files
"""
import yaml
import logging

logger = logging.getLogger('WeatherService.load_config')


class Config:

    def __init__(self):
        self._path = 'config/config.yml'
        self._config = self._load_config()
        logger.info('Init config')

    def _load_config(self):
        with open(self._path, 'r') as f:
            config = yaml.load(f)
        for key, value in config.items():
            setattr(self, key, value)
        logger.info('Loaded config')

        return config


if __name__ == '__main__':
    config = Config()
    print(config.city)

