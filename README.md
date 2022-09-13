## influxdays-2022-api-demo

ython code from influxdays 2022 api demo.
Code is currently set up for a local instance of influxdb but can easily be changed to work with InlfluxDB Cloud via updating the credentials files.

## Management

Demonstrates how to use the Python client library to create orgs, buckets, tasks, and users. This demo uses a YAML file to define a new organization with users, buckets, and predefined tasks that need to be applied. The YAML file is parsed and the various resources created if they do not already exist.

```shell
cd management
./demo.py
```

## Write

Demonstrates how to write a file of data to an InfluxDB bucket. This demo writes daily vix stock price data for the past couple of years. The data is already in Line Protocol, read in, and written in one big write. Users could adapte this demo to use batching for larger data sets.

```shell
cd write
./demo.py
```

## Query

Demonstrates how to query data out of an InfluxDB bucket and report the data in a couple different formats. In this demo, two idential Flux queries are used to pull out a single or couple of records from the previous write demo. Then the data is printed in both JSON and CSV formats.

```shell
cd query
./demo.py
```
