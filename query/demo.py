#!/usr/bin/env python3
"""
Query the vix stock data for past 7 days. Print an example in JSON and CSV
formats.
"""
import sys

from influxdb_client import InfluxDBClient


def main():
    with InfluxDBClient.from_config_file("creds.toml") as client:
        result = client.query_api().query("""
            from(bucket: "testing")
                |> range(start: -7d)
                |> limit(n:1, offset: 0)
        """)
        print(result.to_json())

        csv_result = client.query_api().query_csv("""
            from(bucket: "testing")
                |> range(start: -7d)
                |> limit(n:1, offset: 0)
        """)

        for row in csv_result.to_values():
            print(",".join(row))


if __name__ == "__main__":
    sys.exit(main())
