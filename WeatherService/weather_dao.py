import psycopg2
import datetime

from WeatherService.config_loader import Config


class WeatherDAO:

    def __init__(self):
        self._config = Config()
        self._connect_data = f'dbname={self._config.db_name}  user={self._config.user} password={self._config.password} ' \
            f'host={self._config.host} port={self._config.port}'
        self._create_table()

    def _create_table(self):
        with psycopg2.connect(self._connect_data) as conn:
            with conn.cursor() as cursor:
                cursor.execute('CREATE TABLE if not exists weather_data'
                               '(id serial PRIMARY KEY, applicable_date DATE NOT NULL, created_time VARCHAR, '
                               'weather_state_name VARCHAR NOT NULL, wind_direction_compass VARCHAR, min_temp FLOAT, '
                               'max_temp FLOAT, the_temp FLOAT NOT NULL, wind_speed FLOAT, wind_direction FLOAT,'
                               'air_pressure FLOAT, humidity FLOAT, visibility FLOAT, predictability INTEGER);')

    def get_data(self):
        with psycopg2.connect(self._connect_data) as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM weather_data')
                for row in cursor:
                    print(row)

    def save_data(self, weather_data):
        with psycopg2.connect(self._connect_data) as conn:
            with conn.cursor() as cursor:
                for data in weather_data:
                    data['created_time'] = datetime.datetime.strptime(data['created'], "%Y-%m-%dT%H:%M:%S.%fZ").time().\
                        strftime('%H:%M:%S')
                    cursor.execute("""
                                            INSERT INTO weather_data (applicable_date, created_time, weather_state_name, wind_direction_compass,
                                              min_temp, max_temp, the_temp, wind_speed, wind_direction, air_pressure, humidity, visibility,
                                              predictability)
                                            VALUES (%(applicable_date)s, %(created_time)s, %(weather_state_name)s, 
                                            %(wind_direction_compass)s, %(min_temp)s, %(max_temp)s, %(the_temp)s,
                                             %(wind_speed)s, %(wind_direction)s, %(air_pressure)s, %(humidity)s,
                                              %(visibility)s, %(predictability)s);
                                            """, data)

    def _delete_table(self):
        with psycopg2.connect(self._connect_data) as conn:
            with conn.cursor() as cursor:
                cursor.execute('DROP TABLE weather_data CASCADE')


if __name__ == '__main__':
    WeatherDAO = WeatherDAO()
    WeatherDAO.get_data()
