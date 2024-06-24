"""
Modern sensor replacement: https://learn.adafruit.com/modern-replacements-for-dht11-dht22-sensors
"""

import adafruit_ahtx0
import board
import busio
import pymysql
from datetime import datetime
import config
import sys

def round_num(input):
    return '{:.2f}'.format(input)

def write_to_database(connection, timestamp, temperature, relative_humidity, sensor_type="aht20"):
    try:
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO temperaturedata (dateandtime, sensor, temperature, humidity)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (timestamp, sensor_type, temperature, relative_humidity))
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error inserting data into the database: {e}")

def main():
    # Load database configuration
    try:
        db_config = config.DATABASE
    except AttributeError as e:
        print("Error reading database configuration:", e)
        sys.exit(1)

    # Establish database connection
    try:
        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.MySQLError as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)

    try:
        # Create I2C bus interface
        i2c = busio.I2C(board.SCL, board.SDA)

        # Create sensor object
        try:
            sensor = adafruit_ahtx0.AHTx0(i2c)
        except Exception as e:
            print(f"Error initializing sensor: {e}")
            connection.close()
            sys.exit(1)

        # Basic data retrieval
        try:
            temperature = float(round_num(sensor.temperature))
            relative_humidity = float(round_num(sensor.relative_humidity))
        except Exception as e:
            print(f"Error reading sensor data: {e}")
            connection.close()
            sys.exit(1)

        timestamp = datetime.now()

        # Write to database
        write_to_database(connection, timestamp, temperature, relative_humidity)

        #print(f"Temperature: {temperature} °C")
        #print(f"Humidity: {relative_humidity} %")

    except Exception as main_e:
        print(f"Unexpected error: {main_e}")
    finally:
        connection.close()

if __name__ == "__main__":
    main()
