# influxdays-2022-api-demo
Python code from influxdays 2022 api demo.
Code is currently set up for a local instance of influxdb but can easily be changed to work with the cloud.


<img align="right" width="250" height="250" src="https://user-images.githubusercontent.com/17863490/189961663-0d599bc4-687b-4ce4-aa96-940987d24533.png">


# management
Shows how to use the python client library to create orgs, buckets, tasks, and users.

`cd management`

`python3 demo.py --creds creds.toml --org devops.yaml`

# write
Shows how to write a file of data to an influxdb bucket.

`cd write`

`python3 demo.py`

# query
Shows how to query data out of influxdb.

`cd query`

`python3 demo.py`
