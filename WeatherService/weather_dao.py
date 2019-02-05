"""
Module for interaction with database
"""
import psycopg2
import datetime
import logging

from WeatherService.load_config import Config

logger = logging.getLogger('WeatherService.weather_dao')

QUERY_CREATE_TABLE = """CREATE TABLE if not exists weather_data (applicable_date DATE NOT NULL, 
                     created_time VARCHAR NOT NULL, PRIMARY KEY (applicable_date, created_time), 
                     weather_state_name VARCHAR NOT NULL, wind_direction_compass VARCHAR, min_temp FLOAT, 
                     max_temp FLOAT, the_temp FLOAT NOT NULL, wind_speed FLOAT, wind_direction FLOAT,
                     air_pressure FLOAT, humidity FLOAT, visibility FLOAT, predictability INTEGER); """

QUERY_SELECT = 'SELECT * FROM weather_data WHERE applicable_date=%s'

QUERY_INSERT = """INSERT INTO weather_data (applicable_date, created_time, weather_state_name, 
                  wind_direction_compass, min_temp, max_temp, the_temp, wind_speed, wind_direction, 
                  air_pressure, humidity, visibility, predictability)
                  VALUES (%(applicable_date)s, %(created_time)s, %(weather_state_name)s, 
                  %(wind_direction_compass)s, %(min_temp)s, %(max_temp)s, %(the_temp)s,
                  %(wind_speed)s, %(wind_direction)s, %(air_pressure)s, %(humidity)s,
                  %(visibility)s, %(predictability)s);
                  """

QUERY_DROP = 'DROP TABLE weather_data CASCADE'

QUERY_CREATE_INDEX = 'CREATE INDEX if not exists idx_weather_date ON weather_data (applicable_date);'


class WeatherDAO:

    def __init__(self):
        self._config = Config()
        self._connect_data = f'dbname={self._config.db_name}  user={self._config.user} password={self._config.password} ' \
            f'host={self._config.host} port={self._config.port}'
        self._create_table()
        self._create_index()
        logger.info('Init db')

    def _create_table(self):
        """
        Method for create table where weather data will be saved
        :return:
        """
        logger.info('Create table')
        with psycopg2.connect(self._connect_data) as conn:
            with conn.cursor() as cursor:
                cursor.execute(QUERY_CREATE_TABLE)

    def get_data(self, num_days=30):
        """
        Method for get weather data from DB
        :param num_days: days number
        :return:
        """
        logger.info('Get data from db')
        keys = ('applicable_date', 'created_time', 'weather_state_name', 'wind_direction_compass', 'min_temp',
                'max_temp', 'the_temp', 'wind_speed', 'wind_direction', 'air_pressure', 'humidity', 'visibility',
                'predictability')
        end_date = datetime.datetime.today()
        date_list = [end_date - datetime.timedelta(days=x) for x in range(0, num_days)]
        all_data = []
        with psycopg2.connect(self._connect_data) as conn:
            for date in date_list:
                with conn.cursor() as cursor:
                    cursor.execute(QUERY_SELECT, (date.date(),))
                    for row in cursor:
                        dictionary = dict(zip(keys, row))
                        app_date = dictionary['applicable_date']
                        dictionary['applicable_date'] = app_date.strftime("%Y-%m-%d")
                        all_data.append(dictionary)
        return all_data

    def save_data(self, weather_data):
        """
        Method for save weather data to db
        :param weather_data: lists of weather data in json
        :return:
        """
        logger.info('Save data to db')
        with psycopg2.connect(self._connect_data) as conn:
            with conn.cursor() as cursor:
                for data in weather_data:
                    data['created_time'] = datetime.datetime.strptime(data['created'], "%Y-%m-%dT%H:%M:%S.%fZ").time().\
                        strftime('%H:%M:%S')
                    try:
                        cursor.execute(QUERY_INSERT, data)
                    except psycopg2.IntegrityError:
                        cursor.execute('ROLLBACK;')

    def _delete_table(self):
        """
        Method to drop the table
        :return:
        """
        logger.info('Delete table')
        with psycopg2.connect(self._connect_data) as conn:
            with conn.cursor() as cursor:
                cursor.execute(QUERY_DROP)

    def _create_index(self):
        logger.info('Create index')
        with psycopg2.connect(self._connect_data) as conn:
            with conn.cursor() as cursor:
                cursor.execute(QUERY_CREATE_INDEX)


if __name__ == '__main__':
    WeatherDAO = WeatherDAO()
    WeatherDAO.get_data()
