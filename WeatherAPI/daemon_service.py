
from WeatherAPI.config_loader import Config
from WeatherAPI.weather_data import WeatherData
from WeatherAPI.weather_dao import WeatherDAO


class DaemonService:

    def __init__(self):
        self._config = Config()
        self._city = self._config.city

    def proceed_weather(self, num_days=1):
        """
        Method for data record to DB
        :param num_days: number of days
        :return:
        """
        weather_data = WeatherData(self._city)
        all_weather_data = weather_data.get_data_for_days(num_days)
        db = WeatherDAO()
        db.save_data(all_weather_data)


if __name__ == '__main__':
    DaemonService = DaemonService()
    DaemonService.proceed_weather()
