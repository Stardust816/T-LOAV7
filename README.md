# T-LOAV7
A private project using Grafana for displaying aviation data.

# Description
This project uses Grafana to visualize data from an ADS-B antenna.
It includes python scripts, Grafana panel configurations and examples for different types of visualization.

It uses dump1090 software (https://github.com/antirez/dump1090).
Dump1090 provides .json where you can get all the data from the aircrafts detected by your antenna.

Python scripts store the gathered data into a influxdb where the information is stored. The grafana instance uses the date from the database.


