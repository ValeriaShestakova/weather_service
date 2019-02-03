import yaml


class Config:

    def __init__(self):
        self._path = '../config/config.yml'
        self._config = self._config_load()

    def _config_load(self):
        with open(self._path, 'r') as f:
            config = yaml.load(f)
        for key, value in config.items():
            setattr(self, key, value)
        return config


if __name__ == '__main__':
    config = Config()
    print(config.city)

