#!/usr/bin/env python3
import time
import requests
from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# Configuration of InfluxDB
influxdb_url = 'http://<IPADDRESS>'
token = '<TOKEN>'
org = '<Organization>'
bucket = '<Bucket>'

client = InfluxDBClient(url=influxdb_url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

def fetch_and_store():
    response = requests.get('http://<IPADDRESS/dump1090/data/aircraft.json')
    data = response.json()

    for aircraft in data.get('aircraft', {}):
        flight_id = aircraft.get('flight', '').strip()
        if flight_id:
  
          # Datapoints for InfluxDB
          point = Point("aircraft_data").tag("flight", flight_id)
          point.field("flight_count", 1)
  
          timestamp = datetime.utcnow()
          point = point.time(timestamp)
  
          point = point.field("count", 1)
          point = point.field("lat", float(aircraft.get("lat", 0)))
          point = point.field("lon", float(aircraft.get("lon", 0)))
          point = point.field("nucp", aircraft.get("nucp", 0))
          point = point.field("seen_pos", float(aircraft.get("seen_pos", 0)))
          point = point.field("altitude", aircraft.get("altitude", 0))
          point = point.field("vert_rate", aircraft.get("vert_rate", 0))
          point = point.field("track", aircraft.get("track", 0))
          point = point.field("speed", aircraft.get("speed", 0))
          point = point.field("category", aircraft.get("category", ""))
          point = point.field("messages", aircraft.get("messages", 0))
          point = point.field("seen", float(aircraft.get("seen", 0)))
          point = point.field("rssi", float(aircraft.get("rssi", 0)))

          write_api.write(bucket=bucket, org=org, record=point)

while True:
  try:
    fetch_and_store()
  except Exception as e:
    print(f"Ein Fehler ist aufgetreten: {e}")
time.sleep(5)
