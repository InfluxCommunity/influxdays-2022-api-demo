#!/usr/bin/env python3
"""
Read in the vix.data file and send to the InfluxDB instance specified by the
config.toml file.
"""
import sys

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write_api import SYNCHRONOUS


def main():
    with open("vix.data", "r", encoding="utf-8") as file:
        data = file.readlines()

    with InfluxDBClient.from_config_file("creds.toml") as client:
        with client.write_api(write_options=SYNCHRONOUS) as write_api:
            try:
                write_api.write(bucket="testing", record=data)
            except InfluxDBError as e:
                print(e)

            print(f"successfully wrote {len(data)} metrics")


if __name__ == "__main__":
    sys.exit(main())
