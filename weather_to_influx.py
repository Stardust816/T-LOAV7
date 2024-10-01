#!/usr/bin/env python3
import requests
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import time

# InfluxDB settings
influxdb_url = 'http://<IPADDRESS>:8086'
influxdb_token = '<INFLUXDBTOKEN>'
influxdb_org = '<Organization>'
influxdb_bucket = '<Bucket>'

# OpenWeatherMap API settings
owm_api_key = '<APIKEY>'
owm_lat = '<LAT>'
owm_lon = '<LON>'
owm_url = f'http://api.openweathermap.org/data/2.5/weather?lat={owm_lat}&lon={owm_lon}&appid={owm_api_key}&units=metric'

# InfluxDB Client
client = InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
write_api = client.write_api(write_options=SYNCHRONOUS)

try:
    while True:
        response = requests.get(owm_url)
        if response.status_code == 200:
            weather_data = response.json()
            point = Point("weather")
            point.tag("location", "Fischamend Dorf")
            point.tag("country", weather_data['sys']['country'])
            point.field("longitude", weather_data['coord']['lon'])
            point.field("latitude", weather_data['coord']['lat'])
            point.field("weather_id", weather_data['weather'][0]['id'])
            point.field("main", weather_data['weather'][0]['main'])
            point.field("description", weather_data['weather'][0]['description'])
            point.field("base", weather_data['base'])
            point.field("temperature",weather_data['main']['temp'])
            point.field("temperature",weather_data['main']['temp'])
            point.field("feels_like", weather_data['main']['feels_like'])
            point.field("temp_min",weather_data['main']['temp_min'])
            point.field("temp_max",weather_data['main']['temp_max'])
            point.field("pressure",weather_data['main']['pressure'])
            point.field("humidity",weather_data['main']['humidity'])
            point.field("visibility",weather_data['visibility'])
            point.field("wind_speed",weather_data['wind']['speed'])
            point.field("wind_deg",weather_data['wind']['deg'])
            point.field("dt",weather_data['dt'])
            point.field("sys_type",weather_data['sys']['type'])
            point.field("sys_id",weather_data['sys']['id'])
            point.field("sunrise",weather_data['sys']['sunrise'])
            point.field("sunset",weather_data['sys']['sunset'])
            point.field("timezone",weather_data['timezone'])
            point.field("city_id",weather_data['id'])
            point.field("city_name",weather_data['name'])
            point.time(datetime.utcnow(), WritePrecision.NS)
          
            write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=point)
          
            print("Wetterdaten erfolgreich in InfluxDB gespeichert.")
          
        else:
            print(f"Fehler beim Abrufen der Wetterdaten: Statuscode{response.status_code}")
        time.sleep(5)
except KeyboardInterrupt:
    print("Skript durch Benutzer gestoppt.")
finally:
    # Close InfluxDB connection
    client.close()
    print("InfluxDB Client geschlossen.")
