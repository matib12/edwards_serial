# edwards_serial
Python script for vacuum pressure monitoring using Edwards gauge via serial communication and InfluxDB.

# Dependencies
    pip install edwardsserial

# Init file for InfluxDB
A configuration file is necessary to connect to the InfluxDB database.

    [Influx]
    URL = http://SERVER_IP:8086  
    Token = YOUR_ACCESS_TOKEN  
    Org = YOUR_ORGANIZATION  
    Bucket = YOUR_BUCKET
      
    [Edwards]  
    Port = /dev/ttyUSB0
