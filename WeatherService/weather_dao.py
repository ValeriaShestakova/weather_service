"""
Module for interaction with database
"""
import psycopg2
import datetime
import logging

from WeatherService.config import Config

logger = logging.getLogger('WeatherService.weather_dao')
config = Config()

QUERY_CREATE_TABLE = f"""CREATE TABLE if not exists {config.db_name}.{config.db_schema}.{config.db_table} 
                     (applicable_date DATE NOT NULL, 
                     created_time VARCHAR NOT NULL, PRIMARY KEY (applicable_date, created_time), 
                     weather_state_name VARCHAR NOT NULL, wind_direction_compass VARCHAR, min_temp FLOAT, 
                     max_temp FLOAT, the_temp FLOAT NOT NULL, wind_speed FLOAT, wind_direction FLOAT,
                     air_pressure FLOAT, humidity FLOAT, visibility FLOAT, predictability INTEGER); """


QUERY_INSERT = f"""INSERT INTO {config.db_name}.{config.db_schema}.{config.db_table} (applicable_date, created_time, 
                  weather_state_name, 
                  wind_direction_compass, min_temp, max_temp, the_temp, wind_speed, wind_direction, 
                  air_pressure, humidity, visibility, predictability)
                  VALUES (%(applicable_date)s, %(created_time)s, %(weather_state_name)s, 
                  %(wind_direction_compass)s, %(min_temp)s, %(max_temp)s, %(the_temp)s,
                  %(wind_speed)s, %(wind_direction)s, %(air_pressure)s, %(humidity)s,
                  %(visibility)s, %(predictability)s);
                  """

QUERY_SELECT = f'SELECT * FROM {config.db_name}.{config.db_schema}.{config.db_table} ' \
    f'WHERE applicable_date between %s and %s'

QUERY_DROP = f'DROP TABLE {config.db_name}.{config.db_schema}.{config.db_table}'

QUERY_CREATE_INDEX = f'CREATE INDEX if not exists idx_weather_date ' \
    f'ON {config.db_name}.{config.db_schema}.{config.db_table} (applicable_date);'

ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


class WeatherDAO:

    def __init__(self):
        self._connect_data = f'dbname={config.db_name}  user={config.user} password={config.password} host={config.host} ' \
            f'port={config.port}'
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

    def get_data(self, begin_date, end_date):
        """
        Method for get weather data from DB
        :param begin_date: begin date in range
        :param end_date: end date in range
        :return: lists of data in json format
        """
        logger.info('Get data from db')
        keys = ('applicable_date', 'created_time', 'weather_state_name', 'wind_direction_compass', 'min_temp',
                'max_temp', 'the_temp', 'wind_speed', 'wind_direction', 'air_pressure', 'humidity', 'visibility',
                'predictability')
        all_data = []
        with psycopg2.connect(self._connect_data) as conn:
            with conn.cursor() as cursor:
                cursor.execute(QUERY_SELECT, (begin_date, end_date))
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
                    data['created_time'] = datetime.datetime.strptime(data['created'], ISO_FORMAT).time().\
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
        """
        Method to create index for date field
        :return:
        """
        logger.info('Create index')
        with psycopg2.connect(self._connect_data) as conn:
            with conn.cursor() as cursor:
                cursor.execute(QUERY_CREATE_INDEX)


if __name__ == '__main__':
    WeatherDAO = WeatherDAO()
    print(WeatherDAO.get_data(datetime.date(2019, 2, 1), datetime.datetime.today()))
